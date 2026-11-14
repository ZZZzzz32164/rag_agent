# -*- coding: utf-8 -*-
"""DeepSeek 调用封装：超时、限流、5xx 重试；只重试可恢复错误。"""
import os

import requests

BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
TIMEOUT = 60
RETRIES = 3


def _load_dotenv():
    """从项目根目录的 .env 读 key，避免把密钥写进代码。"""
    if os.environ.get("DEEPSEEK_API_KEY"):
        return
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def chat(messages, temperature=0.0, max_tokens=800, model=None):
    _load_dotenv()
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        raise RuntimeError("缺少 DEEPSEEK_API_KEY：在项目根目录 .env 里写 DEEPSEEK_API_KEY=sk-xxx")
    url = BASE_URL.rstrip("/") + "/chat/completions"
    payload = {
        "model": model or MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}

    last = None
    for i in range(RETRIES):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
            if r.status_code in (429, 500, 502, 503, 504):
                last = "HTTP %d" % r.status_code
                raise RuntimeError(last)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            last = "%s: %s" % (type(exc).__name__, exc)
            if i == RETRIES - 1:
                break
            import time

            time.sleep(2 * (i + 1))
    raise RuntimeError("调用失败（重试 %d 次）：%s" % (RETRIES, last))
