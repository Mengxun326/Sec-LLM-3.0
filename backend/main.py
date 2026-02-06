import os
import shutil
import threading
import time
from datetime import datetime, timedelta
from typing import Optional

# --- 🔥 核心补丁：强制关闭代理 ---
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
os.environ['no_proxy'] = 'localhost,127.0.0.1'

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import json
from openai import OpenAI  # 引入 OpenAI 库

# ================= 数据库 & 认证相关导入 =================
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt

# ================= JWT 配置 =================
SECRET_KEY = "your-super-secret-key-change-in-production-灵犀网卫-2024"  # 生产环境请使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Token 有效期 24 小时

# ================= 数据库配置 =================
DATABASE_URL = "sqlite:///./data/users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ================= 数据库模型 =================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="user")  # admin, user
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

# 创建数据库表
os.makedirs("./data", exist_ok=True)
Base.metadata.create_all(bind=engine)

# ================= 密码加密工具 =================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

# ================= JWT Token 工具 =================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ================= 数据库依赖 =================
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= OAuth2 配置 =================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """从 Token 获取当前用户"""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户（必须登录）"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或 Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

# ================= 初始化默认管理员账户 =================
def init_default_admin():
    """创建默认管理员账户（如果不存在）"""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                email="admin@sec-llm.local",
                full_name="系统管理员",
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("[OK] 已创建默认管理员账户: admin / admin123")
        else:
            print("[OK] 管理员账户已存在")
    finally:
        db.close()

# 启动时初始化
init_default_admin()

app = FastAPI(title="Sec-LLM RAG Backend", version="3.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= 临时文件清理配置 =================
TEMP_DIR = "temp"
TEMP_FILE_MAX_AGE_HOURS = 24  # 文件最大保留时间（小时）
CLEANUP_INTERVAL_HOURS = 1   # 清理检查间隔（小时）

def cleanup_temp_files():
    """清理超过指定时间的临时文件"""
    if not os.path.exists(TEMP_DIR):
        return
    
    now = time.time()
    max_age_seconds = TEMP_FILE_MAX_AGE_HOURS * 3600
    cleaned_count = 0
    
    try:
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                file_age = now - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    cleaned_count += 1
                    print(f"[CLEANUP] 已删除过期临时文件: {filename}")
        
        if cleaned_count > 0:
            print(f"[CLEANUP] 本次清理完成，共删除 {cleaned_count} 个过期文件")
    except Exception as e:
        print(f"[CLEANUP ERROR] 清理临时文件时出错: {e}")

def temp_cleanup_scheduler():
    """后台定时清理任务"""
    while True:
        time.sleep(CLEANUP_INTERVAL_HOURS * 3600)  # 每隔指定小时检查一次
        print(f"[CLEANUP] 开始执行定时清理任务...")
        cleanup_temp_files()

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    # 启动时先执行一次清理
    print("[STARTUP] 执行启动清理...")
    cleanup_temp_files()
    
    # 启动后台清理线程
    cleanup_thread = threading.Thread(target=temp_cleanup_scheduler, daemon=True)
    cleanup_thread.start()
    print(f"[STARTUP] 临时文件清理任务已启动 (保留时间: {TEMP_FILE_MAX_AGE_HOURS}小时, 检查间隔: {CLEANUP_INTERVAL_HOURS}小时)")

# ================= DeepSeek API 配置区域 =================
# 1. 这里填你的 DeepSeek API Key
API_KEY = "sk-0822242e3472406b9514c70e04a93cb3"  # ⚠️ 请替换为你的真实 API Key
# 2. 这里填 Base URL (DeepSeek 官方是 https://api.deepseek.com)
BASE_URL = "https://api.deepseek.com"
# ===========================================

# 初始化 OpenAI 客户端（用于 DeepSeek）
deepseek_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# --- 全局变量：向量数据库 ---
VECTOR_DB_DIR = "./data/chroma_db"
# 初始化嵌入模型 (使用刚才下载的 nomic-embed-text)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

# 尝试加载已有的数据库
try:
    vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    print("[OK] 已加载本地知识库")
except:
    vector_store = None
    print("[WARN] 暂无知识库，等待上传文件")

# --- 数据模型 ---
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class ChatRequest(BaseModel):
    message: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    role: str
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- 接口 1: 健康检查 ---
@app.get("/")
def health_check():
    return {"status": "online", "system": "Sec-LLM V3.0 RAG", "engine": "Ollama + DeepSeek + RAG"}

# --- 接口 2: 用户注册 ---
@app.post("/api/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册接口"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == req.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册"
        )
    
    # 检查邮箱是否已存在
    if req.email:
        existing_email = db.query(User).filter(User.email == req.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    # 创建新用户
    new_user = User(
        username=req.username,
        hashed_password=get_password_hash(req.password),
        email=req.email,
        full_name=req.full_name,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"[OK] 新用户注册: {req.username}")
    
    # 自动生成 Token
    access_token = create_access_token(data={"sub": new_user.username})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            role=new_user.role
        )
    )

