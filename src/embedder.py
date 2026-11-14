# -*- coding: utf-8 -*-
"""可插拔向量后端：bge（真实语义）/ lsa（TF-IDF+SVD 降维）/ hash（零依赖兜底）。"""
import hashlib

import numpy as np


class BaseEmbedder(object):
    name = "base"
    dim = 0

    def encode(self, texts):
        raise NotImplementedError


class HashEmbedder(BaseEmbedder):
    """md5 特征哈希，不依赖任何模型，用来在没有网络时跑通链路。"""

    name = "hash"

    def __init__(self, dim=1024):
        self.dim = dim

    def encode(self, texts):
        m = np.zeros((len(texts), self.dim), dtype="float32")
        for i, t in enumerate(texts):
            for token in list(t) + t.split():
                h = hashlib.md5(token.encode("utf-8")).hexdigest()
                m[i, int(h[:8], 16) % self.dim] += 1.0
        return _normalize(m)


class LSAEmbedder(BaseEmbedder):
    """词袋 TF-IDF 经 SVD 压成稠密向量，纯 sklearn，无需下载模型。"""

    name = "lsa"

    def __init__(self, dim=256, ngram=(1, 2)):
        self.dim = dim
        self.ngram = ngram
        self._vec = None
        self._svd = None

    def fit(self, corpus):
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer

        self._vec = TfidfVectorizer(analyzer="char", ngram_range=self.ngram, min_df=1)
        x = self._vec.fit_transform(corpus)
        k = min(self.dim, max(2, min(x.shape) - 1))
        self._svd = TruncatedSVD(n_components=k, random_state=42)
        self._svd.fit(x)
        self.dim = k
        return self

    def encode(self, texts):
        x = self._vec.transform(texts)
        return _normalize(self._svd.transform(x).astype("float32"))


class BgeEmbedder(BaseEmbedder):
    """bge-small-zh：真实语义向量，需要 sentence-transformers。"""

    name = "bge"

    def __init__(self, model="BAAI/bge-small-zh-v1.5"):
        from sentence_transformers import SentenceTransformer

        self.model_name = model
        self.model = SentenceTransformer(model)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts):
        vecs = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.asarray(vecs, dtype="float32")


def build_embedder(kind="auto", corpus=None):
    """auto: 有 sentence-transformers 就用 bge，否则退回 lsa。"""
    if kind in ("auto", "bge"):
        try:
            return BgeEmbedder()
        except Exception as exc:  # noqa: BLE001
            if kind == "bge":
                raise
            print("[embedder] bge 不可用（%s），退回 lsa" % type(exc).__name__)
            kind = "lsa"
    if kind == "lsa":
        if corpus is None:
            raise ValueError("lsa 后端需要 corpus 才能 fit")
        return LSAEmbedder().fit(corpus)
    if kind == "hash":
        return HashEmbedder()
    raise ValueError("未知后端: %s" % kind)


def _normalize(m):
    norm = np.linalg.norm(m, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    return (m / norm).astype("float32")
