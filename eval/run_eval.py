# -*- coding: utf-8 -*-
"""检索评估：Hit@K 与 MRR。用法：
    python -m eval.run_eval --k 3
"""
import argparse
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.index import Index  # noqa: E402


def load_qa(path):
    items = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=os.path.join(ROOT, "data", "index"))
    ap.add_argument("--qa", default=os.path.join(ROOT, "eval", "qa_set.jsonl"))
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--oos", default=os.path.join(ROOT, "eval", "qa_out_of_scope.jsonl"))
    args = ap.parse_args()

    idx = Index.load(args.index)
    qa = load_qa(args.qa)

    hit, rr_sum, rows = 0, 0.0, []
    for item in qa:
        q, expect = item["q"], item["expect"]
        hits = idx.search(q, args.k)
        rank = 0
        for h in hits:
            if expect in (h["heading"] + h["text"]):
                rank = h["rank"]
                break
        if rank:
            hit += 1
            rr_sum += 1.0 / rank
        rows.append((q, expect, rank, hits[0]["heading"] if hits else "-", hits[0]["score"] if hits else 0))

    n = len(qa)
    print("backend=%s dim=%d chunks=%d" % (idx.embedder.name, idx.vectors.shape[1], len(idx.chunks)))
    print("Hit@%d = %d/%d = %.1f%%    MRR = %.3f" % (args.k, hit, n, 100.0 * hit / n, rr_sum / n))
    print("-" * 72)
    for q, expect, rank, top, score in rows:
        flag = "OK " if rank else "MISS"
        print("%s rank=%s score=%.3f | %s" % (flag, rank or "-", score, q))
        if not rank:
            print("     期望关键词：%s ｜ 召回第一名：%s" % (expect, top))

    # 拒答测试：知识库外的问题，最高分低于阈值才算正确拒答
    if args.oos and os.path.exists(args.oos):
        thr = {"bge": 0.55, "lsa": 0.30, "hash": 0.20}.get(idx.embedder.name, 0.55)
        oos = load_qa(args.oos)
        ok = 0
        print("-" * 72)
        for item in oos:
            top = idx.search(item["q"], 1)[0]
            refused = top["score"] < thr
            ok += 1 if refused else 0
            print("%s score=%.3f | %s" % ("拒答OK " if refused else "误答!!", top["score"], item["q"]))
        print("阈值=%.2f  拒答正确率 = %d/%d = %.1f%%" % (thr, ok, len(oos), 100.0 * ok / len(oos)))


if __name__ == "__main__":
    main()

