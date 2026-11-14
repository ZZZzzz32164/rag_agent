# -*- coding: utf-8 -*-
"""RAG Agent：检索 -> 带编号上下文 -> 强制引用 -> 生成后校验引用。"""
import os
import re

from .index import Index

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYSTEM = (
    "你是一个只依据给定资料回答问题的助手。规则：\n"
    "1. 只能使用【参考资料】中的内容作答，不要引入资料以外的知识；\n"
    "2. 每个结论后面必须标注来源编号，格式如 [1]、[2]，可以多个；\n"
    "3. 如果参考资料里没有答案，直接回答「资料中没有相关内容」，不要猜测；\n"
    "4. 回答用中文，简洁，控制在 200 字以内。"
)

SCORE_THRESHOLD = 0.55  # bge 余弦相似度低于此值视为「资料里没有」，直接拒答
THRESHOLD_BY_BACKEND = {"bge": 0.55, "lsa": 0.30, "hash": 0.20}  # 三种后端分数量纲不同


class RAGAgent(object):
    def __init__(self, index=None, index_dir=None, top_k=3, llm=None, threshold=None):
        self.index = index or Index.load(index_dir or os.path.join(ROOT, "data", "index"))
        self.top_k = top_k
        self._llm = llm
        self.threshold = threshold if threshold is not None else \
            THRESHOLD_BY_BACKEND.get(self.index.embedder.name, SCORE_THRESHOLD)

    def _call(self, messages):
        if self._llm:
            return self._llm(messages)
        from . import llm as llm_mod

        return llm_mod.chat(messages)

    def retrieve(self, question):
        return self.index.search(question, self.top_k)

    def ask(self, question):
        hits = self.retrieve(question)
        if not hits or hits[0]["score"] < self.threshold:
            return {"answer": "资料中没有相关内容。", "hits": hits, "cited": [], "refused": True}

        prompt = "【参考资料】\n%s\n\n【问题】%s\n\n请依据资料回答，并标注来源编号。" % (
            self.index.context(hits), question)
        answer = self._call([
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ])
        return {"answer": answer, "hits": hits,
                "cited": check_citations(answer, len(hits)), "refused": False}


def check_citations(answer, n_hits):
    """抽出版本号和非法编号（指向不存在的资料）。"""
    nums = [int(x) for x in re.findall(r"\[(\d+)\]", answer or "")]
    valid = sorted(set(x for x in nums if 1 <= x <= n_hits))
    invalid = sorted(set(x for x in nums if x < 1 or x > n_hits))
    return {"valid": valid, "invalid": invalid, "has_citation": bool(nums)}


def main():
    import argparse
    import json

    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--no-llm", action="store_true", help="只检索不生成，用于免 key 自测")
    args = ap.parse_args()

    agent = RAGAgent(top_k=args.k)
    if args.no_llm:
        for h in agent.retrieve(args.question):
            print("rank=%d score=%.3f %s" % (h["rank"], h["score"], h["heading"]))
        return
    print(json.dumps(agent.ask(args.question), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