# --- 接口 3: 用户登录 ---
@app.post("/api/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """用户登录接口"""
    # 查找用户
    user = db.query(User).filter(User.username == req.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    # 生成 JWT Token
    access_token = create_access_token(data={"sub": user.username})
    
    print(f"[OK] 用户登录: {user.username}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role
        )
    )

# --- 接口 4: 获取当前用户信息 ---
@app.get("/api/me")
def get_me(current_user: User = Depends(get_current_active_user)):
    """获取当前登录用户信息"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role
    )

# --- 接口 5: 仪表盘统计 ---
@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    import random
    return {
        "total_events": 1200 + random.randint(0, 50),
        "active_threats": 20 + random.randint(0, 5),
        "online_users": 8400 + random.randint(0, 100),
        "system_load": 60 + random.randint(0, 10),
        "chart_data": [{"time": f"{i+10}:00", "value": random.randint(30, 100)} for i in range(7)]
    }

# --- 接口 5.1: 临时文件管理 ---
@app.get("/api/admin/temp-status")
def get_temp_status():
    """获取临时文件夹状态"""
    if not os.path.exists(TEMP_DIR):
        return {
            "exists": False,
            "file_count": 0,
            "total_size_mb": 0,
            "files": []
        }
    
    files_info = []
    total_size = 0
    now = time.time()
    
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        if os.path.isfile(file_path):
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            file_age_hours = (now - file_stat.st_mtime) / 3600
            total_size += file_size
            files_info.append({
                "name": filename,
                "size_kb": round(file_size / 1024, 2),
                "age_hours": round(file_age_hours, 2),
                "will_be_cleaned": file_age_hours > TEMP_FILE_MAX_AGE_HOURS
            })
    
    return {
        "exists": True,
        "file_count": len(files_info),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "max_age_hours": TEMP_FILE_MAX_AGE_HOURS,
        "files": files_info
    }

@app.post("/api/admin/cleanup-temp")
def manual_cleanup_temp():
    """手动触发临时文件清理"""
    if not os.path.exists(TEMP_DIR):
        return {"status": "success", "message": "临时文件夹不存在，无需清理", "cleaned_count": 0}
    
    now = time.time()
    max_age_seconds = TEMP_FILE_MAX_AGE_HOURS * 3600
    cleaned_count = 0
    cleaned_files = []
    
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                cleaned_count += 1
                cleaned_files.append(filename)
    
    return {
        "status": "success",
        "message": f"清理完成，删除了 {cleaned_count} 个过期文件",
        "cleaned_count": cleaned_count,
        "cleaned_files": cleaned_files
    }

