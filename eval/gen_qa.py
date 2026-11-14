# -*- coding: utf-8 -*-
"""从语料里合成评估集：抽块 -> 让大模型出题 -> 机器校验 -> 去重。

为什么要合成：人工写 45 道题要半天，而且容易只写自己记得住的点。
做法是工业界常用的「LLM 出题 + 规则校验」，但关键在于**校验**：
- evidence 必须是原片段里的原样字符串（否则命中判定会失真）
- keywords 至少命中一个（防止模型凭空编题）
- 问题必须能从片段回答，且不依赖片段外的常识

用法：
    python -m eval.gen_qa --n 45
"""
import argparse
import io
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.index import Index      # noqa: E402
from src.llm import chat         # noqa: E402

OUT = os.path.join(ROOT, "eval", "qa_docs.jsonl")

PROMPT = """你是检索评估集的出题人。给定一段技术文档片段，请出一道**中文问题**，要求：

1. 问题必须能**仅凭这段片段**回答，不能依赖片段外的常识
2. 问题要具体（问参数名、默认值、限制、步骤、区别），不要问"这段讲了什么"
3. 答案应该是片段里明确写着的某个事实
4. 同时给出 evidence：片段中**原样出现**的一句 10~30 字连续原文（用于自动判定命中）
5. 给出 2~3 个 keywords：答案里必须出现的关键词

只输出 JSON，不要解释：
{"question": "...", "evidence": "...", "keywords": ["...", "..."]}

片段（标题：__HEADING__）：
__TEXT__
"""


def clean_json(s):
    s = s.strip()
    s = re.sub(r"^```(?:json)?|```$", "", s, flags=re.M).strip()
    m = re.search(r"\{.*\}", s, re.S)
    return m.group(0) if m else s


def pick_chunks(chunks, n, seed=42):
    rng = random.Random(seed)
    cands = []
    for c in chunks:
        t = c["text"].strip()
        if 220 <= len(t) <= 900 and len(c.get("heading", "")) >= 4:
            cands.append(c)
    # 按来源站点分层，保证 deepseek / fastapi / mcp 都出题
    buckets = {}
    for c in cands:
        site = c.get("source", "").split("/")[0] or "misc"
        buckets.setdefault(site, []).append(c)
    out = []
    per = max(1, n // max(len(buckets), 1))
    for site, items in buckets.items():
        rng.shuffle(items)
        out.extend(items[:per])
    rng.shuffle(out)
    return out[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=45)
    ap.add_argument("--index", default=os.path.join(ROOT, "data", "index_docs"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    idx = Index.load(args.index)
    chunks = pick_chunks(idx.chunks, args.n, args.seed)
    print("候选块 %d 个，开始出题…" % len(chunks))

    rows, seen = [], []
    for i, c in enumerate(chunks, 1):
        try:
            ans = chat([{"role": "user", "content": PROMPT.replace("__HEADING__", c.get("heading", "")).replace("__TEXT__", c["text"][:1200])}],
                temperature=0, max_tokens=300)
        except Exception as e:
            print("  [%d] 调用失败 %s" % (i, type(e).__name__))
            continue
        try:
            obj = json.loads(clean_json(ans))
        except Exception:
            print("  [%d] JSON 解析失败" % i)
            continue

        q = (obj.get("question") or "").strip()
        ev = (obj.get("evidence") or "").strip()
        kws = obj.get("keywords") or []
        body = c.get("heading", "") + c["text"]

        if not (8 <= len(q) <= 60):
            continue
        if not ev or ev not in body:              # 证据必须原样存在
            continue
        if not any(k and k in body for k in kws):  # 关键词至少命中一个
            continue
        if any(_sim(q, s) > 0.72 for s in seen):   # 去重
            continue
        seen.append(q)
        rows.append({"q": q, "expect": ev, "source": c.get("source", ""),
                     "chunk_id": c.get("id")})
        print("  [%d] %s" % (i, q))

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("写入 %d 题 -> %s" % (len(rows), OUT))


def _sim(a, b):
    sa = set(a[i:i + 2] for i in range(len(a) - 1))
    sb = set(b[i:i + 2] for i in range(len(b) - 1))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / float(len(sa | sb))


if __name__ == "__main__":
    main()
