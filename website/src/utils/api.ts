/**
 * API 客户端工具
 * 用于调用后端 API 服务
 */

// API 基础地址
// 在生产环境中使用相对路径（通过 Nginx 反向代理转发到后端）
// 在浏览器中，空字符串会使用当前域名，通过 Nginx 代理到后端
// 注意：不能使用 process.env，因为 process 在浏览器中不存在
// 如果需要配置不同的 API 地址，可以通过 Docusaurus 的 webpack 配置注入
const API_BASE_URL = '';

// 通用响应类型
export interface ApiResponse<T> {
  total: number;
  items: T[];
}

// 讨论类型
export interface Discussion {
  id: number;
  title: string;
  content: string;
  category: string; // usage/bug/feature/other
  author?: string;
  status: string; // open/solved
  view_count: number;
  reply_count: number;
  created_at: string;
  updated_at: string;
}

// 讨论回复类型
export interface DiscussionReply {
  id: number;
  discussion_id: number;
  content: string;
  author?: string;
  created_at: string;
  updated_at: string;
}

// 新闻类型
export interface News {
  id: number;
  title: string;
  content: string;
  excerpt?: string;
  author?: string;
  category?: string;
  cover_image?: string;
  source?: string;
  slug?: string;
  status: string;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * 通用 API 请求函数
 */
async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  console.log('[API] Making request to:', url, 'API_BASE_URL:', API_BASE_URL);
  
