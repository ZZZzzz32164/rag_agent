FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_ENDPOINT=https://hf-mirror.com \
    RAG_INDEX_DIR=/app/data/index

WORKDIR /app

COPY requirements.txt .
# torch 走 CPU 源，避免镜像里塞进 CUDA
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt fastapi "uvicorn[standard]"

COPY . .

# 构建期把索引建好（镜像里自带向量，启动就不用等）
RUN python -m src.index build --backend auto || echo "skip build (offline)"

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health').status==200 else 1)"

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
