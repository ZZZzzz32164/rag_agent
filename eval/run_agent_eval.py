# -*- coding: utf-8 -*-
"""端到端评估：真调 DeepSeek，看回答是否带合法引用、是否该拒答的拒答了。

用法：python -m eval.run_agent_eval --k 3
输出：回答率 / 带引用率 / 引用合法率 / 拒答正确率 / 平均耗时
"""
import argparse
import io
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.agent import RAGAgent  # noqa: E402


def load(path):
    rows = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=os.path.join(ROOT, "data", "index_docs"))
    ap.add_argument("--qa", default=os.path.join(ROOT, "eval", "qa_docs.jsonl"))
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 条，0 表示全跑")
    ap.add_argument("--out", default="", help="把结果写成 JSON，便于复现与对比")
    ap.add_argument("--mode", default="vector",
                    help="retrieval mode: vector | keyword | hybrid | hybrid_rerank")
    args = ap.parse_args()

    agent = RAGAgent(index_dir=args.index, top_k=args.k, mode=args.mode)
    qa = load(args.qa)
    if args.limit:
        qa = qa[:args.limit]

    n_cite = n_valid = 0
    t0 = time.time()
    print("== 库内问题 ==")
    for item in qa:
        r = agent.ask(item["q"])
        cited = r["cited"] if isinstance(r["cited"], dict) else {}
        good = bool(cited.get("has_citation")) and bool(cited.get("valid")) and not cited.get("invalid")
        n_cite += 1 if cited.get("has_citation") else 0
        n_valid += 1 if good else 0
        print("%s 引用=%s | %s" % ("OK  " if good else "WARN", cited.get("valid"), item["q"]))
        print("     %s" % r["answer"].replace("\n", " ")[:80])

    oos = load(os.path.join(ROOT, "eval", "qa_out_of_scope.jsonl"))
    n_ref = 0
    print("== 库外问题（应拒答）==")
    for item in oos:
        r = agent.ask(item["q"])
        ok = r["refused"]
        n_ref += 1 if ok else 0
        print("%s | %s" % ("拒答OK" if ok else "误答!!", item["q"]))

    dt = time.time() - t0
    total = len(qa) + len(oos)
    print("-" * 60)
    print("库内 %d 条：带引用 %d/%d  引用全部合法 %d/%d" % (len(qa), n_cite, len(qa), n_valid, len(qa)))
    print("库外 %d 条：拒答正确 %d/%d" % (len(oos), n_ref, len(oos)))
    print("总耗时 %.1fs，平均 %.2fs/题" % (dt, dt / max(total, 1)))

    if args.out:
        payload = {
            "index": os.path.relpath(args.index, ROOT).replace("\\", "/"),
            "k": args.k,
            "mode": args.mode,
            "in_scope": {"n": len(qa), "with_citation": n_cite, "all_valid": n_valid},
            "out_of_scope": {"n": len(oos), "refused": n_ref},
            "timing": {"total_s": round(dt, 1), "avg_s_per_q": round(dt / max(total, 1), 2)},
        }
        out_path = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)
        d = os.path.dirname(out_path)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with io.open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        print("结果已写入 %s" % out_path)


if __name__ == "__main__":
    main()
