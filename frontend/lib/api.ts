import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
  email?: string;
  full_name?: string;
}

export interface UserInfo {
  id: number;
  username: string;
  email: string | null;
  full_name: string | null;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserInfo;
}

// 兼容旧版本的 LoginResponse
export interface LoginResponse {
  token: string;
  user: string;
}

export const login = async (credentials: LoginRequest): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/api/login', credentials);
  return response.data;
};

export const register = async (data: RegisterRequest): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/api/register', data);
  return response.data;
};

export const getCurrentUser = async (token: string): Promise<UserInfo> => {
  const response = await api.get<UserInfo>('/api/me', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  reply: string;
  sources?: string[];
}

export const chat = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/api/chat', request);
  return response.data;
};

export interface UploadResponse {
  status: string;
  message: string;
  chunks?: number;
}

export const uploadFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export interface AnalysisResult {
  summary: string;
  threat_level: 'Low' | 'Medium' | 'High' | 'Critical';
  advice: string;
  details: Array<{
    type: string;
    payload: string;
    source_ip: string;
  }>;
}

export interface LogAnalysisResponse {
  filename: string;
  status: string;
  ai_analysis: AnalysisResult;
}

export const uploadLogFile = async (file: File): Promise<LogAnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  // 传递 mode=analysis 强制进行日志分析（而不是加入知识库）
  const response = await api.post<LogAnalysisResponse>('/api/upload?mode=analysis', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;
