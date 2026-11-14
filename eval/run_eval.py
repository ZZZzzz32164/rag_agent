# -*- coding: utf-8 -*-
"""检索评估：Hit@K / MRR / 拒答率，支持对比多种检索模式。

用法：
    python -m eval.run_eval --k 3 --modes vector,keyword,hybrid
"""
import argparse
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.index import Index  # noqa: E402

THRESHOLDS = {"bge": 0.55, "lsa": 0.30, "hash": 0.20}


def load_qa(path):
    items = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def eval_mode(idx, qa, k, mode):
    hit, rr_sum, rows = 0, 0.0, []
    for item in qa:
        q, expect = item["q"], item["expect"]
        hits = idx.search(q, k, mode=mode)
        rank = 0
        for h in hits:
            if expect in (h["heading"] + h["text"]):
                rank = h["rank"]
                break
        if rank:
            hit += 1
            rr_sum += 1.0 / rank
        rows.append((q, expect, rank, hits[0]["heading"] if hits else "-"))
    n = len(qa)
    return hit, n, rr_sum / n if n else 0.0, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=os.path.join(ROOT, "data", "index_docs"))
    ap.add_argument("--qa", default=os.path.join(ROOT, "eval", "qa_docs.jsonl"))
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--modes", default="vector,keyword,hybrid")
    ap.add_argument("--oos", default=os.path.join(ROOT, "eval", "qa_out_of_scope.jsonl"))
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    idx = Index.load(args.index)
    qa = load_qa(args.qa)
    print("backend=%s dim=%d chunks=%d 题目=%d" %
          (idx.embedder.name, idx.vectors.shape[1], len(idx.chunks), len(qa)))
    print("-" * 60)
    print("%-10s %-14s %-8s" % ("模式", "Hit@%d" % args.k, "MRR"))
    results = {}
    for mode in [m.strip() for m in args.modes.split(",") if m.strip()]:
        hit, n, mrr, rows = eval_mode(idx, qa, args.k, mode)
        results[mode] = rows
        print("%-10s %-14s %-8.3f" % (mode, "%d/%d = %.0f%%" % (hit, n, 100.0 * hit / n), mrr))

    if args.verbose:
        for mode, rows in results.items():
            print("\n[%s] 明细" % mode)
            for q, expect, rank, top in rows:
                print("%s rank=%s | %s" % ("OK " if rank else "MISS", rank or "-", q))
                if not rank:
                    print("    期望：%s ｜ 召回第一：%s" % (expect, top))

    if args.oos and os.path.exists(args.oos):
        thr = THRESHOLDS.get(idx.embedder.name, 0.55)
        oos = load_qa(args.oos)
        ok = 0
        for item in oos:
            top = idx.search(item["q"], 1, mode="vector")[0]
            ok += 1 if top["score"] < thr else 0
        print("-" * 60)
        print("拒答（仅向量模式可比）：阈值=%.2f  %d/%d = %.0f%%" %
              (thr, ok, len(oos), 100.0 * ok / len(oos)))


if __name__ == "__main__":
    main()
