# Sec-LLM-Local 安全大语言模型平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.128.0-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/github/stars/yusichen396/Sec-LLM-3.0?style=social" alt="GitHub stars">
</p>

<p align="center">
  <b>第一作者：雨思晨</b> | 开发团队：灵犀网卫
</p>

<p align="center">
  <a href="https://github.com/yusichen396/Sec-LLM-3.0">GitHub 仓库</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-功能特性">功能特性</a>
</p>

一个面向网络安全场景的本地/云端 LLM 平台，集成 RAG 知识库、日志分析、威胁情报联网富化、流式对话与仪表盘统计，支持本地 Ollama 与 DeepSeek 云端模型切换。

> 🔐 **Sec-LLM** - 由灵犀网卫开发的网络安全专用大模型

---

## ✨ 功能特性

- 🤖 **安全领域专用**：严格限制非安全话题，中文优先回答
- 🔁 **引擎实时切换**：网页一键切换本地 Ollama / 云端 DeepSeek（用户级独立选择）
- 📚 **知识库学习**：PDF/TXT 上传入库，检索增强问答
- 🔍 **智能日志分析**：威胁等级、攻击类型、源 IP 自动提取
- 🛰️ **威胁情报自动化研判**：IOC 自动识别（IP/域名/MD5/SHA256）+ 多源情报富化 + AI 研判报告
- 🧰 **安全工具箱（独立页面化）**：钓鱼邮件鉴定、源码审计、蓝队规则生成、扫描报告解析
- 📊 **真实仪表盘**：基于 MySQL 统计日志与风险指标
- 🧪 **流式对话**：后端流式输出，前端打字机效果
- 🔐 **用户认证**：JWT 认证 + bcrypt 密码加密 + 邮箱验证激活
- 👤 **用户数据隔离**：日志记录、知识库文件、统计数据按用户隔离
- 🧹 **临时文件清理**：`temp/` 目录定期清理（默认 24h）

---

## 🆕 V3.0 升级重点

- **威胁情报独立主模块**：从工具箱拆分为一级导航，避免功能遮挡与入口冲突
- **IOC 自动精准嗅探**：后端自动识别 IPv4 / Domain / MD5 / SHA256，并按类型路由情报源
- **并发容错富化**：`asyncio.gather + wait_for + return_exceptions=True`，单源失败不影响整体
- **双段式响应体验**：先返回结构化情报结果，再流式生成中文研判报告
- **报告生成增强**：威胁情报研判结果可自动并入报告，与日志分析/AI 对话一起导出
- **安全工具箱页面化**：四个工具分别独立页面，维护与扩展更清晰

---

## 🛠 技术栈

**后端**: Python 3.10+ | FastAPI | PyMySQL | LangChain | Chroma | Ollama | DeepSeek API  
**前端**: Next.js 14 | React 18 | TypeScript | Tailwind CSS

---

## 📦 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.x
- Ollama（本地模型：`llama3:8b` + `nomic-embed-text`）
- DeepSeek API Key（可选，启用云端时需要）

### 安装 Ollama 模型

```bash
ollama pull llama3:8b
ollama pull nomic-embed-text
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yusichen396/Sec-LLM-3.0.git
cd Sec-LLM-3.0
```

### 2. 后端设置

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端设置

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问应用

浏览器访问 `http://localhost:3000`  
默认管理员账户：`admin` / `admin123`

---

## ⚙️ 配置说明（backend/.env）

关键字段：

