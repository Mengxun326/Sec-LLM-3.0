# Sec-LLM-Local 安全大语言模型平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.128.0-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<p align="center">
  <b>第一作者：陈思宇</b> | 开发团队：灵犀网卫
</p>

一个基于本地 LLM（Ollama）和云端 API（DeepSeek）的**网络安全专用**智能分析平台。集成了 RAG（检索增强生成）技术，提供日志分析、AI 对话、威胁检测和安全报告生成等功能。

> 🔐 **Sec-LLM** - 由灵犀网卫开发的网络安全专门用途大模型

---

## 📋 目录

- [项目简介](#-项目简介)
- [功能特性](#-功能特性)
- [技术架构](#-技术架构)
- [项目结构](#-项目结构)
- [环境要求](#-环境要求)
- [快速开始](#-快速开始)
- [功能说明](#-功能说明)
- [API 文档](#-api-文档)
- [配置说明](#-配置说明)
- [常见问题](#-常见问题)
- [开发指南](#-开发指南)
- [更新日志](#-更新日志)
- [作者信息](#-作者信息)

---

## 🎯 项目简介

**Sec-LLM-Local** 是一个全栈网络安全分析平台，专为网络安全领域设计，结合了：

| 组件 | 说明 |
|------|------|
| **本地 LLM (Ollama)** | 基于 deepseek-r1:1.5b 模型，用于 AI 安全问答和 RAG 检索 |
| **DeepSeek API** | 云端大模型 API，用于日志深度分析和威胁检测 |
| **RAG 技术** | 基于 ChromaDB 向量数据库 + LangChain，支持知识库增强检索 |
| **现代化前端** | Next.js 14 + React 18 + TypeScript，现代化 UI |
| **安全认证** | JWT 令牌认证 + SQLite 用户数据库 + bcrypt 密码加密 |

### 核心亮点

- 🤖 **专业安全 AI**：严格限定网络安全领域，拒绝回答非安全话题
- 📚 **知识库学习**：上传 PDF/TXT 文档，AI 自动学习并用于问答
- 🔍 **智能日志分析**：自动识别威胁类型、提取 Payload、分析攻击源
- 📊 **实时仪表盘**：动态数据展示、威胁状态监控、系统健康检查
- 📄 **报告生成**：一键导出 PDF/Markdown 安全审计报告

---

## ✨ 功能特性

### 🔐 用户认证系统
- JWT 令牌认证，24 小时有效期
- SQLite 数据库存储用户信息
- bcrypt 密码加密
- 用户注册/登录功能
- 用户信息卡片（点击头像显示详情）
- 默认管理员账户：`admin` / `admin123`

### 🤖 AI 智能对话
- 基于 RAG 的知识库检索问答
- 网络安全专用回答模式
- 严格的话题过滤（仅回答安全相关问题）
- 固定自我介绍响应
- 详尽的安全知识解答（8 个维度）
- 聊天记录自动保存

### 📊 智能日志分析
- 支持 .log / .txt / .csv 等格式
- DeepSeek API 深度分析
- 威胁等级评估（Low/Medium/High/Critical）
- Payload 提取与高亮显示
- 修复建议生成

### 📈 安全仪表盘
- 实时威胁统计
- 系统状态监控（CPU/内存/存储）
- 动画加载效果
- 数据随机波动（模拟真实场景）
- 快捷功能入口

### 📄 报告生成
- 整合日志分析 + AI 对话记录
- A4 纸比例预览
- PDF 导出（html2canvas + jspdf）
- Markdown 导出
- 专业安全审计报告格式

### 🗂️ 文件管理
- 知识库文件永久保存（uploads/）
- 临时文件自动清理（24 小时）
- 管理员接口查看/清理临时文件

---

## 🛠 技术架构

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 运行环境 |
| FastAPI | 0.128.0 | Web 框架 |
| Uvicorn | - | ASGI 服务器 |
| SQLAlchemy | - | ORM 数据库操作 |
| SQLite | - | 用户数据存储 |
| Passlib | - | 密码加密 (bcrypt) |
| python-jose | - | JWT 令牌生成/验证 |
| LangChain | - | RAG 框架 |
| ChromaDB | - | 向量数据库 |
| Ollama | - | 本地 LLM 服务 |
| OpenAI SDK | - | DeepSeek API 调用 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 14 | React 框架 (App Router) |
| React | 18 | UI 库 |
| TypeScript | 5.0 | 类型安全 |
| Tailwind CSS | 3.4 | 样式框架 |
| Lucide React | - | 图标库 |
| Recharts | - | 数据可视化 |
| Axios | - | HTTP 客户端 |
| html2canvas | - | 截图工具 |
| jspdf | - | PDF 生成 |

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐│
│  │  Login   │ │Dashboard │ │   Chat   │ │ Log Analysis/Report ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘│
│                              │                                   │
│                    Axios (HTTP Client)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │ REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                     Backend (FastAPI)                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │ Auth Module │ │ RAG Module  │ │ Analysis    │                │
│  │ (JWT/SQLite)│ │ (LangChain) │ │ (DeepSeek)  │                │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘                │
│         │               │               │                        │
│    ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐                 │
│    │ SQLite  │    │ ChromaDB  │   │ DeepSeek  │                 │
│    │(users.db)│   │(chroma_db)│   │   API     │                 │
│    └─────────┘    └─────┬─────┘   └───────────┘                 │
│                         │                                        │
│                   ┌─────▼─────┐                                  │
│                   │  Ollama   │                                  │
│                   │(Local LLM)│                                  │
│                   └───────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
Sec-LLM-Local/
├── backend/                        # 后端服务
│   ├── main.py                    # FastAPI 主程序（约 800 行）
│   ├── requirements.txt           # Python 依赖
│   ├── venv/                      # Python 虚拟环境
│   ├── data/                      # 数据目录
│   │   ├── users.db              # SQLite 用户数据库
│   │   └── chroma_db/            # ChromaDB 向量数据库
│   ├── uploads/                   # 永久文件存储
│   └── temp/                      # 临时文件（24小时自动清理）
│
├── frontend/                       # 前端应用
│   ├── app/                       # Next.js App Router
│   │   ├── page.tsx              # 仪表盘首页
│   │   ├── login/page.tsx        # 登录页面
│   │   ├── register/page.tsx     # 注册页面
│   │   ├── chat/page.tsx         # AI 对话页面
│   │   ├── log-analysis/page.tsx # 日志分析页面
│   │   ├── report-generation/    # 报告生成页面
│   │   ├── layout.tsx            # 全局布局
│   │   └── globals.css           # 全局样式
│   ├── lib/
│   │   └── api.ts                # API 客户端封装
│   ├── public/
│   │   └── login-bg.jpg          # 登录页背景图
│   ├── package.json              # Node.js 依赖
│   ├── tailwind.config.js        # Tailwind 配置
│   └── tsconfig.json             # TypeScript 配置
│
└── README.md                       # 项目文档
```

---

## 📦 环境要求

### 必需软件

| 软件 | 版本要求 | 下载地址 |
|------|----------|----------|
| Python | 3.10+ | https://python.org |
| Node.js | 18+ | https://nodejs.org |
| Ollama | 最新版 | https://ollama.ai |

### Ollama 模型安装

```bash
# 安装对话模型（必需）
ollama pull deepseek-r1:1.5b

# 安装嵌入模型（必需，用于 RAG）
ollama pull nomic-embed-text

# 验证安装
ollama list
```

### DeepSeek API

- 注册地址：https://platform.deepseek.com
- 获取 API Key 后配置到后端

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd sec-llm-local
```

### 2. 启动 Ollama 服务

```bash
# 确保 Ollama 正在运行
ollama serve

# 验证模型已安装
ollama list
# 应显示: deepseek-r1:1.5b, nomic-embed-text
```

### 3. 后端设置

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境 (Windows)
python -m venv venv
.\venv\Scripts\activate

# 创建并激活虚拟环境 (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置 DeepSeek API Key（编辑 main.py 第 207 行）
# API_KEY = "your-deepseek-api-key-here"

# 启动后端服务
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务运行在：`http://localhost:8000`

### 4. 前端设置

```bash
# 新开终端窗口，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用运行在：`http://localhost:3000`

### 5. 访问应用

1. 打开浏览器访问 `http://localhost:3000`
2. 使用默认管理员账户登录：
   - **用户名**: `admin`
   - **密码**: `admin123`
3. 或注册新账户

---

## 🎨 功能说明

### 1. 登录/注册页面

**登录页面** (`/login`)
- 用户名/密码登录
- JWT 令牌认证
- 记住登录状态

**注册页面** (`/register`)
- 新用户注册
- 密码强度验证
- 邮箱（可选）
- 注册后自动登录

### 2. 安全仪表盘 (`/`)

**功能特性**:
- 安全概览统计卡片
  - 威胁总数（从日志分析获取）
  - 网络流量
  - 活跃端点
  - 安全评分
- 威胁流量趋势图（Recharts AreaChart）
- 系统状态监控
  - CPU 使用率（动画加载）
  - 内存占用（动画加载）
  - 存储空间（动画加载）
  - 数值每次刷新随机波动 ±10%
- 用户信息卡片（点击头像显示）
  - 用户名/全名
  - 角色（管理员/普通用户）
  - 邮箱
  - 在线状态
  - 退出登录按钮

### 3. AI 智能对话 (`/chat`)

**功能特性**:
- 基于 RAG 的知识库问答
- 网络安全专用模式
- 代码高亮显示
- 参考来源显示
- 聊天记录持久化

**AI 行为规则**:
1. **自我介绍**：当问"你是谁"时，固定回复：
   > "你好！我是Sec-LLM，是由灵犀网卫开发的网络安全专门用途大模型，很高兴为您服务！"

2. **话题限制**：仅回答网络安全相关问题，拒绝其他话题

3. **详细回答**：安全问题从 8 个维度回答：
   - 概念定义
   - 核心原理
   - 攻击分类
   - 实战案例
   - 代码示例
   - 检测方法
   - 防御方案
   - 工具推荐

**知识库上传**:
- 点击 📎 图标上传 PDF/TXT 文件
- 文件自动处理并存入向量数据库
- 同时永久保存到 `uploads/` 目录

### 4. 日志分析 (`/log-analysis`)

**功能特性**:
- 拖拽上传或点击选择
- 支持 .log / .txt / .csv 格式
- DeepSeek API 深度分析
- 威胁等级评估
- Payload 代码高亮
- 修复建议

**分析结果**:
```json
{
  "summary": "分析摘要",
  "threat_level": "High",
  "details": [
    {
      "type": "SQL Injection",
      "payload": "' OR '1'='1",
      "source_ip": "192.168.1.100"
    }
  ],
  "advice": "修复建议..."
}
```

### 5. 报告生成 (`/report-generation`)

**功能特性**:
- 整合日志分析 + AI 对话
- A4 纸比例预览
- 导出 PDF
- 导出 Markdown

**报告内容**:
- 威胁审计结论
- 威胁等级徽章
- 详细分析
- AI 问答记录

---

## 📡 API 文档

启动后端后访问：`http://localhost:8000/docs`

### 认证接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |
| GET | `/api/me` | 获取当前用户信息 |

### 业务接口

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/dashboard/stats` | 仪表盘统计数据 |
| POST | `/api/upload` | 文件上传（RAG/日志分析） |
| POST | `/api/chat` | AI 对话 |

### 管理接口

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/admin/temp-status` | 查看临时文件状态 |
| POST | `/api/admin/cleanup-temp` | 手动清理临时文件 |

### 请求示例

**用户注册**
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "password123",
    "email": "user@example.com",
    "full_name": "张三"
  }'
```

**用户登录**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**AI 对话**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是SQL注入？"
  }'
```

---

## ⚙️ 配置说明

### 后端配置 (`backend/main.py`)

#### JWT 配置
```python
SECRET_KEY = "your-super-secret-key"  # 生产环境请修改
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 小时
```

#### DeepSeek API 配置
```python
API_KEY = "sk-your-api-key"  # 替换为你的 API Key
BASE_URL = "https://api.deepseek.com"
```

#### 临时文件清理配置
```python
TEMP_FILE_MAX_AGE_HOURS = 24  # 文件保留时间（小时）
CLEANUP_INTERVAL_HOURS = 1    # 清理检查间隔（小时）
```

#### Ollama 配置
```python
# 嵌入模型
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://127.0.0.1:11434"
)

# 对话模型
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:1.5b"
```

### 前端配置

#### API 地址
创建 `frontend/.env.local`：
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## ❓ 常见问题

### 1. Ollama 连接失败

**问题**: `无法连接本地 AI`

**解决方案**:
```bash
# 检查 Ollama 服务状态
ollama list

# 启动 Ollama 服务
ollama serve

# 确认模型已安装
ollama pull deepseek-r1:1.5b
ollama pull nomic-embed-text
```

### 2. 端口被占用

**问题**: `[Errno 10048] 端口已被使用`

**解决方案**:
```bash
# Windows - 查找并结束占用端口的进程
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# 或更改启动端口
python -m uvicorn main:app --port 8001
```

### 3. bcrypt 版本兼容问题

**问题**: `AttributeError: module 'bcrypt' has no attribute '__about__'`

**解决方案**:
```bash
pip install bcrypt==4.0.1
```

### 4. DeepSeek API 调用失败

**问题**: `AI 分析服务暂时不可用`

**解决方案**:
- 检查 API Key 是否正确
- 确认 API 余额充足
- 检查网络连接

### 5. 前端无法连接后端

**问题**: `Network Error` 或 `CORS Error`

**解决方案**:
- 确认后端服务正在运行
- 检查后端 CORS 配置
- 确认 API 地址正确

---

## 🛠 开发指南

### 添加新 API 端点

```python
# backend/main.py
@app.post("/api/your-endpoint")
def your_function(data: YourModel):
    # 业务逻辑
    return {"status": "success", "data": result}
```

### 添加新页面

```bash
# 创建页面目录
mkdir frontend/app/your-page

# 创建页面文件
touch frontend/app/your-page/page.tsx
```

### 添加新 API 调用

```typescript
// frontend/lib/api.ts
export const yourApiCall = async (data: YourType): Promise<ResponseType> => {
  const response = await api.post<ResponseType>('/api/your-endpoint', data);
  return response.data;
};
```

### 数据持久化

**前端 (localStorage)**:
- `token` - JWT 令牌
- `user` - 用户信息
- `cyberguard_chat_history` - 聊天记录
- `cyberguard_log_analysis` - 日志分析结果

**后端**:
- `data/users.db` - 用户数据 (SQLite)
- `data/chroma_db/` - 向量数据库 (ChromaDB)
- `uploads/` - 永久文件存储
- `temp/` - 临时文件 (24h 自动清理)

---

## 📝 更新日志

### v3.1 (当前版本)
- ✅ 真实用户认证系统 (JWT + SQLite + bcrypt)
- ✅ 用户注册功能
- ✅ 用户信息卡片（点击头像显示）
- ✅ 仪表盘系统状态动画加载
- ✅ 数值随机波动（模拟真实数据）
- ✅ AI 严格话题限制（仅网络安全）
- ✅ AI 固定自我介绍
- ✅ AI 详尽回答模式（8 维度）
- ✅ 临时文件自动清理（24 小时）
- ✅ 文件双重保存（uploads + temp）
- ✅ 管理员临时文件接口

### v3.0
- ✅ 集成 DeepSeek API 进行日志分析
- ✅ 实现 RAG 检索增强生成
- ✅ 添加报告生成功能（PDF/Markdown）
- ✅ 优化仪表盘 UI

### v2.0
- ✅ 集成 Ollama 本地 LLM
- ✅ 实现基础 AI 对话功能

### v1.0
- ✅ 初始版本
- ✅ 用户登录和基础 UI

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## ⚠️ 安全提示

1. **生产环境请修改**:
   - JWT SECRET_KEY
   - 默认管理员密码
   - DeepSeek API Key

2. **敏感信息保护**:
   - 不要将 API Key 提交到代码仓库
   - 使用环境变量管理配置
   - 定期更换密钥

3. **数据安全**:
   - 定期备份 `data/` 目录
   - 检查 `uploads/` 文件内容
   - 监控临时文件清理日志

---

## 👨‍💻 作者信息

| 角色 | 姓名 | 说明 |
|------|------|------|
| **第一作者** | 陈思宇 | 项目负责人、核心开发 |
| **开发团队** | 灵犀网卫 | 网络安全技术团队 |

---

<p align="center">
  <b>Sec-LLM-Local</b> - 网络安全专用大语言模型平台<br>
  第一作者：<b>陈思宇</b> | 开发团队：<b>灵犀网卫</b>
</p>
