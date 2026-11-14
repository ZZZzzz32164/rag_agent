# -*- coding: utf-8 -*-
"""上下文预算：token 计数、按预算裁剪、摘要压缩、长期记忆落盘。"""
import io
import json
import os

try:  # 有 tiktoken 就用真实 token
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text):
        return len(_ENC.encode(text or ""))

    TOKENIZER = "tiktoken/cl100k_base"
except Exception:  # noqa: BLE001
    def count_tokens(text):
        """保守估算：中文按 1 字 ≈ 1 token，英文按 4 字符 ≈ 1 token。"""
        text = text or ""
        cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
        other = len(text) - cjk
        return int(cjk + other / 4.0) + 1

    TOKENIZER = "char-estimate"


def msg_tokens(msg):
    content = msg.get("content") or ""
    return count_tokens(content) + 4  # 角色等固定开销


class ContextManager(object):
    """保留 system + 从最新往前的消息，超出预算的更早消息压成摘要。"""

    def __init__(self, budget=3000, keep_recent=6):
        self.budget = budget
        self.keep_recent = keep_recent

    def fit(self, messages, summarize=None):
        system = [m for m in messages if m.get("role") == "system"]
        rest = [m for m in messages if m.get("role") != "system"]
        fixed = sum(msg_tokens(m) for m in system)
        budget = max(self.budget - fixed, 200)

        kept, used = [], 0
        for m in reversed(rest):
            t = msg_tokens(m)
            if used + t > budget and len(kept) >= self.keep_recent:
                break
            kept.append(m)
            used += t
        kept.reverse()

        dropped = rest[: len(rest) - len(kept)]
        if dropped and summarize:
            summary = summarize(dropped)
            if summary:
                kept.insert(0, {"role": "system", "content": "【更早对话摘要】" + summary})
        return system + kept


class LongTermMemory(object):
    """长期记忆：明确说出的事实才写入，避免闲聊污染。"""

    def __init__(self, path):
        self.path = path
        self.facts = []
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                self.facts = json.load(f)

    def add(self, fact):
        fact = (fact or "").strip()
        if not fact or fact in self.facts:
            return False
        self.facts.append(fact)
        self._save()
        return True

    def render(self, limit=10):
        if not self.facts:
            return ""
        return "【长期记忆】" + "；".join(self.facts[-limit:])

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with io.open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.facts, f, ensure_ascii=False, indent=1)
