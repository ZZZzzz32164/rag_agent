# syntax=docker/dockerfile:1
# CPU 版镜像：不装 CUDA，torch 走官方 CPU 源，体积约 1.2GB
FROM python:3.11-slim

LABEL org.opencontainers.image.title="rag_agent" \
      org.opencontainers.image.description="RAG QA API: bge + BM25/RRF + cross-encoder rerank + citation" \
      org.opencontainers.image.source="https://github.com/ZZZzzz32164/rag_agent"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_ENDPOINT=https://hf-mirror.com \
    RAG_INDEX_DIR=/app/data/index

WORKDIR /app

# curl 供 HEALTHCHECK 用；建一个非 root 用户跑服务
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 10001 appuser

# 依赖层单独缓存：只有 requirements 变了才重装
COPY requirements.txt requirements-api.txt ./
RUN pip install --upgrade pip \
    && pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r requirements.txt -r requirements-api.txt

COPY . .

# 构建期把向量索引建好（镜像自带索引，启动即可用）。
# 切块参数必须和评估时一致（350 字 / 重叠 60 → 1728 块），否则镜像里的索引和 README 数字对不上。
# 这里故意不带兜底：建索引失败就让整个 build 失败，不允许产出一个跑不起来的镜像。
RUN python -m src.index build --backend auto --chunk 350 --overlap 60 --index "$RAG_INDEX_DIR" \
    && python -c "import json,os; \
d=os.environ['RAG_INDEX_DIR']; \
c=json.load(open(os.path.join(d,'chunks.json'),encoding='utf-8')); \
m=json.load(open(os.path.join(d,'meta.json'),encoding='utf-8')); \
print('index ok: chunks=%d backend=%s dim=%s' % (len(c), m.get('backend'), m.get('dim')))"

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/health || exit 1

# 单 worker：镜像里没有 Redis，多 worker 会各自载一份模型；要横向扩展请挂外部缓存
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
