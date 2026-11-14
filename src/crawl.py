# -*- coding: utf-8 -*-
"""抓取公开技术文档，构建项目自己的知识库语料。

为什么自己抓而不用现成 txt：面试官问「你的知识库哪来的」，
答「我写了三篇笔记」和答「我从 X 个文档页抓的、抓了 N 页 N 万字」是两个量级。

礼貌与边界：
- 只爬白名单域名下的文档页
- 每个请求间隔 >= 0.8s，带正常 UA
- 只抓正文，不抓登录内容、不绕反爬
- 结果落盘成 markdown，来源 URL 记在文件头

用法：
    python -m src.crawl --limit 40          # 每个站点最多 40 页
    python -m src.crawl --site deepseek     # 只抓某个站点
"""
import argparse
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "corpus")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

SITES = {
    "deepseek": {
        "sitemap": "https://api-docs.deepseek.com/sitemap.xml",
        "include": r"^https://api-docs\.deepseek\.com/",
        "exclude": r"/(img|assets|static)/",
        "prefix_zh": True,
    },
    "fastapi": {
        "sitemap": "https://fastapi.tiangolo.com/zh/sitemap.xml",
        "include": r"^https://fastapi\.tiangolo\.com/zh/",
        "exclude": r"/(img|assets|static|release-notes)/",
    },
    "mcp": {
        "sitemap": "https://modelcontextprotocol.io/sitemap.xml",
        "include": r"^https://modelcontextprotocol\.io/",
        "exclude": r"/(img|assets|static|api)/",
    },
}


def get(url, timeout=20):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"
    return r


def urls_from_sitemap(sitemap, include, exclude, limit):
    r = get(sitemap)
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text)
    out = []
    for u in locs:
        if not re.search(include, u):
            continue
        if exclude and re.search(exclude, u):
            continue
        out.append(u.split("#")[0])
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq[:limit]


def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg"]):
        tag.decompose()
    main = (soup.find("article") or soup.find("main")
            or soup.find(class_=re.compile(r"(markdown|content|doc|prose)", re.I)) or soup.body)
    if main is None:
        return ""
    lines = []
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "td"]):
        txt = el.get_text(" ", strip=True)
        if not txt:
            continue
        if el.name in ("h1", "h2", "h3", "h4"):
            level = int(el.name[1])
            lines.append("\n" + "#" * level + " " + txt)
        elif el.name == "li":
            lines.append("- " + txt)
        elif el.name == "pre":
            if len(txt) > 400:      # 超长代码块进语料会淹掉语义
                continue
            lines.append("```\n" + txt + "\n```")
        else:
            lines.append(txt)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def safe_name(url):
    path = re.sub(r"^https?://", "", url)
    path = re.sub(r"[^0-9A-Za-z\u4e00-\u9fa5]+", "_", path).strip("_")
    return (path[:80] or "index") + ".md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="all")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--delay", type=float, default=0.8)
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    names = list(SITES) if args.site == "all" else [args.site]
    total = 0
    for name in names:
        cfg = SITES[name]
        site_dir = os.path.join(OUT_DIR, name)
        os.makedirs(site_dir, exist_ok=True)
        try:
            urls = urls_from_sitemap(cfg["sitemap"], cfg["include"], cfg["exclude"], args.limit)
        except Exception as e:
            print("[skip] %s: %s" % (name, e))
            continue
        print("[%s] %d 个待抓页面" % (name, len(urls)))
        for u in tqdm(urls, ncols=70):
            if cfg.get("prefix_zh") and "/zh-cn/" not in u and not u.endswith("/zh-cn/"):
                pass  # DeepSeek 站点本身就是中文，不需要过滤
            fp = os.path.join(site_dir, safe_name(u))
            if os.path.exists(fp) and os.path.getsize(fp) > 200:
                total += 1
                continue
            try:
                r = get(u)
                text = html_to_text(r.text)
                if len(text) < 300:
                    continue
                with open(fp, "w", encoding="utf-8") as f:
                    f.write("<!-- source: %s -->\n" % u)
                    f.write(text + "\n")
                total += 1
            except Exception as e:
                print("  [fail] %s (%s)" % (u, type(e).__name__))
            time.sleep(args.delay)
    print("完成，共 %d 个文件 -> %s" % (total, OUT_DIR))


if __name__ == "__main__":
    main()
