# -*- coding: utf-8 -*-
"""接口限流：令牌桶（token bucket），按客户端 IP 分桶。

为什么用令牌桶而不是固定窗口：
    固定窗口在窗口边界会放过 2 倍流量（59s 和 61s 各打满一次）。
    令牌桶按时间连续补充，能保证长期平均速率，同时允许短时突发（就是这个项目的场景：
    前端连续问几句，正常；爬虫式并发，要挡住）。

用法：
    rl = TokenBucket(rate=5, burst=10)   # 平均 5 rps，最多突发 10
    ok, retry_after = rl.take(key)
    if not ok: return 429 + Retry-After

线程安全：用一把锁保护字典；桶只在命中时更新（避免定时清理线程）。
"""
import threading
import time


class TokenBucket(object):
    def __init__(self, rate=5.0, burst=10.0):
        self.rate = float(rate)      # 每秒补充多少令牌
        self.burst = float(burst)    # 桶容量 = 允许的最大突发
        self._lock = threading.Lock()
        self._buckets = {}           # key -> [tokens, last_ts]

    def _now(self):
        return time.time()

    def take(self, key, cost=1.0):
        """取一个令牌；返回 (是否放行, 建议等待秒数)。"""
        now = self._now()
        with self._lock:
            tokens, last = self._buckets.get(key, (self.burst, now))
            tokens = min(self.burst, tokens + (now - last) * self.rate)
            if tokens >= cost:
                self._buckets[key] = (tokens - cost, now)
                return True, 0.0
            self._buckets[key] = (tokens, now)
            need = (cost - tokens) / self.rate
            return False, need

    def state(self, key):
        """当前剩余令牌（/metrics 里展示用）。"""
        now = self._now()
        with self._lock:
            tokens, last = self._buckets.get(key, (self.burst, now))
            tokens = min(self.burst, tokens + (now - last) * self.rate)
            return {"tokens": round(tokens, 2), "rate": self.rate, "burst": self.burst}

    def gc(self, idle=600.0):
        """清理长时间不活跃的桶，防止按 IP 无限增长。"""
        now = self._now()
        with self._lock:
            dead = [k for k, (_, last) in self._buckets.items() if now - last > idle]
            for k in dead:
                self._buckets.pop(k, None)
            return len(dead)
