// API调用模块 - 配置后端地址
const API_BASE = 'http://localhost:5000/api'

async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  const data = await res.json()
  if (data.code !== 200) {
    throw new Error(data.message || '请求失败')
  }
  return data
}

// 数据资产
export const assetsApi = {
  list: (params) => request(`/assets?${new URLSearchParams(params)}`),
  get: (id) => request(`/assets/${id}`),
  create: (data) => request('/assets', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/assets/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/assets/${id}`, { method: 'DELETE' })
}

// 模型管理
export const modelsApi = {
  list: (params) => request(`/models?${new URLSearchParams(params)}`),
  get: (id) => request(`/models/${id}`),
  create: (data) => request('/models', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/models/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/models/${id}`, { method: 'DELETE' })
}

// 元数据管理
export const metadataApi = {
  list: (params) => request(`/metadata?${new URLSearchParams(params)}`),
  get: (id) => request(`/metadata/${id}`),
  create: (data) => request('/metadata', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/metadata/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/metadata/${id}`, { method: 'DELETE' })
}

// 报表管理
export const reportsApi = {
  list: (params) => request(`/reports?${new URLSearchParams(params)}`),
  get: (id) => request(`/reports/${id}`),
  create: (data) => request('/reports', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/reports/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/reports/${id}`, { method: 'DELETE' })
}
