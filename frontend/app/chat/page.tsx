'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
  Home,
  MessageSquare,
  Eye,
  FileText,
  LogOut,
  Shield,
  Search,
  Bell,
  User,
  HelpCircle,
  Send,
  Bot,
  Paperclip,
} from 'lucide-react';
import { chat, uploadFile, type UserInfo } from '@/lib/api';

interface Message {
  role: 'user' | 'ai';
  content: string;
  sources?: string[];
}

export default function ChatPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeMenu, setActiveMenu] = useState('chat');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 检查认证状态
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    setIsAuthenticated(true);

    // 读取用户信息
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        setUserInfo(JSON.parse(savedUser));
      } catch (e) {
        console.error('解析用户信息失败:', e);
      }
    }

    // 从 localStorage 恢复聊天记录
    const savedHistory = localStorage.getItem('cyberguard_chat_history');
    if (savedHistory) {
      try {
        const parsedMessages = JSON.parse(savedHistory);
        if (Array.isArray(parsedMessages) && parsedMessages.length > 0) {
          setMessages(parsedMessages);
        }
      } catch (error) {
        console.error('恢复聊天记录失败:', error);
      }
    }
  }, [router]);

  // 自动保存聊天记录到 localStorage
  useEffect(() => {
    if (messages.length > 0) {
      try {
        localStorage.setItem('cyberguard_chat_history', JSON.stringify(messages));
      } catch (error) {
        console.error('保存聊天记录失败:', error);
      }
    }
  }, [messages]);

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setShowUserMenu(false);
    router.push('/login');
  };

  // 点击外部关闭用户菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    };

    if (showUserMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showUserMenu]);

  const handleMenuClick = (menu: string) => {
    setActiveMenu(menu);
    if (menu === 'dashboard') {
      router.push('/');
    } else if (menu === 'chat') {
      router.push('/chat');
    } else if (menu === 'analysis') {
      router.push('/log-analysis');
    } else if (menu === 'reports') {
      router.push('/report-generation');
    }
  };

  const handleSend = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // 立即添加用户消息
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // 调用 API
      const response = await chat({ message: userMessage });
      
      // 添加 AI 回复
      setMessages((prev) => [
        ...prev,
        {
          role: 'ai',
          content: response.reply,
          sources: response.sources,
        },
      ]);
    } catch (error: any) {
      // 错误处理
      setMessages((prev) => [
        ...prev,
        {
          role: 'ai',
          content: `错误: ${error.response?.data?.detail || '发送消息失败，请稍后重试'}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // 检查文件类型
    const allowedTypes = ['.pdf', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
      alert('仅支持 PDF 和 TXT 文件');
      return;
    }

    setIsUploading(true);
    setUploadStatus('上传中...');

    try {
      const response = await uploadFile(file);
      
      if (response.status === 'success') {
        setUploadStatus(`✅ ${response.message}`);
        setTimeout(() => setUploadStatus(null), 3000);
      } else {
        setUploadStatus(`❌ ${response.message}`);
        setTimeout(() => setUploadStatus(null), 3000);
      }
    } catch (error: any) {
      setUploadStatus(`❌ 上传失败: ${error.response?.data?.message || error.message}`);
      setTimeout(() => setUploadStatus(null), 3000);
    } finally {
      setIsUploading(false);
      // 清空文件输入，允许重复上传同一文件
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  // 如果未认证，不渲染内容
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden">
      {/* 左侧固定侧边栏 */}
      <aside className="w-64 bg-slate-900 flex flex-col border-r border-slate-800">
        {/* Logo */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Shield className="w-8 h-8 text-cyan-400" />
            <div className="flex flex-col">
              <span className="text-xl font-bold text-white leading-tight">灵犀网卫</span>
              <span className="text-xl font-bold text-white leading-tight">Sec-LLM</span>
            </div>
          </div>
        </div>

        {/* 导航菜单 */}
        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => handleMenuClick('dashboard')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activeMenu === 'dashboard'
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                : 'text-gray-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Home className="w-5 h-5" />
            <span className="font-medium">仪表盘</span>
          </button>

          <button
            onClick={() => handleMenuClick('chat')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activeMenu === 'chat'
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                : 'text-gray-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            <span className="font-medium">AI智能回答</span>
          </button>

          <button
            onClick={() => handleMenuClick('analysis')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activeMenu === 'analysis'
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                : 'text-gray-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Eye className="w-5 h-5" />
            <span className="font-medium">日志分析</span>
          </button>

          <button
            onClick={() => handleMenuClick('reports')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activeMenu === 'reports'
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                : 'text-gray-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <FileText className="w-5 h-5" />
            <span className="font-medium">报告生成</span>
          </button>
        </nav>

        {/* 系统状态 */}
        <div className="p-4 border-t border-slate-800">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-gray-400">系统安全</span>
          </div>
          <p className="text-xs text-gray-500">上次扫描: 2 分钟前</p>
        </div>

        {/* 登出按钮 */}
        <div className="p-4 border-t border-slate-800">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-slate-800/50 transition-all"
          >
            <LogOut className="w-5 h-5" />
            <span className="font-medium">登出</span>
          </button>
        </div>
      </aside>

      {/* 主内容区域 */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* 顶部标题栏 */}
        <header className="h-16 bg-slate-900/50 backdrop-blur border-b border-white/5 flex items-center justify-between px-6 relative z-50">
          <div>
            <h1 className="text-xl font-bold text-white">AI智能回答</h1>
            <p className="text-xs text-gray-400">AI Security Analyst</p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* 搜索框 */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="搜索日志、IP、威胁..."
                className="pl-10 pr-4 py-2 bg-slate-800/50 border border-white/5 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 w-64"
              />
            </div>

            {/* 用户信息 */}
            <div className="flex items-center gap-3">
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <Bell className="w-5 h-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <HelpCircle className="w-5 h-5" />
              </button>
              {/* 用户头像和信息 */}
              <div className="relative z-[9999]" ref={userMenuRef}>
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 hover:bg-slate-800/50 rounded-lg p-1.5 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center border border-cyan-500/30">
                    <User className="w-4 h-4 text-cyan-400" />
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-white">
                      {userInfo?.full_name || userInfo?.username || '用户'}
                    </p>
                    <p className="text-xs text-gray-400">
                      {userInfo?.role === 'admin' ? '系统管理员' : '普通用户'}
                    </p>
                  </div>
                </button>

                {/* 用户信息悬浮卡片 */}
                {showUserMenu && (
                  <div className="fixed top-16 right-6 w-72 bg-slate-900 border border-slate-700 rounded-lg shadow-2xl z-[9999] overflow-hidden">
                    {/* 头部背景 */}
                    <div className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 p-4 border-b border-slate-700">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-full bg-cyan-500/30 flex items-center justify-center border-2 border-cyan-500/50">
                          <User className="w-6 h-6 text-cyan-400" />
                        </div>
                        <div>
                          <p className="text-lg font-semibold text-white">
                            {userInfo?.full_name || userInfo?.username || '用户'}
                          </p>
                          <p className="text-sm text-cyan-400">@{userInfo?.username || 'user'}</p>
                        </div>
                      </div>
                    </div>

                    {/* 用户详情 */}
                    <div className="p-4 space-y-3">
                      <div className="flex items-center gap-3 text-sm">
                        <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
                          <Shield className="w-4 h-4 text-cyan-400" />
                        </div>
                        <div>
                          <p className="text-gray-400 text-xs">角色</p>
                          <p className="text-white font-medium">
                            {userInfo?.role === 'admin' ? '系统管理员' : '普通用户'}
                          </p>
                        </div>
                      </div>

                      {userInfo?.email && (
                        <div className="flex items-center gap-3 text-sm">
                          <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
                            <svg className="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                          </div>
                          <div>
                            <p className="text-gray-400 text-xs">邮箱</p>
                            <p className="text-white font-medium">{userInfo.email}</p>
                          </div>
                        </div>
                      )}

                      <div className="flex items-center gap-3 text-sm">
                        <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
                          <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <div>
                          <p className="text-gray-400 text-xs">状态</p>
                          <p className="text-green-400 font-medium">在线</p>
                        </div>
                      </div>
                    </div>

                    {/* 操作按钮 */}
                    <div className="border-t border-slate-700 p-2">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        <span>退出登录</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* 消息区域 - 可滚动 */}
        <div className="flex-1 overflow-y-auto p-6 relative z-0">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <Bot className="w-16 h-16 text-cyan-400 mx-auto mb-4 opacity-50" />
                <p className="text-gray-400 text-lg">开始与 AI 安全分析师对话</p>
                <p className="text-gray-500 text-sm mt-2">询问安全相关问题，获取专业的攻防建议</p>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-4 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'ai' && (
                  <div className="w-10 h-10 rounded-full bg-slate-800/50 border border-white/5 flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-cyan-400" />
                  </div>
                )}

                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white'
                      : 'bg-slate-900/50 backdrop-blur border border-white/5 text-gray-100'
                  }`}
                >
                  <div className="whitespace-pre-wrap break-words">{message.content}</div>
                  
                  {/* 参考来源功能已隐藏 */}
                </div>

                {message.role === 'user' && (
                  <div className="w-10 h-10 rounded-full bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-cyan-400" />
                  </div>
                )}
              </div>
            ))}

            {/* 思考中指示器 */}
            {isLoading && (
              <div className="flex gap-4 justify-start">
                <div className="w-10 h-10 rounded-full bg-slate-800/50 border border-white/5 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-cyan-400" />
                </div>
                <div className="bg-slate-900/50 backdrop-blur border border-white/5 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-gray-400">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-sm">思考中...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* 输入区域 - 固定在底部 */}
        <div className="border-t border-white/5 bg-slate-900/50 backdrop-blur p-4">
          <div className="max-w-4xl mx-auto">
            {/* 上传状态提示 */}
            {uploadStatus && (
              <div className={`mb-3 px-4 py-2 rounded-lg text-sm ${
                uploadStatus.includes('✅') 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {uploadStatus}
              </div>
            )}
            
            <div className="flex gap-4 items-end">
              {/* 隐藏的文件输入 */}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileUpload}
                className="hidden"
              />
              
              {/* 文件上传按钮 */}
              <button
                onClick={triggerFileInput}
                disabled={isUploading || isLoading}
                className="px-4 py-3 bg-slate-800/50 border border-white/5 rounded-lg text-gray-400 hover:text-cyan-400 hover:border-cyan-500/30 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                title="上传文件 (PDF/TXT)"
              >
                {isUploading ? (
                  <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <Paperclip className="w-5 h-5" />
                )}
              </button>
              
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="输入您的问题... (按 Enter 发送，Shift+Enter 换行)"
                  rows={1}
                  className="w-full px-4 py-3 bg-slate-800/50 border border-white/5 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 resize-none font-mono text-sm"
                  style={{
                    minHeight: '48px',
                    maxHeight: '200px',
                    height: 'auto',
                  }}
                  onInput={(e) => {
                    const target = e.target as HTMLTextAreaElement;
                    target.style.height = 'auto';
                    target.style.height = `${target.scrollHeight}px`;
                  }}
                  disabled={isLoading || isUploading}
                />
              </div>
              <button
                onClick={handleSend}
                disabled={!inputMessage.trim() || isLoading || isUploading}
                className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold rounded-lg transition-all duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
                <span>发送</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