# --- 辅助函数：AI 日志分析（使用真实的 DeepSeek API）---
def real_llm_analysis(log_content: str):
    """
    调用真实的大模型进行日志分析
    """
    print(f"[ANALYSIS] 正在分析日志，长度: {len(log_content)} 字符...")
    
    # 定义提示词 (Prompt Engineering)
    system_prompt = """
    你是一位资深的网络安全专家。请分析用户上传的日志片段。
    请以纯 JSON 格式返回分析结果，不要包含 Markdown 格式（如 ```json）。
    返回结构必须包含：
    - summary: 简短的分析总结
    - threat_level: 威胁等级 (Low/Medium/High/Critical)
    - details: 一个列表，包含具体的攻击类型、Payload和源IP（如果能在日志里找到）
    - advice: 针对性的修复或防御建议
    """
    
    user_prompt = f"请分析以下日志内容：\n\n{log_content}"

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",  # 或者 deepseek-reasoner
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,  # 低温度，保证输出格式稳定
            response_format={ "type": "json_object" }  # 强制 JSON 模式（关键！）
        )
        
        # 获取 AI 的回复内容
        ai_text = response.choices[0].message.content
        print("[AI] 回复原文本:", ai_text)  # 方便调试
        
        # 将字符串转为 Python 字典
        return json.loads(ai_text)
        
    except Exception as e:
        print(f"[ERROR] AI 调用出错: {e}")
        return {
            "summary": "AI 分析服务暂时不可用",
            "threat_level": "Unknown",
            "details": [],
            "advice": f"请检查后端日志。错误信息: {str(e)}"
        }

