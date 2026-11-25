# -*- coding: utf-8 -*-
"""FastAPI 服务层：把 RAG Agent 暴露成 HTTP 接口（同步 + SSE 流式）。

启动：
    uvicorn api:app --host 0.0.0.0 --port 8000
    # 或 python -m uvicorn api:app --port 8000

接口：
    GET  /health          服务与索引状态
    POST /ask             {question, top_k} -> 回答 + 引用 + 命中片段
    POST /ask/stream      同上，但用 SSE 逐字返回
    GET  /                简单 HTML 演示页（无需前端构建）
"""
import json
import logging
import os
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from src.agent import SYSTEM, RAGAgent
from src.llm import chat_stream

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.environ.get("RAG_INDEX_DIR", os.path.join(ROOT, "data", "index"))

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("rag-api")

app = FastAPI(title="RAG QA API", version="1.0",
              description="检索增强问答：bge 向量 + BM25/RRF 融合 + cross-encoder 精排 + 引用溯源与拒答")
_agent = None


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """每个请求带一个 id，日志里能对上；也方便在客户端报错时定位。"""
    rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
    t0 = time.time()
    response = await call_next(request)
    cost = (time.time() - t0) * 1000
    response.headers["X-Request-ID"] = rid
    log.info("%s %s -> %d %.0fms rid=%s", request.method, request.url.path,
             response.status_code, cost, rid)
    return response


@app.exception_handler(RuntimeError)
async def upstream_error(request: Request, exc: RuntimeError):
    """上游（DeepSeek）不可用 / 没配 key：返回 503，别让客户端看到 500 堆栈。"""
    log.warning("upstream error: %s", exc)
    return JSONResponse(status_code=503,
                        content={"error": {"code": "upstream_unavailable",
                                           "message": str(exc)}})


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    log.exception("unhandled error")
    return JSONResponse(status_code=500,
                        content={"error": {"code": "internal_error",
                                           "message": type(exc).__name__}})



def agent():
    """懒加载：第一次请求时再载索引，避免启动时卡在模型下载。"""
    global _agent
    if _agent is None:
        _agent = RAGAgent(index_dir=INDEX_DIR)
    return _agent


class AskIn(BaseModel):
    question: str = Field(..., min_length=1, description="用户问题")
    top_k: int = Field(3, ge=1, le=10)


@app.get("/health")
def health():
    a = agent()
    return {
        "status": "ok",
        "backend": a.index.embedder.name,
        "dim": int(a.index.vectors.shape[1]),
        "chunks": len(a.index.chunks),
        "threshold": a.threshold,
        "top_k": a.top_k,
        "has_llm_key": bool(os.environ.get("DEEPSEEK_API_KEY")),
    }


@app.post("/ask")
def ask(body: AskIn):
    a = agent()
    a.top_k = body.top_k
    r = a.ask(body.question)
    # 两道拒答：检索分低于阈值（agent 内部已判），或模型自己说"资料中没有"
    # —— 后者在库里没答案但检索分略高于阈值时会出现，不补这一步 refused 会误报 False。
    refused = bool(r["refused"]) or ("资料中没有相关内容" in (r.get("answer") or ""))
    return {
        "question": body.question,
        "answer": r["answer"],
        "refused": refused,
        "citations": r["cited"],
        "hits": [
            {"rank": h["rank"], "score": round(h["score"], 3),
             "heading": h["heading"], "source": h["source"]}
            for h in r["hits"]
        ],
    }


@app.post("/ask/stream")
def ask_stream(body: AskIn):
    a = agent()
    hits = a.retrieve(body.question)

    def gen():
        # 先发引用信息，前端可以先渲染来源列表
        yield "event: hits\ndata: %s\n\n" % json.dumps(
            [{"rank": h["rank"], "score": round(h["score"], 3), "heading": h["heading"]}
             for h in hits], ensure_ascii=False)
        if not hits or hits[0]["score"] < a.threshold:
            yield "event: token\ndata: %s\n\n" % json.dumps("资料中没有相关内容。", ensure_ascii=False)
            yield "event: done\ndata: %s\n\n" % json.dumps({"refused": True}, ensure_ascii=False)
            return
        prompt = "【参考资料】\n%s\n\n【问题】%s\n\n请依据资料回答，并标注来源编号。" % (
            a.index.context(hits), body.question)
        try:
            for piece in chat_stream([{"role": "system", "content": SYSTEM},
                                      {"role": "user", "content": prompt}]):
                yield "event: token\ndata: %s\n\n" % json.dumps(piece, ensure_ascii=False)
            yield "event: done\ndata: %s\n\n" % json.dumps({"refused": False}, ensure_ascii=False)
        except Exception as exc:  # noqa: BLE001
            yield "event: error\ndata: %s\n\n" % json.dumps(str(exc), ensure_ascii=False)

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


DEMO = """<!doctype html><meta charset="utf-8"><title>RAG 问答演示</title>
<style>body{font-family:system-ui;max-width:760px;margin:40px auto;padding:0 16px;line-height:1.7}
input{width:100%;padding:10px;font-size:16px;border:1px solid #ccc;border-radius:8px}
pre{background:#f6f8fa;padding:14px;border-radius:8px;white-space:pre-wrap}
small{color:#666}</style>
<h2>RAG 知识库问答</h2>
<p><small>只依据 <code>data/knowledge/</code> 里的资料回答，回答带 [n] 引用；资料里没有就拒答。</small></p>
<input id="q" placeholder="比如：为什么要留重叠？" />
<p><button onclick="go()">提问</button></p>
<pre id="out">等待提问…</pre>
<script>
async function go(){
  const q=document.getElementById('q').value.trim(); if(!q) return;
  const out=document.getElementById('out'); out.textContent='思考中…';
  const r=await fetch('/ask/stream',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({question:q,top_k:3})});
  const rd=r.body.getReader(), dec=new TextDecoder(); let buf='', ans='', cites=[];
  while(true){const {value,done}=await rd.read(); if(done) break;
    buf+=dec.decode(value,{stream:true});
    const parts=buf.split('\\n\\n'); buf=parts.pop();
    for(const p of parts){
      const ev=(p.match(/event: (\\w+)/)||[])[1];
      const dt=(p.match(/data: (.*)/)||[])[1]; if(!dt) continue;
      if(ev==='hits'){cites=JSON.parse(dt);}
      else if(ev==='token'){ans+=JSON.parse(dt); out.textContent=ans;}
      else if(ev==='error'){out.textContent='出错：'+JSON.parse(dt);}
    }}
  if(cites && cites.length){out.textContent += '\\n\\n---\\n命中：' +
    cites.map(c=>'['+c.rank+'] '+(c.heading||'')+' ('+c.score+')').join('\\n');}
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')go()});
</script>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return DEMO
