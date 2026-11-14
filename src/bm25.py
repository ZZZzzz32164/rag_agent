# -*- coding: utf-8 -*-
"""BM25 关键词检索：零依赖实现，中文用 jieba 分词。

为什么要它：向量检索擅长「意思相近」，但怕专有名词和数字
（比如问 "max_tokens 上限是多少"，向量可能召回一段讲 temperature 的话）。
BM25 正好相反——它靠词面命中，对术语精确。两者用 RRF 融合互补。
"""
import math
import re

import jieba

PUNCT = re.compile(r"^[\s\W_]+$", re.U)


def tokenize(text):
    return [w for w in jieba.lcut(text or "") if w.strip() and not PUNCT.match(w)]


class BM25(object):
    def __init__(self, docs, k1=1.5, b=0.75):
        """docs: list[str]"""
        self.k1, self.b = k1, b
        self.tokens = [tokenize(d) for d in docs]
        self.N = len(self.tokens)
        self.doc_len = [len(t) for t in self.tokens]
        self.avgdl = (sum(self.doc_len) / self.N) if self.N else 0.0
        self.tf = []
        self.df = {}
        for toks in self.tokens:
            counter = {}
            for w in toks:
                counter[w] = counter.get(w, 0) + 1
            self.tf.append(counter)
            for w in counter:
                self.df[w] = self.df.get(w, 0) + 1

    def idf(self, w):
        df = self.df.get(w, 0)
        return math.log(1.0 + (self.N - df + 0.5) / (df + 0.5))

    def scores(self, query):
        q_tokens = tokenize(query)
        out = [0.0] * self.N
        if not q_tokens:
            return out
        for i in range(self.N):
            tf, dl = self.tf[i], self.doc_len[i]
            s = 0.0
            for w in q_tokens:
                f = tf.get(w)
                if not f:
                    continue
                denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1.0))
                s += self.idf(w) * f * (self.k1 + 1) / denom
            out[i] = s
        return out