- `LLM_PROVIDER=local|cloud`（默认值，仅首次/兜底；运行时可前端切换）
- `OLLAMA_BASE_URL` / `OLLAMA_MODEL_NAME`
- `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL_NAME`
- `ABUSEIPDB_API_KEY`（威胁情报源，可选）
- `OTX_API_KEY`（AlienVault OTX，可选）
- `THREAT_INTEL_TIMEOUT_SECONDS`（威胁情报源超时秒数，默认 4.0）
- `DATABASE_TYPE=mysql`
- `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DB`
- `MAIL_USERNAME` / `MAIL_PASSWORD` / `MAIL_FROM` / `MAIL_PORT` / `MAIL_SERVER`
- `MAIL_FROM_NAME` / `DOMAIN_URL`
- `SEC_LLM_SKILL_API_KEY`（可选，用于 [OpenClaw Skill](#openclaw-skill-集成) 等外部调用）

> 注意：`DEEPSEEK_API_KEY` 必须为真实可用密钥；否则云端对话会返回 401/400。

### OpenClaw Skill 集成

在 Telegram、Discord 等渠道通过 [OpenClaw](https://github.com/openclaw/openclaw) 调用 Sec-LLM 能力（威胁情报、RAG、钓鱼鉴定等）：

1. 在 `backend/.env` 中设置 `SEC_LLM_SKILL_API_KEY`
2. 将 `openclaw-skill/sec-llm` 复制到 OpenClaw 的 Skills 目录
3. 配置 `SEC_LLM_BASE_URL` 与 `SEC_LLM_SKILL_API_KEY` 环境变量

详见 [openclaw-skill/README.md](openclaw-skill/README.md)。

---

## ✅ 数据库连接验证

### 方式一：看启动日志

后端启动时会打印类似：
```
[DB] Using MySQL Database: host:port/db
```
若连接失败会直接抛出异常。

### 方式二：接口验证

访问 `http://localhost:8000/api/dashboard/stats`，如果返回非全 0 的统计数据，说明数据库连接正常且可查询。

### 方式三：命令行快速测试

在 `backend` 目录执行：
```powershell
.\venv\Scripts\python.exe -c "import os;from dotenv import load_dotenv;import pymysql;load_dotenv(r'H:\sec-llm-local\backend\.env');conn=pymysql.connect(host=os.getenv('MYSQL_HOST'),user=os.getenv('MYSQL_USER'),password=os.getenv('MYSQL_PASSWORD'),port=int(os.getenv('MYSQL_PORT')),database=os.getenv('MYSQL_DB'));cur=conn.cursor();cur.execute('SELECT 1');print(cur.fetchone());conn.close()"
```

---

## 📡 API 文档

启动后端后访问：`http://localhost:8000/docs`

### 主要接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/register` | 用户注册（发送验证邮件） |
| GET | `/api/verify` | 邮箱验证激活 |
| POST | `/api/resend-verification` | 重发验证邮件 |
| POST | `/api/login` | 用户登录 |
| GET | `/api/me` | 获取当前用户 |
| GET | `/api/llm/provider` | 获取当前用户引擎偏好 |
| PUT | `/api/llm/provider` | 更新当前用户引擎偏好 |
| GET | `/api/dashboard/stats` | 仪表盘统计 |
| POST | `/api/upload` | 文件上传（RAG/日志分析） |
| POST | `/api/chat` | 流式 AI 对话 |
| POST | `/api/security-tools/phishing-analyzer` | 钓鱼邮件智能鉴定 |
| POST | `/api/security-tools/code-audit` | 源码漏洞审计 |
| POST | `/api/security-tools/rule-generator` | 蓝队规则流式生成 |
| POST | `/api/security-tools/report-explainer` | 扫描报告解析 |
| POST | `/api/security-tools/threat-intel/enrich` | IOC 情报富化（结构化） |
| POST | `/api/security-tools/threat-intel/report` | 威胁情报 AI 研判报告（流式） |
| GET | `/api/log-records` | 获取日志审计记录（当前用户） |
| PUT | `/api/log-records/{id}/status` | 更新日志状态（当前用户） |
| DELETE | `/api/log-records/{id}` | 删除日志记录（当前用户） |
| GET | `/api/chat-histories` | 获取对话历史（当前用户） |
| POST | `/api/chat-histories` | 新建对话历史 |
| PUT | `/api/chat-histories/{id}` | 更新对话历史 |
| DELETE | `/api/chat-histories/{id}` | 删除对话历史 |
| GET | `/api/knowledge/files` | 获取知识库文件列表（当前用户） |
| DELETE | `/api/knowledge/files/{id}` | 删除知识库文件（当前用户） |

---

## 📝 项目结构

```
sec-llm-local/
├── backend/          # FastAPI 后端
│   ├── main.py      # 主程序
│   └── requirements.txt
├── frontend/         # Next.js 前端
│   ├── app/
│   │   ├── security-tools/      # 安全工具箱（4个独立页面）
│   │   ├── threat-intel-agent/  # 威胁情报自动化研判（独立一级功能）
│   │   └── report-generation/   # 报告导出（聚合日志/对话/情报）
│   └── lib/         # API 客户端
└── README.md
```

---

## ⚠️ 安全提示

- 生产环境请修改 `JWT_SECRET_KEY` 与默认管理员密码
- 不要将 API Key 提交到代码仓库
- 建议使用专用 MySQL 账号并限制权限

---

## 👨‍💻 作者信息

| 角色 | 姓名 | 说明 |
|------|------|------|
| **第一作者** | 雨思晨 | 项目负责人、核心开发 |
| **开发团队** | 灵犀网卫 | 网络安全技术团队 |

---

<p align="center">
  <b>Sec-LLM-Local</b> - 网络安全专用大语言模型平台<br>
  第一作者：<b>雨思晨</b> | 开发团队：<b>灵犀网卫</b>
</p>
