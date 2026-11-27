![docker](https://github.com/ZZZzzz32164/rag_agent/actions/workflows/docker.yml/badge.svg)

# rag_agent：带引用与评估的 RAG Agent

一个可以讲清楚、也经得起追问的 RAG 项目：**切块 → 向量化 → 检索 → 强制引用 → 评估**，外加 token 预算和长期记忆。

## 证据索引（Evidence Index）

> 简历上每个数字都能在这里落地：一张图、一张表、三行命令。

**架构**

```
        ┌──────────── 一次问答 ────────────┐
 问句 → │ BM25 召回 ┐                      │
        │ 向量召回 ┴→ RRF 融合 → cross-encoder 精排 → DeepSeek 生成
        │                                   │ → [n] 引用校验 → 库外拒答
        └───────────────────────────────────┘
  服务层 FastAPI：/ask · /ask/stream(SSE) · /retrieve · /health · /metrics · /logs
  稳定性：令牌桶限流(429) · 超时与重试 · 统一错误码(422/429/503) · X-Request-ID
  数据层：SQLite qa_log（每问一行）+ 进程内 LRU 缓存（key=问题+top_k+mode）
  交付：非 root 镜像 + 构建期建索引 + 启动断言 + HEALTHCHECK + GitHub Actions
```

**指标（可复现，均来自仓库内脚本）**

| 指标 | 数值 | 复现命令 / 证据文件 |
|---|---|---|
| 语料规模 | 78 篇 / 约 38 万字 / 1728 块 | `python -m src.index build` 输出 · `data/index_docs/meta.json` |
| 检索 Hit@3 | 纯向量 50% · 纯 BM25 42% · RRF 56% · 加精排 78%（MRR 0.764） | `python -m eval.run_eval --k 3` · `eval/results/retrieval.json` |
| 端到端引用合法率 | 44% → 75%（加精排后） | `python -m eval.run_agent_eval` · `eval/results/end_to_end*.json` |
| 库外拒答 | 6/6 正确（余弦阈值 0.55） | `eval/qa_out_of_scope.jsonl` |
| 并发 | 20 并发 × 50 次 /health：540–630 QPS，p50 29ms，p95 46ms | `python bench.py --mode health --c 20 --n 50` |
| 缓存 | 同题 987ms → 13–16ms（命中率 50%） | `GET /metrics` · `GET /logs` |
| 容器 | 2.36GB 镜像，容器内 `/health` = bge / 512 / 1728 | GitHub Actions `docker.yml` 运行记录 |

**三行复现**

```bash
docker build -t rag-agent . && docker run -p 8000:8000 rag-agent
curl -s localhost:8000/health
python bench.py --mode health --base http://127.0.0.1:8000 --c 20 --n 50
```

**失败案例（面试常问）**

- 容器内向量后端曾**静默降级成 LSA（256 维）而服务仍返 200** → 加启动断言，让「看起来正常」的故障变成启动失败。
- 缓存最初只缓存非拒答样本，复放命中率仅 25% → 改成拒答也缓存（答案确定性），命中率升到 50%。
- 试过用 LLM 判相关性替代 cross-encoder，单条 3–13s 且结果不稳，放弃并保留精排离线评估。


## 目录

```
rag_agent/
├─ api.py            FastAPI 服务层：/health、/ask、/ask/stream（SSE）、HTML 演示页
├─ Dockerfile        自带索引构建与 healthcheck 的镜像
├─ src/
│  ├─ chunking.py    按 Markdown 标题切块，过长再按句子切，块间重叠
│  ├─ embedder.py    可插拔向量后端：bge（语义）/ lsa（TF-IDF+SVD）/ hash（零依赖）
│  ├─ index.py       建索引、落盘、余弦检索、拼带编号上下文
│  ├─ memory.py      tiktoken 计数、按预算裁剪、摘要压缩、长期记忆
│  ├─ llm.py         DeepSeek 调用（超时、429/5xx 重试、流式）
│  └─ agent.py       检索 + 生成 + 引用校验 + 低分拒答
├─ eval/
│  ├─ qa_set.jsonl   10 条问题与期望命中的关键词
│  ├─ qa_out_of_scope.jsonl  6 条库外问题（测拒答）
│  ├─ run_eval.py    算 Hit@K 和 MRR
│  └─ run_agent_eval.py  端到端：引用合法率 / 拒答率 / 耗时
└─ data/knowledge/   3 篇笔记（Agent 基础 / MCP 与工具 / 工程化）
```

## 快速开始

```bash
cd rag_agent
pip install -r requirements.txt

# 1) 建索引（第一次会下载 bge-small-zh，约 100MB；没有网络会自动退回 lsa）
python -m src.index build --backend auto

# 2) 检索效果看数字
python -m eval.run_eval --k 3

# 3) 只检索不生成（不需要 key）
python -m src.agent "RRF 是怎么融合两路结果的" --no-llm

# 4) 完整问答（需要 .env 里的 DEEPSEEK_API_KEY）
python -m src.agent "为什么切块要留重叠"
```

## 四个设计取舍（面试重点）

**1. 为什么切块先按标题、再按句子**
标题本身就是语义概括，按结构切能保证一块讲一件事；只有超长章节才退化成按句子切。块大小 **350 字、重叠 60 字**（重叠率 17%），防止答案被切在边界上。78 篇文档按这个参数切出 **1728 块**，下文所有指标都是在这套参数上测的（`src/chunking.py` 与 `python -m src.index build` 的默认值就是这套）。

**2. 为什么向量后端做成可插拔**
`bge` 是真实语义向量，效果最好但需要下载模型；`lsa` 用 TF-IDF + SVD 降维，纯 sklearn，零下载；`hash` 只做特征哈希，用来在没有网络时跑通链路。同一个接口三种实现，说明白"效果与工程成本"的权衡。

**3. 为什么要有评估集**
没有 Hit@K 的时候，调 chunk 大小、换 embedding 全靠感觉。10 条问题、每条带一个"必须命中的关键词"，跑一次就知道改得好不好。当前基线见下方数字，其中没命中的那条能直接暴露问题。

**4. 为什么要强制引用 + 低分拒答**
模型很容易在没召回到内容时硬编。所以 prompt 里写死"只依据资料、必须标编号、没有就说没有"，生成后再用正则校验编号是否越界；检索相似度低于阈值时直接拒答，不进模型。

## 语料：真爬的公开文档

```bash
python -m src.crawl --site all --limit 40 --delay 0.8
```

| 站点 | 文件数 | 字符数 | 说明 |
|---|---|---|---|
| DeepSeek API 文档 | 12 | 112,135 | 英文，API 参考页参数列表多 |
| FastAPI 中文文档 | 44 | 183,671 | 中文，结构最规整 |
| MCP 规范 | 22 | 86,820 | 英文，含 1 个超时未重试 |
| **合计** | **78** | **382,626** | 切块后 **1728 块**（UTF-8 体积 517,128 字节；中文字符占 3 字节，故字段数≠字数） |

爬虫做三件事：从 sitemap 发现链接（白名单限定站点）、只取 article/main 正文并去导航页脚、0.8s 间隔。落盘文件头带 `<!-- source: url -->`，检索结果能追溯回原文地址。

## 评估集：合成 + 机器校验

```bash
python -m eval.gen_qa --n 45     # 写入 eval/qa_docs.jsonl
```

- 从 1728 块里按来源站点分层抽块（220–900 字、有标题）
- 让 DeepSeek 出题，同时要求给出「片段中原样出现的 evidence」和 2–3 个关键词
- 机器校验：evidence 必须真在片段里、关键词至少命中一个、字符二元组 Jaccard>0.72 去重
- **45 个候选 → 36 题合格**，落选的 9 条是"evidence 不在原文"或"关键词一个都没命中"

不做校验会怎样：模型会编出片段里根本没有的题，评估集本身就是假的。

## 实测数字（1728 块 / 36 题 / k=3）

> 复现：`python -m eval.run_eval --k 3 --modes vector,keyword,hybrid,hybrid_rerank --out eval/results/retrieval.json`
> 原始结果：`eval/results/retrieval.json`（含四种模式的 Hit@3 / MRR / 拒答统计）

| 检索方式 | Hit@3 | MRR |
|---|---|---|
| 纯向量（bge-small-zh） | 18/36 = 50% | 0.421 |
| 纯 BM25（jieba 分词） | 15/36 = 42% | 0.306 |
| 混合（RRF 融合两路 top-30） | 20/36 = 56% | 0.472 |
| **混合 + cross-encoder 精排** | **28/36 = 78%** | **0.764** |

四个结论：

1. **混合比纯向量多 6 个点，比纯 BM25 多 14 个点。** BM25 单独用很弱（中文分词 + 短查询），但它补的正是向量漏掉的那类命中：参数名、字段名、日期。
2. **精排是最大增量：+22 个点，MRR 从 0.472 到 0.764。** cross-encoder 把 (query, 文档) 拼在一起看，能看到双塔模型看不到的交互。
3. **精排很贵。** CPU 上单查询 13.3s；混合检索 0.11s（首次 2.5s 是建 BM25 索引），纯向量 0.12s。生产上要么上 GPU，要么只对 Top-10 精排。
4. **语料从 19 块扩到 1728 块，Hit@3 从 90% 掉到 50%——这不是退步。** 原来 10 条题、19 块语料，几乎必中；现在 36 条题问的是"stop 参数最多几个序列"这种必须精确定位的细节，指标掉下来才说明评估真的有了意义。

## 已知局限

- 精排 13s/查询，只在离线评估可行，没做 GPU 或缩小 pool 的加速
- 36 题是合成题，集中在"参数/字段/日期"这类事实题，缺少"怎么设计"的开放题
- 拒答阈值 0.55 只在 bge 余弦分上校准过；RRF 分与精排分不能直接比，所以拒答判定单独走向量分
- 记忆只做了"事实落盘 + 读回"，没有遗忘与冲突消解

## 端到端（真调 DeepSeek / 36 条库内 + 6 条库外）

```bash
# 纯向量
python -m eval.run_agent_eval --k 3 --mode vector        --out eval/results/end_to_end.json
# 混合召回 + cross-encoder 精排
python -m eval.run_agent_eval --k 3 --mode hybrid_rerank --out eval/results/end_to_end_rerank.json
```

两份原始结果已在仓库里：`eval/results/end_to_end.json`、`eval/results/end_to_end_rerank.json`。

| 指标 | 纯向量 | 混合 + 精排 |
|---|---|---|
| 库内 36 条：回答带引用 | 16/36 = 44% | **27/36 = 75%** |
| 引用编号全部合法 | 16/36 | 27/36 |
| 库外 6 条：正确拒答 | 6/6 | 6/6 |
| 平均耗时 | **0.64 s/题** | 4.63 s/题（本次复现，CPU）/ 9.05 s/题（机器负载高时） |

**这张表是整个项目最该被记住的地方：精度 +31 个点，延迟 ×7～14（视 CPU 负载）。**
所以工程上的结论不是"上精排"，而是"看清楚你在为什么买单"——
在线服务可以先走向量（0.66s），把精排留给离线批处理或二次确认；
或者只对 Top-10 精排、或换成 GPU。

一个设计细节：**拒答判定走单独的向量分**（余弦 0.55），不跟精排分混用。
RRF 分是 1/(60+rank) 累加出来的小数、精排分是 cross-encoder 的 logit，两者量纲都不同，
拿同一个阈值去比必然出错——这是很多 RAG demo 里最常见的一个坑。

## HTTP 服务（FastAPI）

```bash
pip install -r requirements-api.txt
uvicorn api:app --port 8000
```

| 接口 | 说明 |
|---|---|
| `GET /` | 演示页，输入问题直接看流式回答与命中来源 |
| `GET /health` | 后端、维度、块数、当前阈值、是否配了 LLM key |
| `POST /ask` | `{"question": "...", "top_k": 3}` → 回答 + 引用 + 命中列表（带缓存、带 `rid`；检索在 `anyio.to_thread` 里跑，不堵事件循环） |
| `POST /ask/stream` | 同上，SSE：先发 `event: hits`，再逐字 `event: token`，最后 `event: done` |
| `POST /retrieve` | **只检索不生成**：返回命中片段 + 本次检索耗时，用于排查慢查询、压测不烧额度 |
| `GET /metrics` | 运行指标：QPS、延迟 p50/p90/p95/p99、拒答率、缓存命中率、高频问题 |
| `GET /logs` | 最近 N 条问答日志（同时落盘在 `data/qa_log.db`，可直接用 SQL 查） |

工程细节（这几条不是装饰，是为了"能上线"）：

- **每个请求都带 `X-Request-ID`**，日志里同一 rid 能串起来，客户端报错时可以直接把 id 给我；
- **上游失败返回 503 而不是 500**：`{"error":{"code":"upstream_unavailable","message":"..."}}`，没配 `DEEPSEEK_API_KEY` 时也是这条，不会把堆栈吐给调用方；
- **非法请求返回 422**（FastAPI + Pydantic 自带），`top_k` 限制在 1–10；
- LLM 调用本身已有 **60s 超时 + 3 次重试**（只重试 429/5xx，`src/llm.py`）；
- **令牌桶限流**：默认每 IP 5 rps / 突发 10，超了返回 **429 + `Retry-After` + `X-RateLimit-*`**（`src/ratelimit.py`）；
- **问答缓存**：同题 1 小时内直接返回（`RAG_CACHE_TTL`，默认 3600s），**LRU 淘汰**（`RAG_CACHE_MAX` 默认 500 条）；
- **拒答也缓存**：给定索引 + 阈值 + `temperature=0`，拒答是确定性的。早期版本跳过拒答缓存，实测复放场景命中率只有 **25%**，改成也缓存后升到 **50%**（重复的库外问题不再每次跑满检索 + 一次大模型调用）；
- **每次问答落一行 SQLite**（`data/qa_log.db`：rid / 时间 / 问题 / 耗时 / 是否拒答 / 后端 / 命中数 / 是否命中缓存），单机零依赖，线上换 MySQL 只改 DSN。

### 压测（本机实测，单进程 uvicorn）

`bench.py` 用线程池压，输出 QPS 与延迟分位（`python bench.py --mode health --c 20 --n 50`）：

| 场景 | 并发 | 请求数 | QPS | p50 | p95 | p99 |
|---|---|---|---|---|---|---|
| `GET /health`（只读内存状态） | 20 | 1000 | **540–630** | 29–31ms | 46–75ms | 111–148ms |
| `GET /health` | 50 | 2000 | **592** | 71.3ms | 147.9ms | 206.0ms |

并发 20 → 50 时 QPS 只从 630 掉到 592、p95 从 46ms 涨到 148ms：**`/health` 不碰模型，瓶颈是单进程的 HTTP 栈**；
再往上加并发只是排队。这条结论写在这里，是因为它决定了后面要不要上多 worker / 异步化，而不是"数字好看就行"。

#### worker 数不是越多越好（实测）
同一台 8 核机器、同一份 1728 块索引、`/health` 端点、20 并发 × 50 次：

| workers | QPS | p50 | p95 | p99 |
|---|---|---|---|---|
| 1 | **540–630** | 29–31 ms | 46–75 ms | 111–148 ms |
| 2 | 130.5 | 19.9 ms | 33.5 ms | 55.3 ms（max 7.5 s） |
| 4 | 67.6 | 5.1 ms | 13.4 ms | **8052 ms**（max 14.6 s） |

原因：每个 worker 各自载入一份 bge（约 400 MB）并各自开 torch 线程池，CPU 抢核后 p99 直接塌陷；2/4 worker 的 p50 更低只是因为部分请求落在空闲进程，尾部延迟不可接受。
**结论：镜像里固定 `--workers 1`，靠多副本（多容器/多机）水平扩展。**


| 链路 | 实测 |
|---|---|
| `POST /retrieve`（bge 编码 + 混合召回 + cross-encoder 精排 3 条） | **185–347ms** |
| `POST /ask` 冷启动（真调 DeepSeek，非拒答） | **2019ms** |
| `POST /ask` 命中缓存 | **13–16ms**（首轮 987ms，实测复放 12 题两遍） |

重复提问的收益是可量化的：同一问题第一次约 1.0s（含一次大模型调用），命中缓存后 13–16ms；`/metrics` 里 `cache_hit_rate` 直接反映这件事（复放 12 题两遍 = 50%）。

**限流实测**（`RAG_RATE=2 RAG_BURST=3` 启动，连打 10 次）：

```
status sequence: [200, 200, 200, 200, 429, 429, 429, 429, 429, 429]
429 body: {"error":{"code":"rate_limited","message":"too many requests, retry after 1s"}}  Retry-After: 1
```

**指标实测**（同样这几次请求之后）：

```json
{"requests":9,"errors":0,"latency_ms":{"p50":183.3,"p90":1157.5,"p95":1977.6,"samples":9},
 "refused":4,"refused_rate":0.444,"cache_hits":3,"cache_hit_rate":0.333,
 "top_questions":[{"q":"FastAPI 怎么用依赖注入？","n":4}],
 "paths":{"/health":3002,"/retrieve":3,"/ask":18}}
```

```bash
curl -s localhost:8000/health
curl -s -X POST localhost:8000/ask -H 'Content-Type: application/json' \
     -d '{"question":"为什么要留重叠","top_k":3}'
curl -s localhost:8000/metrics
curl -s 'localhost:8000/logs?n=5'
```

### Docker

```bash
docker build -t rag-agent .                                  # 构建期建索引，失败即 build 失败
```

**CI 实测**（GitHub Actions，run #2 `99a3e81`，12 个步骤全绿）：镜像 `rag-agent:ci` 构建成功，磁盘占用 **2.36GB**（压缩后 546MB）；
容器起来后 `/health` 返回 `{"status":"ok","backend":"bge","dim":512,"chunks":1728,"threshold":0.55}`，`/openapi.json` 的 paths 为 `/`、`/ask`、`/ask/stream`、`/health`。
第一次 CI（run #1）还抓到一个问题：**镜像里 `--backend auto` 悄悄降级成了 LSA（dim=256）**，因为构建环境连不上 hf-mirror 下不了 bge 模型。
现在 Dockerfile 里加了断言——`backend != bge` 或 `chunks != 1728` 直接让 build 失败，不再产出"看起来能用、其实换了模型"的镜像。

docker run -p 8000:8000 -e DEEPSEEK_API_KEY=sk-xxx rag-agent
curl -s localhost:8000/health                                # 容器自带 HEALTHCHECK
```

国内网络构建时把 HuggingFace 源换成镜像（否则 bge 模型下不下来，构建会**故意失败**而不是偷偷降级成 LSA）：

```bash
docker build --build-arg HF_ENDPOINT=https://hf-mirror.com -t rag-agent .
```

镜像设计上的几个决定：

| 决定 | 为什么 |
|---|---|
| `python:3.11-slim` + torch 走 `download.pytorch.org/whl/cpu` | 不把 CUDA 塞进镜像（省 2GB+），本机没有 GPU 也跑得动 |
| 构建期建索引，**不加 `\|\| echo skip`** | 索引是服务的必需品，建不出来就该让 build 失败，而不是产出一个 `/health` 直接 500 的镜像 |
| `--chunk 350 --overlap 60` 写进构建命令 | 镜像里的索引必须和 README 的评估数字同参数（1728 块），否则数字对不上 |
| 非 root 用户 `appuser` 跑服务 | 容器逃逸成本更高，属于部署基线 |
| `HEALTHCHECK` 打 `/health` | 让编排系统（compose / k8s）能判断"活着且索引可用"，而不是只看进程在 |
| `--workers 1` | 镜像里没有 Redis，多 worker 会各自载一份 bge 模型；要横向扩展得先抽出共享缓存 |

### 这台机器没有装 Docker，怎么验证镜像能跑

本机是 Windows 家庭版、无 WSL2、无管理员权限，装不了 Docker Desktop。
所以把 Dockerfile 的每一步在**本地逐步复现**（除 `FROM` 那层），并把输出留档：

| Dockerfile 里的步骤 | 本地怎么验 | 结果 |
|---|---|---|
| `pip install torch --index-url .../cpu` | 干净 venv 装 CPU 版 torch | 通过 |
| `pip install -r requirements*.txt` | 同上 | 通过 |
| `RUN python -m src.index build` | 同一命令、同一参数 | 通过，**1728 块 / bge / 512 维**，202s |
| `CMD uvicorn api:app` | 同一条命令起服务 | 通过 |
| `HEALTHCHECK curl /health` | `GET /health` | `200`，`{"status":"ok","backend":"bge","dim":512,"chunks":1728,...}` |
| 冒烟 `/`、`/openapi.json` | 同上 | `200`，paths = `/`, `/ask`, `/ask/stream`, `/health` |

真正的 `docker build` 由 **GitHub Actions 在云端跑**（`.github/workflows/docker.yml`）：
构建 → 起容器 → 探 `/health` → 校验 `chunks>0` → 上传冒烟产物。
本地这套复现的完整输出在 `docs/docker-local-proof.txt`。

顺带在这次复现里修掉了一个真问题：**检索分刚过阈值、但模型自己答「资料中没有相关内容」时，`refused` 会误报 `false`**。
现在 `/ask` 会把这种情况也算作拒答（`api.py` 里 `refused = r["refused"] or "资料中没有相关内容" in answer`），
证据在同一份 proof 的第 10 节：同一道题修复前 `refused=false`、修复后 `refused=true`。