# --- 接口 6: 文件上传 (支持 RAG 知识库上传和日志分析) ---
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), mode: str = "auto"):
    """
    文件上传接口
    mode 参数:
    - "auto": 自动判断（PDF/TXT 加入知识库，其他做日志分析）
    - "rag": 强制加入 RAG 知识库
    - "analysis": 强制进行日志分析
    """
    file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    
    # 根据 mode 参数决定处理方式
    should_do_rag = False
    if mode == "rag":
        should_do_rag = True
    elif mode == "analysis":
        should_do_rag = False
    else:  # auto 模式
        should_do_rag = file_extension in ['pdf', 'txt']
    
    # 判断文件类型：如果是 PDF 或 TXT，则添加到 RAG 知识库
    if should_do_rag:
        # RAG 知识库上传
        try:
            # 1. 先保存到 uploads/ （永久存储）
            os.makedirs("uploads", exist_ok=True)
            uploads_path = f"uploads/{file.filename}"
            
            with open(uploads_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"[UPLOAD] 文件已永久保存到: {uploads_path}")
            
            # 2. 复制到 temp/ （用于 RAG 处理，会被自动清理）
            os.makedirs("temp", exist_ok=True)
            temp_path = f"temp/{file.filename}"
            shutil.copy2(uploads_path, temp_path)
            
            # 3. 从 temp 目录加载文件进行 RAG 处理
            if file.filename.endswith(".pdf"):
                loader = PyPDFLoader(temp_path)
            else:
                loader = TextLoader(temp_path, encoding="utf-8")
            
            docs = loader.load()
            
            # 切分文本 (Chunks)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            splits = text_splitter.split_documents(docs)
            
            # 存入向量数据库
            global vector_store
            if vector_store is None:
                vector_store = Chroma.from_documents(
                    documents=splits,
                    embedding=embeddings,
                    persist_directory=VECTOR_DB_DIR
                )
                print(f"[OK] 创建新知识库，添加文件: {file.filename}, {len(splits)} 个片段")
            else:
                vector_store.add_documents(splits)
                print(f"[OK] 添加文件到知识库: {file.filename}, {len(splits)} 个片段")
            
            return {
                "status": "success",
                "message": f"成功学习文件: {file.filename}（已永久保存到 uploads/）",
                "chunks": len(splits),
                "saved_path": uploads_path
            }
        except Exception as e:
            print(f"[ERROR] RAG 上传失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    # 否则，进行日志分析
    else:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 读取日志内容 (限制前 3000 字符，避免 Tokens 超支)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                log_content = f.read(3000)
        except:
            # 如果 utf-8 读取失败，尝试 latin-1 (常见于服务器日志)
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    log_content = f.read(3000)
            except Exception as e:
                return {
                    "filename": file.filename,
                    "status": "error",
                    "ai_analysis": {
                        "summary": "文件读取失败",
                        "threat_level": "Unknown",
                        "details": [],
                        "advice": f"文件编码问题: {str(e)}"
                    }
                }

        # === 调用真实的 AI ===
        ai_report = real_llm_analysis(log_content)

        return {
            "filename": file.filename,
            "status": "success",
            "ai_analysis": ai_report
        }

# --- 接口 7: 智能对话 (带 RAG 检索) ---
@app.post("/api/chat")
def chat(req: ChatRequest):
    print(f"[QUERY] 用户提问: {req.message}")
    
    context_text = ""
    sources = []
    
    # 1. 先去知识库里查 (RAG)
    if vector_store:
        print("[RAG] 正在检索知识库...")
        # 增加检索数量，确保能获取多个不同文件的片段
        # 检索更多片段（k=15），然后按文件分组，确保每个文件至少有一个片段
        results = vector_store.similarity_search(req.message, k=15)
        if results:
            print(f"[DEBUG] 检索到 {len(results)} 个文档片段")
            
            # 按文件来源分组
            source_groups = {}
            for doc in results:
                source = doc.metadata.get("source", "未知来源")
                print(f"[DEBUG] 文档来源: {source}")
                if source not in source_groups:
                    source_groups[source] = []
                source_groups[source].append(doc)
            
            print(f"[DEBUG] 文件分组: {len(source_groups)} 个不同文件")
            for source, docs in source_groups.items():
                print(f"[DEBUG]   - {os.path.basename(source)}: {len(docs)} 个片段")
            
            # 先收集所有不同的来源文件（在限制文档之前）
            all_sources = list(set([doc.metadata.get("source", "未知来源") for doc in results]))
            print(f"[DEBUG] 所有来源文件: {len(all_sources)} 个")
            for s in all_sources:
                print(f"[DEBUG]   - {os.path.basename(s)}")
            
            # 从每个文件中选择最相关的片段（每个文件最多2个片段）
            selected_docs = []
            for source, docs in source_groups.items():
                # 每个文件最多取2个最相关的片段
                selected_docs.extend(docs[:2])
            
            # 按相关性重新排序（保持前10个最相关的用于上下文）
            selected_docs = selected_docs[:10]
            
            # 构建上下文文本
            context_text = "\n\n".join([doc.page_content for doc in selected_docs])
            
            # 使用所有来源文件，而不仅仅是 selected_docs 中的
            sources = all_sources
            print(f"[OK] 找到相关资料: {len(selected_docs)} 个片段用于上下文，来自 {len(sources)} 个文件")
            print(f"[OK] 文件列表: {[os.path.basename(s) for s in sources]}")
    
    # 2. 定义核心人设 (System Prompt) - 深度定制版
    # 实现"双标"处理：无关问题简短拒绝，安全问题详细展开
    if context_text:
        # 如果有 RAG 检索到的资料，结合资料和身份
        system_instruction = f"""
你是 Sec-LLM，由灵犀网卫开发的【网络安全专用】大模型。

## 核心规则（必须严格遵守）

### 规则1：自我介绍
如果用户问"你是谁"、"介绍你自己"等身份问题，只回复：
"你好！我是Sec-LLM，是由灵犀网卫开发的网络安全专门用途大模型，很高兴为您服务！"

### 规则2：严格拒绝非安全话题
你【只能】回答以下领域的问题：
- 网络安全、黑客攻防、渗透测试、漏洞挖掘
- 编程开发、代码审计、软件安全
- 服务器运维、Linux系统、网络协议

对于【任何其他话题】，包括但不限于：历史、文学、诗人、地理、娱乐、生活、情感、数学、物理、化学、生物等，你必须拒绝回答。

拒绝时只说这一句话："抱歉，作为网络安全专用模型，我只能回答网络安全与技术相关的问题。"

【禁止】回答任何非安全相关的问题，即使你知道答案也不能说。

### 规则3：安全问题必须详细回答（重要！）
对于网络安全相关问题，你必须提供【极其详尽、全面、专业】的回答。回答要尽可能长，内容要丰富。

每次回答都必须包含以下所有部分：

**1. 概念定义**：用通俗易懂的语言解释这个概念是什么

**2. 核心原理**：深入解释技术原理和底层机制，越详细越好

**3. 攻击分类**：如果是攻击类型，列出所有变种和分类

**4. 实战案例**：描述真实世界中的攻击场景和案例

**5. 代码示例**：提供具体的攻击代码或防御代码示例，用代码块展示

**6. 检测方法**：如何检测这种攻击或问题

**7. 防御方案**：详细的防御措施和最佳实践，列出多种方法

**8. 工具推荐**：相关的安全工具推荐

回答长度要求：至少500字以上，越详细越好！

## 参考资料：
{context_text}
"""
    else:
        # 如果没有资料，只使用身份设定和话题过滤
        system_instruction = """
你是 Sec-LLM，由灵犀网卫开发的【网络安全专用】大模型。

## 核心规则（必须严格遵守）

### 规则1：自我介绍
如果用户问"你是谁"、"介绍你自己"等身份问题，只回复：
"你好！我是Sec-LLM，是由灵犀网卫开发的网络安全专门用途大模型，很高兴为您服务！"

### 规则2：严格拒绝非安全话题
你【只能】回答以下领域的问题：
- 网络安全、黑客攻防、渗透测试、漏洞挖掘
- 编程开发、代码审计、软件安全
- 服务器运维、Linux系统、网络协议

对于【任何其他话题】，包括但不限于：历史、文学、诗人、地理、娱乐、生活、情感、数学、物理、化学、生物等，你必须拒绝回答。

拒绝时只说这一句话："抱歉，作为网络安全专用模型，我只能回答网络安全与技术相关的问题。"

【禁止】回答任何非安全相关的问题，即使你知道答案也不能说。

### 规则3：安全问题必须详细回答（重要！）
对于网络安全相关问题，你必须提供【极其详尽、全面、专业】的回答。回答要尽可能长，内容要丰富。

每次回答都必须包含以下所有部分：

**1. 概念定义**：用通俗易懂的语言解释这个概念是什么

**2. 核心原理**：深入解释技术原理和底层机制，越详细越好

**3. 攻击分类**：如果是攻击类型，列出所有变种和分类

**4. 实战案例**：描述真实世界中的攻击场景和案例

**5. 代码示例**：提供具体的攻击代码或防御代码示例，用代码块展示

**6. 检测方法**：如何检测这种攻击或问题

**7. 防御方案**：详细的防御措施和最佳实践，列出多种方法

**8. 工具推荐**：相关的安全工具推荐

回答长度要求：至少500字以上，越详细越好！

## 示例对话：

用户: 你是谁
回复: 你好！我是Sec-LLM，是由灵犀网卫开发的网络安全专门用途大模型，很高兴为您服务！

用户: 李白是谁
回复: 抱歉，作为网络安全专用模型，我只能回答网络安全与技术相关的问题。

用户: 李白是哪个朝代的
回复: 抱歉，作为网络安全专用模型，我只能回答网络安全与技术相关的问题。

用户: 1+1等于几
回复: 抱歉，作为网络安全专用模型，我只能回答网络安全与技术相关的问题。

用户: 什么是SQL注入
回复: （详细解释SQL注入的原理、攻击方式、代码示例和防御方案）
"""
    
    # 3. 组装消息列表
    # 将 system_instruction 放在最前面作为第一条 system 消息
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": req.message}
    ]
    
    try:
        # 使用原生 HTTP 请求 (最稳的方式)
        url = "http://127.0.0.1:11434/api/chat"
        payload = {
            "model": "deepseek-r1:1.5b",
            "messages": messages,
            "stream": False,
            "temperature": 0.5  # 适中温度，平衡遵循指令和内容丰富度
        }
        
        resp = requests.post(url, json=payload, proxies={"http": None, "https": None})
        ai_reply = resp.json()['message']['content']
        
        # 4. 返回所有相关的来源文件
        source_names = [os.path.basename(s) for s in sources] if sources else []
        print(f"[DEBUG] 返回的来源文件: {source_names}")
        print(f"[DEBUG] 来源文件数量: {len(source_names)}")
        return {
            "reply": ai_reply,
            "sources": source_names if source_names else ["本地 DeepSeek-R1 模型"]
        }
        
    except Exception as e:
        return {"reply": f"AI 思考中断: {str(e)}", "sources": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
