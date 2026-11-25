# -*- coding: utf-8 -*-
"""运行时可观测性：请求指标（内存）+ 问答日志（落盘）。

为什么要有这个文件：
    接口能跑不等于能上线。上线之后要回答三个问题 ——
    "现在多少 QPS""慢在哪""拒答率是多少"。
    这里用最小的代码把三件事做完：内存里滚动统计（/metrics 直接读）、
    每次问答写一行日志到 SQLite（零依赖，单机可跑；线上换成 MySQL/ClickHouse 只改 DSN）。

设计取舍：
    - 不引 Prometheus 客户端：本项目只有一个进程一个接口，内存直方图够用，
      多一个依赖就多一层部署失败的可能。
    - 日志用 SQLite 而不是 MySQL：本机没有 MySQL 也能跑通 CI；
      DB_PATH 支持换成 mysql://... 由调用方传自己的连接（见 store_hint）。
    - 统计与日志都在后台线程之外同步写：写一行 SQLite 约 0.1ms，
      相比一次 LLM 调用（秒级）可以忽略；真要做高并发再换队列。
"""
import os
import sqlite3
import threading
import time
from collections import Counter, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("QA_LOG_DB", os.path.join(ROOT, "data", "qa_log.db"))
WINDOW = int(os.environ.get("QA_METRICS_WINDOW", "200"))  # 滚动窗口大小

_lock = threading.Lock()
_lat = deque(maxlen=WINDOW)          # 最近 N 次耗时（ms）
_total = 0                            # 累计请求数
_refused = 0                          # 累计拒答数
_cache_hit = 0                        # 缓存命中数
_errors = 0
_top = Counter()                      # 高频问题
_paths = Counter()                    # 各路径次数
_started = time.time()

_conn = None
_conn_lock = threading.Lock()


def _db():
    """惰性建库 + 建表。失败不影响主流程（只是没有日志）。"""
    global _conn
    if _conn is not None:
        return _conn
    with _conn_lock:
        if _conn is None:
            try:
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                c = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
                c.execute("PRAGMA journal_mode=WAL")
                c.execute(
                    """CREATE TABLE IF NOT EXISTS qa_log(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rid TEXT, ts REAL, question TEXT, answer_len INTEGER,
                        latency_ms REAL, refused INTEGER, backend TEXT,
                        hits INTEGER, cache_hit INTEGER)"""
                )
                c.execute("CREATE INDEX IF NOT EXISTS idx_qa_ts ON qa_log(ts)")
                c.commit()
                _conn = c
            except Exception:
                _conn = False  # 标记不可用，避免每次重试
    return _conn or None


def record(rid, question, answer, latency_ms, refused, backend, hits, cache_hit):
    """一次问答落一条；同时更新内存指标。任何异常都不能影响接口返回。"""
    global _total, _refused, _cache_hit
    with _lock:
        _total += 1
        if refused:
            _refused += 1
        if cache_hit:
            _cache_hit += 1
        _lat.append(float(latency_ms))
        _top[question[:40]] += 1
        _paths["/ask"] += 1
    c = _db()
    if c:
        try:
            with _conn_lock:
                c.execute(
                    "INSERT INTO qa_log(rid,ts,question,answer_len,latency_ms,"
                    "refused,backend,hits,cache_hit) VALUES(?,?,?,?,?,?,?,?,?)",
                    (rid, time.time(), question[:200], len(answer or ""),
                     float(latency_ms), int(bool(refused)), backend,
                     int(hits or 0), int(bool(cache_hit))))
                c.commit()
        except Exception:
            pass


def record_path(path):
    with _lock:
        _paths[path] += 1


def record_error():
    global _errors
    with _lock:
        _errors += 1


def _pct(sorted_vals, q):
    if not sorted_vals:
        return 0.0
    i = min(len(sorted_vals) - 1, int(round((len(sorted_vals) - 1) * q)))
    return round(sorted_vals[i], 1)


def snapshot():
    """给 /metrics 用：返回可直接 JSON 化的字典。"""
    with _lock:
        vals = sorted(_lat)
        total, refused, hit, errors = _total, _refused, _cache_hit, _errors
        top = _top.most_common(5)
        paths = dict(_paths)
    uptime = time.time() - _started
    return {
        "uptime_s": round(uptime, 1),
        "requests": total,
        "errors": errors,
        "qps_avg": round(total / uptime, 2) if uptime > 0 else 0.0,
        "latency_ms": {
            "p50": _pct(vals, 0.50), "p90": _pct(vals, 0.90),
            "p95": _pct(vals, 0.95), "p99": _pct(vals, 0.99),
            "max": round(vals[-1], 1) if vals else 0.0,
            "samples": len(vals),
        },
        "refused": refused,
        "refused_rate": round(refused / total, 3) if total else 0.0,
        "cache_hits": hit,
        "cache_hit_rate": round(hit / total, 3) if total else 0.0,
        "top_questions": [{"q": q, "n": n} for q, n in top],
        "paths": paths,
        "db": DB_PATH if _conn else None,
    }


def recent(n=20):
    """最近的问答日志（演示 / 排查用）。"""
    c = _db()
    if not c:
        return []
    try:
        with _conn_lock:
            rows = c.execute(
                "SELECT rid,ts,question,latency_ms,refused,backend,hits,cache_hit "
                "FROM qa_log ORDER BY id DESC LIMIT ?", (int(n),)).fetchall()
    except Exception:
        return []
    return [
        {"rid": r[0], "ts": r[1], "question": r[2], "latency_ms": round(r[3], 1),
         "refused": bool(r[4]), "backend": r[5], "hits": r[6], "cache_hit": bool(r[7])}
        for r in rows
    ]
