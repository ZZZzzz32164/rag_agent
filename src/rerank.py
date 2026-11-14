# -*- coding: utf-8 -*-
"""重排：先召回一批（pool），再用 cross-encoder 逐对打分精排。

为什么要它：向量和 BM25 都是"双塔"思路，query 与文档各自编码、最后算相似度，
看不到两者的交互；cross-encoder 把 (query, 文档) 拼在一起送进模型，精度高得多，
代价是慢——所以只对前 pool 条做，不做全量。

模型：BAAI/bge-reranker-base（约 1.1GB，CPU 可跑）。
"""
import os


class Reranker(object):
    def __init__(self, model_name=None):
        self.model_name = model_name or os.environ.get(
            "RERANK_MODEL", "BAAI/bge-reranker-base")
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name, max_length=512)
        return self._model

    def rerank(self, query, hits, top_k=3):
        """hits: [{'chunk', 'score', ...}]，返回按 cross-encoder 分数重排后的 top_k。"""
        if not hits:
            return hits
        pairs = [(query, h["text"][:512]) for h in hits]
        scores = self.model.predict(pairs, show_progress_bar=False)
        for h, s in zip(hits, scores):
            h["rerank_score"] = float(s)
        out = sorted(hits, key=lambda x: -x["rerank_score"])[:top_k]
        for i, h in enumerate(out, 1):
            h["rank"] = i
        return out


_RERANKER = None


def get_reranker():
    global _RERANKER
    if _RERANKER is None:
        _RERANKER = Reranker()
    return _RERANKER
