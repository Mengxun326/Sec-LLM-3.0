# Sec-LLM-Local 安全大语言模型平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.128.0-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/github/stars/yusichen396/sec-llm-local?style=social" alt="GitHub stars">
</p>

<p align="center">
  <b>第一作者：雨思晨</b> | 开发团队：灵犀网卫
</p>

<p align="center">
  <a href="https://github.com/yusichen396/sec-llm-local">GitHub 仓库</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-功能特性">功能特性</a>
</p>

一个面向网络安全场景的本地/云端 LLM 平台，集成 RAG 知识库、日志分析、流式对话与仪表盘统计，支持本地 Ollama 与 DeepSeek 云端模型切换。

> 🔐 **Sec-LLM** - 由灵犀网卫开发的网络安全专用大模型

---

## ✨ 功能特性

- 🤖 **安全领域专用**：严格限制非安全话题，中文优先回答
- 🔁 **引擎实时切换**：网页一键切换本地 Ollama / 云端 DeepSeek（用户级独立选择）
- 📚 **知识库学习**：PDF/TXT 上传入库，检索增强问答
- 🔍 **智能日志分析**：威胁等级、攻击类型、源 IP 自动提取
- 📊 **真实仪表盘**：基于 MySQL 统计日志与风险指标
- 🧪 **流式对话**：后端流式输出，前端打字机效果
- 🔐 **用户认证**：JWT 认证 + bcrypt 密码加密 + 邮箱验证激活
- 👤 **用户数据隔离**：日志记录、知识库文件、统计数据按用户隔离
- 🧹 **临时文件清理**：`temp/` 目录定期清理（默认 24h）

---

## 🆕 本次升级重点

- **引擎切换现代化**：无需改 `.env` / 重启后端，支持前端 Toggle 实时切换
- **用户级引擎偏好**：每个用户独立保存 `llm_provider`，互不影响
- **聊天与日志分析统一引擎**：`/api/chat` 与日志分析接口都按当前用户引擎执行
- **DeepSeek 云端流式接入**：兼容 OpenAI Chat Completions 流式协议
- **反提示注入增强**：聊天提示词新增 `ANTI-JAILBREAK (CRITICAL)` 规则
- **邮箱验证闭环**：注册发验证邮件、链接激活、登录拦截未激活账号、支持重发验证
- **前端组件抽象**：`LLMProviderToggle` 共用组件统一接入首页/聊天/日志分析

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
git clone https://github.com/yusichen396/sec-llm-local.git
cd sec-llm-local
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
- `DATABASE_TYPE=mysql`
- `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DB`
- `MAIL_USERNAME` / `MAIL_PASSWORD` / `MAIL_FROM` / `MAIL_PORT` / `MAIL_SERVER`
- `MAIL_FROM_NAME` / `DOMAIN_URL`

> 注意：`DEEPSEEK_API_KEY` 必须为真实可用密钥；否则云端对话会返回 401/400。

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
│   ├── app/         # 页面组件
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
