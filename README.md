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

一个基于本地 LLM（Ollama）和云端 API（DeepSeek）的**网络安全专用**智能分析平台。集成了 RAG（检索增强生成）技术，提供日志分析、AI 对话、威胁检测和安全报告生成等功能。

> 🔐 **Sec-LLM** - 由灵犀网卫开发的网络安全专门用途大模型

---

## ✨ 功能特性

- 🤖 **专业安全 AI**：严格限定网络安全领域，拒绝回答非安全话题
- 📚 **知识库学习**：上传 PDF/TXT 文档，AI 自动学习并用于问答
- 🔍 **智能日志分析**：自动识别威胁类型、提取 Payload、分析攻击源
- 📊 **实时仪表盘**：动态数据展示、威胁状态监控、系统健康检查
- 📄 **报告生成**：一键导出 PDF/Markdown 安全审计报告
- 🔐 **用户认证**：JWT 令牌认证 + SQLite 数据库 + bcrypt 密码加密

---

## 🛠 技术栈

**后端**: Python 3.10+ | FastAPI | SQLAlchemy | LangChain | ChromaDB | Ollama | DeepSeek API

**前端**: Next.js 14 | React 18 | TypeScript | Tailwind CSS | Recharts

---

## 📦 环境要求

- Python 3.10+
- Node.js 18+
- Ollama（需安装 `deepseek-r1:1.5b` 和 `nomic-embed-text` 模型）
- DeepSeek API Key

### 安装 Ollama 模型

```bash
ollama pull deepseek-r1:1.5b
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

# 配置 DeepSeek API Key（编辑 main.py）
# API_KEY = "your-deepseek-api-key-here"

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端设置

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问应用

打开浏览器访问 `http://localhost:3000`

默认管理员账户：`admin` / `admin123`

---

## 📡 API 文档

启动后端后访问：`http://localhost:8000/docs`

### 主要接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |
| GET | `/api/me` | 获取当前用户信息 |
| GET | `/api/dashboard/stats` | 仪表盘统计数据 |
| POST | `/api/upload` | 文件上传（RAG/日志分析） |
| POST | `/api/chat` | AI 对话 |

---

## ❓ 常见问题

### Ollama 连接失败

```bash
# 检查 Ollama 服务状态
ollama list

# 启动 Ollama 服务
ollama serve
```

### 端口被占用

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F
```

### DeepSeek API 调用失败

- 检查 API Key 是否正确
- 确认 API 余额充足
- 检查网络连接

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

- 生产环境请修改 JWT SECRET_KEY 和默认管理员密码
- 不要将 API Key 提交到代码仓库
- 使用环境变量管理敏感配置

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
