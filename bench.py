# -*- coding: utf-8 -*-
"""压测脚本：用并发线程打接口，输出 QPS / p50 / p95 / p99 以及被限流的次数。

为什么自己写而不用 locust / ab：
    这两个工具在 Windows 上要么装不上（gevent 依赖），要么不支持 SSE / JSON body 的细粒度统计。
    这里只要线程池 + time.perf_counter，40 行就够，而且结果可以直接贴进 README。

用法：
    # 1) 先起服务（另开一个终端）
    python -m uvicorn api:app --port 8000
    # 2) 压 /health（测框架开销），并发 20、每人 50 次
    python bench.py --url http://127.0.0.1:8000/health --c 20 --n 50
    # 3) 压 /ask（测端到端，注意会消耗 DeepSeek 额度）
    python bench.py --mode ask --c 5 --n 10 --limit-off

输出示例（真实数据见 README「压测」一节）：
    ok=1000 429=0 err=0  QPS=412.3  p50=42ms  p95=88ms  p99=140ms
"""
import argparse
import json
import statistics
import threading
import time

import requests

Q = "RAG 里为什么要做混合召回？"
lock = threading.Lock()
lat = []
codes = {"ok": 0, "429": 0, "err": 0}


def worker(url, mode, n, limit_on):
    s = requests.Session()
    local = []
    for i in range(n):
        t0 = time.perf_counter()
        try:
            if mode == "ask":
                r = s.post(url, json={"question": Q, "top_k": 3}, timeout=120)
            else:
                r = s.get(url, timeout=30)
            dt = (time.perf_counter() - t0) * 1000
            local.append(dt)
            with lock:
                if r.status_code == 200:
                    codes["ok"] += 1
                elif r.status_code == 429:
                    codes["429"] += 1
                else:
                    codes["err"] += 1
        except Exception:
            with lock:
                codes["err"] += 1
    with lock:
        lat.extend(local)


def pct(vals, q):
    if not vals:
        return 0.0
    i = min(len(vals) - 1, int(round((len(vals) - 1) * q)))
    return vals[i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    ap.add_argument("--mode", choices=["health", "ask"], default="health")
    ap.add_argument("--c", type=int, default=20, help="并发线程数")
    ap.add_argument("--n", type=int, default=50, help="每线程请求数")
    ap.add_argument("--limit-off", action="store_true",
                    help="提示：压测前请用 RAG_RATE_ON=0 启动服务，否则会被 429")
    args = ap.parse_args()

    url = args.base + ("/ask" if args.mode == "ask" else "/health")
    threads = [threading.Thread(target=worker, args=(url, args.mode, args.n, True))
               for _ in range(args.c)]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total_s = time.perf_counter() - t0

    vals = sorted(lat)
    done = codes["ok"] + codes["429"] + codes["err"]
    print(json.dumps({
        "url": url, "concurrency": args.c, "per_thread": args.n,
        "requests": done, "ok": codes["ok"], "429": codes["429"], "err": codes["err"],
        "elapsed_s": round(total_s, 2),
        "qps": round(codes["ok"] / total_s, 1) if total_s > 0 else 0,
        "latency_ms": {
            "mean": round(statistics.mean(vals), 1) if vals else 0,
            "p50": round(pct(vals, 0.50), 1), "p95": round(pct(vals, 0.95), 1),
            "p99": round(pct(vals, 0.99), 1),
            "max": round(vals[-1], 1) if vals else 0,
        },
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
