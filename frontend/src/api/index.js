import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 公司API
export const companyAPI = {
  getList: (params) => api.get('/companies/', { params }),
  getById: (id) => api.get(`/companies/${id}`),
  create: (data) => api.post('/companies/', data),
  update: (id, data) => api.put(`/companies/${id}`, data),
  delete: (id) => api.delete(`/companies/${id}`)
}

// 人才API
export const talentAPI = {
  getList: (params) => api.get('/talents/', { params }),
  getById: (id) => api.get(`/talents/${id}`),
  create: (data) => api.post('/talents/', data),
  update: (id, data) => api.put(`/talents/${id}`, data),
  delete: (id) => api.delete(`/talents/${id}`)
}

// 沟通记录API
export const communicationAPI = {
  getList: (params) => api.get('/communications/', { params }),
  getById: (id) => api.get(`/communications/${id}`),
  create: (data) => api.post('/communications/', data),
  update: (id, data) => api.put(`/communications/${id}`, data),
  delete: (id) => api.delete(`/communications/${id}`)
}

export default api
