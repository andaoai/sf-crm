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

// 证书API
export const certificateAPI = {
  // 证书类型管理
  getTypes: (params) => api.get('/certificates/types', { params }),
  getTypeByCode: (code) => api.get(`/certificates/types/${code}`),
  createType: (data) => api.post('/certificates/types', data),
  updateType: (code, data) => api.put(`/certificates/types/${code}`, data),

  // 具体证书管理
  getList: (params) => api.get('/certificates/', { params }),
  getStats: (params) => api.get('/certificates/stats', { params }),
  getById: (id) => api.get(`/certificates/${id}`),
  create: (data) => api.post('/certificates/', data),
  update: (id, data) => api.put(`/certificates/${id}`, data),
  delete: (id) => api.delete(`/certificates/${id}`),

  // 人才证书查询
  getTalentCertificates: (talentId) => api.get(`/certificates/talent/${talentId}`),
  getTalentCertificateSummary: (talentId) => api.get(`/certificates/talent/${talentId}/summary`),

  // 证书搜索功能
  searchByType: (certificateType, status = 'VALID') =>
    api.get('/certificates/search/by-type', {
      params: { certificate_type: certificateType, status }
    }),
  searchByCategory: (category, status = 'VALID') =>
    api.get('/certificates/search/by-category', {
      params: { category, status }
    }),

  // 即将到期的证书
  getExpiring: (days = 30) => api.get('/certificates/expiring', { params: { days } })
}

export default api