  // 自动添加认证 token（如果存在）
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    // 添加缓存控制头，防止浏览器缓存
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0',
    ...(options?.headers as Record<string, string>),
  };
  
  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  try {
    console.log('[API] Fetch options:', { mode: 'cors', credentials: 'include', cache: 'no-store', headers });
    console.log('[API] Request URL:', url);
    console.log('[API] Request method:', options?.method || 'GET');
    
    const fetchPromise = fetch(url, {
      ...options,
      mode: 'cors',
      credentials: 'include',
      // 完全禁用缓存，确保每次请求都获取最新数据
      cache: 'no-store',
      headers,
    });
    
    console.log('[API] Fetch promise created, waiting for response...');
    
    // 添加超时处理
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => {
        reject(new Error('Request timeout after 10 seconds'));
      }, 10000);
    });
    
    const response = await Promise.race([fetchPromise, timeoutPromise]);
    
    console.log('[API] Response received!');
    console.log('[API] Response status:', response.status, 'URL:', url);
    console.log('[API] Response statusText:', response.statusText);
    console.log('[API] Response ok:', response.ok);
    // 记录响应头（如果可用）
    try {
      const headersObj: Record<string, string> = {};
      response.headers.forEach((value, key) => {
        headersObj[key] = value;
      });
      console.log('[API] Response headers:', headersObj);
    } catch (e) {
      console.log('[API] Could not read response headers');
    }

    // 304 Not Modified 对于 API 请求来说应该重新获取数据
    // 如果返回 304，说明浏览器使用了缓存，我们需要强制获取新数据
    if (response.status === 304) {
      // 重新请求，但添加时间戳参数来绕过缓存
      const separator = url.includes('?') ? '&' : '?';
      const timestampedUrl = `${url}${separator}_t=${Date.now()}`;
      const retryResponse = await fetch(timestampedUrl, {
        ...options,
        mode: 'cors',
        credentials: 'include',
        cache: 'no-store',
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0',
          ...options?.headers,
        },
      });
      
      if (!retryResponse.ok) {
        throw new Error(`API request failed: ${retryResponse.statusText}`);
      }
      
      return await retryResponse.json();
    }

    if (!response.ok) {
      let errorMessage = `API request failed: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      } catch (e) {
        // 如果响应不是 JSON，使用默认错误消息
        console.error('[API] Failed to parse error response as JSON:', e);
      }
      console.error(`[API] Request failed: ${response.status} ${errorMessage} for ${url}`);
      throw new Error(errorMessage);
    }

    // 尝试解析响应体
    let data;
    try {
      const responseText = await response.text();
      console.log('[API] Response text (raw):', responseText);
      if (responseText) {
        data = JSON.parse(responseText);
        console.log('[API] Response data (parsed):', data);
      } else {
        console.warn('[API] Response body is empty');
        throw new Error('Response body is empty');
      }
    } catch (parseError) {
      console.error('[API] Failed to parse response as JSON:', parseError);
      throw new Error(`Failed to parse response: ${parseError instanceof Error ? parseError.message : String(parseError)}`);
    }
    
    return data;
  } catch (error) {
    console.error(`API request error for ${endpoint}:`, error);
    throw error;
  }
}

/**
 * 讨论 API
 */
export const discussionsApi = {
  /**
   * 获取讨论列表
   */
  getList: async (params?: {
    skip?: number;
    limit?: number;
    category?: string;
    status?: string;
  }): Promise<ApiResponse<Discussion>> => {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.category) queryParams.append('category', params.category);
    if (params?.status) queryParams.append('status', params.status);

    const query = queryParams.toString();
    return apiRequest<ApiResponse<Discussion>>(
      `/api/discussions${query ? `?${query}` : ''}`
    );
  },

  /**
   * 获取单个讨论
   */
  getById: async (id: number): Promise<Discussion> => {
    return apiRequest<Discussion>(`/api/discussions/${id}`);
  },

  /**
   * 创建讨论
   */
  create: async (discussion: {
    title: string;
    content: string;
    category: string;
    author?: string;
    status?: string;
  }): Promise<Discussion> => {
    return apiRequest<Discussion>('/api/discussions', {
      method: 'POST',
      body: JSON.stringify(discussion),
    });
  },

  /**
   * 更新讨论
   */
  update: async (id: number, discussion: {
    title?: string;
    content?: string;
    category?: string;
    status?: string;
  }): Promise<Discussion> => {
    return apiRequest<Discussion>(`/api/discussions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(discussion),
    });
  },

  /**
   * 删除讨论
   */
  delete: async (id: number): Promise<{message: string}> => {
    return apiRequest<{message: string}>(`/api/discussions/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * 获取讨论的回复列表
   */
  getReplies: async (
    discussionId: number,
    params?: {
      skip?: number;
      limit?: number;
    }
  ): Promise<ApiResponse<DiscussionReply>> => {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());

    const query = queryParams.toString();
    return apiRequest<ApiResponse<DiscussionReply>>(
      `/api/discussions/${discussionId}/replies${query ? `?${query}` : ''}`
    );
  },

  /**
   * 创建讨论回复
   */
  createReply: async (
    discussionId: number,
    reply: {
      content: string;
      author?: string;
    }
  ): Promise<DiscussionReply> => {
    return apiRequest<DiscussionReply>(`/api/discussions/${discussionId}/replies`, {
      method: 'POST',
      body: JSON.stringify(reply),
    });
  },

  /**
   * 删除回复
   */
  deleteReply: async (replyId: number): Promise<{message: string}> => {
    return apiRequest<{message: string}>(`/api/discussions/replies/${replyId}`, {
      method: 'DELETE',
    });
  },
};

// 用户类型
export interface User {
  id: number;
  username: string;
  email: string;
  role: string; // developer/admin/root
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Token 响应类型
export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// 登录请求
export interface LoginRequest {
  username: string;
  password: string;
}

// 注册请求
export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

// 网站配置类型
export interface SiteConfig {
  id: number;
  key: string;
  value: string | null;
  description: string | null;
  updated_at: string;
}

// 网站配置创建/更新
export interface SiteConfigCreate {
  key: string;
  value?: string;
  description?: string;
}

export interface SiteConfigUpdate {
  value?: string;
  description?: string;
}

/**
 * 认证 API
 */
export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    return apiRequest<TokenResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  register: async (data: RegisterRequest): Promise<TokenResponse> => {
    return apiRequest<TokenResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getCurrentUser: async (): Promise<User> => {
    return apiRequest<User>('/api/auth/me');
  },

  logout: async (): Promise<void> => {
    removeAuthToken();
  },
};

/**
 * 管理台 API
 */
export const adminApi = {
  getConfigs: async (): Promise<SiteConfig[]> => {
    return apiRequest<SiteConfig[]>('/api/admin/config');
  },

  getConfig: async (key: string): Promise<SiteConfig> => {
    return apiRequest<SiteConfig>(`/api/admin/config/${key}`);
  },

  createConfig: async (data: SiteConfigCreate): Promise<SiteConfig> => {
    return apiRequest<SiteConfig>('/api/admin/config', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  updateConfig: async (key: string, data: SiteConfigUpdate): Promise<SiteConfig> => {
    return apiRequest<SiteConfig>(`/api/admin/config/${key}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  deleteConfig: async (key: string): Promise<void> => {
    await apiRequest(`/api/admin/config/${key}`, {
      method: 'DELETE',
    });
  },

  getNewsList: async (): Promise<News[]> => {
    return apiRequest<News[]>('/api/admin/news');
  },

  createNews: async (data: any): Promise<any> => {
    return apiRequest('/api/admin/news', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  updateNews: async (id: number, data: any): Promise<any> => {
    return apiRequest(`/api/admin/news/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  deleteNews: async (id: number): Promise<void> => {
    await apiRequest(`/api/admin/news/${id}`, {
      method: 'DELETE',
    });
  },
};

/**
 * 用户管理 API（仅 root）
 */
export const usersApi = {
  getList: async (): Promise<User[]> => {
    return apiRequest<User[]>('/api/users');
  },

  getById: async (id: number): Promise<User> => {
    return apiRequest<User>(`/api/users/${id}`);
  },

  create: async (data: RegisterRequest & {role?: string}): Promise<User> => {
    return apiRequest<User>('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: async (id: number, data: Partial<User> & {password?: string}): Promise<User> => {
    return apiRequest<User>(`/api/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  delete: async (id: number): Promise<void> => {
    await apiRequest(`/api/users/${id}`, {
      method: 'DELETE',
    });
  },
};

// Token 管理函数
const TOKEN_KEY = 'auth_token';

export function setAuthToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

export function removeAuthToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
}

// 文档版本相关类型
export interface DocVersion {
  name: string; // 版本名称，如 "1.0.4"
  label: string; // 显示标签，如 "1.0.4 LTS"
  release_date?: string; // 发布日期
  type?: string; // 版本类型，如 "LTS", "STS"
}

export interface DocItem {
  title: string; // 文档标题
  path: string; // 文档路径（相对于文档中心目录）
  type: string; // 类型：file 或 directory
  children?: DocItem[]; // 子项（仅目录类型有）
}

export interface DocVersionsResponse {
  versions: DocVersion[];
  current?: string; // 当前默认版本
}

export interface DocVersionDetailResponse {
  version: DocVersion;
  docs: DocItem[];
}

export interface DocContentResponse {
  version: string;
  path: string;
  content: string;
  title: string;
}

/**
 * 文档版本 API
 */
export const docsVersionsApi = {
  /**
   * 获取文档版本列表
   */
  getVersions: async (): Promise<DocVersionsResponse> => {
    return apiRequest<DocVersionsResponse>('/api/docs-versions/versions');
  },

  /**
   * 获取指定版本的文档详情
   */
  getVersionDetail: async (versionName: string): Promise<DocVersionDetailResponse> => {
    return apiRequest<DocVersionDetailResponse>(`/api/docs-versions/versions/${versionName}`);
  },

  /**
   * 获取文档内容
   */
  getDocContent: async (version: string, path: string): Promise<DocContentResponse> => {
    return apiRequest<DocContentResponse>(`/api/docs-versions/doc-content?version=${encodeURIComponent(version)}&path=${encodeURIComponent(path)}`);
  },
};


