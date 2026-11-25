# -*- coding: utf-8 -*-
"""切块：先按 Markdown 标题切，过长再按句子切，带重叠。"""
import re

SENT_END = "。！？；\n"


def _split_sections(text):
    """按 # 标题切成 (标题, 正文) 列表。"""
    sections = []
    title = ""
    buf = []
    for line in text.splitlines():
        if line.startswith("#"):
            if buf:
                sections.append((title, "\n".join(buf).strip()))
            title = line.lstrip("# ").strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        sections.append((title, "\n".join(buf).strip()))
    return [(t, b) for t, b in sections if b]


def _split_sentences(text):
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in SENT_END:
            out.append(cur)
            cur = ""
    if cur.strip():
        out.append(cur)
    return [s.strip() for s in out if s.strip()]


def split_text(text, chunk_size=350, overlap=60):
    """返回 [{'heading':..., 'text':...}]。"""
    chunks = []
    for heading, body in _split_sections(text):
        body = re.sub(r"\n{3,}", "\n\n", body)
        if len(body) <= chunk_size * 1.2:
            chunks.append({"heading": heading, "text": body})
            continue
        buf, size = "", 0
        for sent in _split_sentences(body):
            if size + len(sent) > chunk_size and buf:
                chunks.append({"heading": heading, "text": buf.strip()})
                buf = buf[-overlap:] if overlap > 0 else ""
                size = len(buf)
            buf += sent
            size += len(sent)
        if buf.strip():
            chunks.append({"heading": heading, "text": buf.strip()})
    for i, c in enumerate(chunks):
        c["id"] = i
        c["text"] = c["text"].strip()
    return chunks
