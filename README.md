# rag_agent：带引用与评估的 RAG Agent

一个可以讲清楚、也经得起追问的 RAG 项目：**切块 → 向量化 → 检索 → 强制引用 → 评估**，外加 token 预算和长期记忆。

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
标题本身就是语义概括，按结构切能保证一块讲一件事；只有超长章节才退化成按句子切。块大小 500 字、重叠 80 字，重叠率 16%，防止答案被切在边界上。

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
| `GET /health` | 后端、维度、块数、当前阈值 |
| `POST /ask` | `{"question": "...", "top_k": 3}` → 回答 + 引用 + 命中列表 |
| `POST /ask/stream` | 同上，SSE：先发 `event: hits`，再逐字 `event: token`，最后 `event: done` |

```bash
curl -s localhost:8000/health
curl -s -X POST localhost:8000/ask -H 'Content-Type: application/json' \
     -d '{"question":"为什么要留重叠","top_k":3}'
```

### Docker

```bash
docker build -t rag-agent .
docker run -p 8000:8000 -e DEEPSEEK_API_KEY=sk-xxx rag-agent
```

镜像里会在构建期把索引建好（`data/index`），容器起来直接能答；torch 走 CPU 源，不含 CUDA。
