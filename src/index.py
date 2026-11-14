# -*- coding: utf-8 -*-
"""索引：把知识库切块 -> 向量化 -> 落盘 -> 检索。"""
import io
import json
import os

import numpy as np

from .chunking import split_text
from .embedder import build_embedder

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


class Index(object):
    def __init__(self, chunks, vectors, embedder):
        self.chunks = chunks
        self.vectors = vectors
        self.embedder = embedder

    # ---------- 构建 ----------
    @classmethod
    def build(cls, knowledge_dir, chunk_size=500, overlap=80, backend="auto"):
        texts = []
        for name in sorted(os.listdir(knowledge_dir)):
            if not name.lower().endswith((".md", ".txt")):
                continue
            path = os.path.join(knowledge_dir, name)
            with io.open(path, encoding="utf-8") as f:
                raw = f.read()
            for c in split_text(raw, chunk_size=chunk_size, overlap=overlap):
                c["source"] = name
                texts.append(c)
        if not texts:
            raise RuntimeError("知识库为空: %s" % knowledge_dir)

        corpus = [c["heading"] + "\n" + c["text"] for c in texts]
        embedder = build_embedder(backend, corpus=corpus)
        vectors = embedder.encode(corpus)
        return cls(texts, vectors, embedder)

    # ---------- 持久化 ----------
    def save(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        np.save(os.path.join(out_dir, "vectors.npy"), self.vectors)
        with io.open(os.path.join(out_dir, "chunks.json"), "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=1)
        meta = {"backend": self.embedder.name, "dim": int(self.vectors.shape[1]),
                "n_chunks": len(self.chunks)}
        with io.open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)
        if self.embedder.name == "lsa":
            import joblib

            joblib.dump({"vec": self.embedder._vec, "svd": self.embedder._svd},
                        os.path.join(out_dir, "embedder.joblib"))
        return meta

    @classmethod
    def load(cls, index_dir):
        with io.open(os.path.join(index_dir, "chunks.json"), encoding="utf-8") as f:
            chunks = json.load(f)
        vectors = np.load(os.path.join(index_dir, "vectors.npy"))
        with io.open(os.path.join(index_dir, "meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
        if meta["backend"] == "lsa":
            import joblib

            from .embedder import LSAEmbedder

            saved = joblib.load(os.path.join(index_dir, "embedder.joblib"))
            emb = LSAEmbedder()
            emb._vec, emb._svd = saved["vec"], saved["svd"]
            emb.dim = meta["dim"]
        else:
            emb = build_embedder(meta["backend"])
        return cls(chunks, vectors, emb)

    # ---------- 检索 ----------
    def search(self, query, top_k=3):
        # 查询侧若后端支持指令前缀，就走 encode_query（bge 官方建议）
        enc = getattr(self.embedder, "encode_query", None) or self.embedder.encode
        q = enc([query])[0]
        scores = self.vectors.dot(q)
        order = np.argsort(-scores)[:top_k]
        out = []
        for rank, i in enumerate(order):
            c = dict(self.chunks[int(i)])
            c["score"] = float(scores[int(i)])
            c["rank"] = rank + 1
            out.append(c)
        return out

    def context(self, hits):
        """拼成带编号的上下文，供 prompt 使用。"""
        lines = []
        for i, h in enumerate(hits):
            lines.append("[%d] （%s · %s）\n%s" % (i + 1, h.get("source", ""), h.get("heading", ""), h["text"]))
        return "\n\n".join(lines)


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "stats", "query"])
    ap.add_argument("--data", default=os.path.join(ROOT, "data", "knowledge"))
    ap.add_argument("--index", default=os.path.join(ROOT, "data", "index"))
    ap.add_argument("--backend", default="auto")
    ap.add_argument("--q", default="")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    if args.cmd == "build":
        idx = Index.build(args.data, backend=args.backend)
        meta = idx.save(args.index)
        print("built:", meta)
    elif args.cmd == "stats":
        idx = Index.load(args.index)
        print("backend=%s dim=%d chunks=%d" % (idx.embedder.name, idx.vectors.shape[1], len(idx.chunks)))
        for c in idx.chunks:
            print("  [%d] %s | %d 字" % (c["id"], c["heading"], len(c["text"])))
    else:
        idx = Index.load(args.index)
        for h in idx.search(args.q, args.k):
            print("rank=%d score=%.4f %s" % (h["rank"], h["score"], h["heading"]))


if __name__ == "__main__":
    main()
