<template>
  <div class="certificates-page">
    <div class="page-header">
      <h1>证书管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          添加证书
        </el-button>
      </div>
    </div>

    <!-- 搜索筛选区域 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline class="search-form">
          <el-form-item label="证书类型">
            <el-select
              v-model="searchForm.certificateType"
              placeholder="选择证书类型"
              clearable
              style="width: 180px"
            >
              <el-option
                v-for="type in certificateTypes"
                :key="type.type_code"
                :label="type.type_name"
                :value="type.type_name"
              />
            </el-select>

          </el-form-item>
          <el-form-item label="证书大类">
            <el-select
              v-model="searchForm.category"
              placeholder="选择证书大类"
              clearable
              style="width: 150px"
            >
              <el-option
                v-for="category in categories"
                :key="category"
                :label="category"
                :value="category"
              />
            </el-select>

          </el-form-item>
          <el-form-item label="证书状态">
            <el-select
              v-model="searchForm.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
            >
              <el-option label="全部" value="" />
              <el-option label="有效" value="VALID" />
              <el-option label="过期" value="EXPIRED" />
              <el-option label="注销" value="REVOKED" />
            </el-select>
          </el-form-item>
          <el-form-item label="人才搜索">
            <el-select
              v-model="searchForm.talentName"
              placeholder="搜索人才姓名"
              filterable
              remote
              clearable
              :remote-method="searchTalents"
              :loading="talentSearchLoading"
              style="width: 200px"
            >
              <el-option
                v-for="talent in talentOptions"
                :key="talent.id"
                :label="talent.name"
                :value="talent.name"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchCertificates">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 证书统计 -->
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total }}</div>
              <div class="stat-label">总证书数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.valid }}</div>
              <div class="stat-label">有效证书</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.expiring }}</div>
              <div class="stat-label">即将到期</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.expired }}</div>
              <div class="stat-label">已过期</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 证书列表 -->
    <div class="table-section">
      <el-card>
        <el-table
          :data="certificates"
          v-loading="loading"
          stripe
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="certificate_id" label="证书ID" width="120" />
          <el-table-column prop="talent_name" label="人才姓名" width="100">
            <template #default="{ row }">
              <el-link type="primary" @click="viewTalent(row.talent_id)">
                {{ row.talent_name }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="certificate_type" label="证书类型" min-width="200" />
          <el-table-column prop="specialty" label="专业" width="120" />
          <el-table-column prop="level" label="等级" width="80" />
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="expiry_date" label="到期日期" width="120">
            <template #default="{ row }">
              <span :class="{ 'text-danger': isExpiringSoon(row.expiry_date) }">
                {{ row.expiry_date || '-' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="editCertificate(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteCertificate(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 添加/编辑证书对话框 -->
    <CertificateDialog
      v-model="showAddDialog"
      :certificate="currentCertificate"
      :certificate-types="certificateTypes"
      @success="handleDialogSuccess"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { certificateAPI } from '../api'
import CertificateDialog from '../components/CertificateDialog.vue'

// 响应式数据
const loading = ref(false)
const certificates = ref([])
const certificateTypes = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const showAddDialog = ref(false)
const currentCertificate = ref(null)
const highlightCertificateId = ref(null)

// 搜索表单
const searchForm = reactive({
  certificateType: '',
  category: '',
  status: '',
  talentName: ''
})

// 人才搜索相关
const talentOptions = ref([])
const talentSearchLoading = ref(false)

// 统计数据
const stats = reactive({
  total: 0,
  valid: 0,
  expiring: 0,
  expired: 0
})

// 计算属性
const categories = computed(() => {
  const cats = new Set()
  certificateTypes.value.forEach(type => {
    if (type.category) cats.add(type.category)
  })
  return Array.from(cats)
})

// 方法
const loadCertificates = async () => {
  loading.value = true
  try {
    // 过滤掉空值参数
    const filteredParams = {}
    Object.keys(searchForm).forEach(key => {
      if (searchForm[key] && searchForm[key].trim() !== '') {
        filteredParams[key] = searchForm[key]
      }
    })

    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      ...filteredParams
    }

    const response = await certificateAPI.getList(params)
    certificates.value = response.data
    // 注意：这里需要后端返回总数，暂时使用数组长度
    total.value = response.data.length
    
    // 更新统计数据
    await updateStats()
  } catch (error) {
    ElMessage.error('加载证书列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadCertificateTypes = async () => {
  try {
    const response = await certificateAPI.getTypes()
    certificateTypes.value = response.data || []
  } catch (error) {
    ElMessage.error('加载证书类型失败')
    console.error('加载证书类型错误:', error)
    certificateTypes.value = []
  }
}

const updateStats = async () => {
  try {
    // 使用与搜索相同的参数获取统计数据
    const filteredParams = {}
    Object.keys(searchForm).forEach(key => {
      if (searchForm[key] && searchForm[key].trim() !== '') {
        filteredParams[key] = searchForm[key]
      }
    })

    const response = await certificateAPI.getStats(filteredParams)
    stats.total = response.data.total
    stats.valid = response.data.valid
    stats.expired = response.data.expired
    stats.expiring = response.data.expiring
  } catch (error) {
    console.error('获取统计数据失败:', error)
    // 如果API失败，回退到本地统计
    stats.total = certificates.value.length
    stats.valid = certificates.value.filter(cert => cert.status === 'VALID').length
    stats.expired = certificates.value.filter(cert => cert.status === 'EXPIRED').length
    stats.expiring = certificates.value.filter(cert =>
      cert.expiry_date && isExpiringSoon(cert.expiry_date)
    ).length
  }
}

const searchCertificates = () => {
  currentPage.value = 1
  loadCertificates()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    certificateType: '',
    category: '',
    status: '',
    talentName: ''
  })
  talentOptions.value = []
  searchCertificates()
}

const editCertificate = (certificate) => {
  currentCertificate.value = { ...certificate }
  showAddDialog.value = true
}

const deleteCertificate = async (certificate) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除证书 "${certificate.certificate_id}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    
    await certificateAPI.delete(certificate.certificate_id)
    ElMessage.success('删除成功')
    loadCertificates()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const handleDialogSuccess = () => {
  showAddDialog.value = false
  currentCertificate.value = null
  loadCertificates()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadCertificates()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadCertificates()
}

// 人才搜索方法
const searchTalents = async (query) => {
  if (!query) {
    talentOptions.value = []
    return
  }

  talentSearchLoading.value = true
  try {
    // 调用人才搜索API
    const response = await fetch(`/api/talents/?search=${encodeURIComponent(query)}`)
    const data = await response.json()
    talentOptions.value = data.slice(0, 10) // 限制显示前10个结果
  } catch (error) {
    console.error('搜索人才失败:', error)
    talentOptions.value = []
  } finally {
    talentSearchLoading.value = false
  }
}

const viewTalent = (talentId) => {
  // 跳转到人才详情页面
  // router.push(`/talents/${talentId}`)
}



const getStatusType = (status) => {
  const types = {
    'VALID': 'success',
    'EXPIRED': 'danger',
    'REVOKED': 'warning'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'VALID': '有效',
    'EXPIRED': '过期',
    'REVOKED': '注销'
  }
  return texts[status] || status
}

const isExpiringSoon = (expiryDate) => {
  if (!expiryDate) return false
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diffTime = expiry - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 30 && diffDays > 0
}

// 获取行样式类名（用于高亮）
const getRowClassName = ({ row }) => {
  if (highlightCertificateId.value && row.certificate_id === highlightCertificateId.value) {
    return 'highlight-row'
  }
  return ''
}

// 从URL参数获取要高亮的证书ID
const getHighlightFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const highlight = urlParams.get('highlight')
  if (highlight) {
    highlightCertificateId.value = highlight
    // 3秒后移除高亮
    setTimeout(() => {
      highlightCertificateId.value = null
    }, 3000)
  }
}

// 从URL参数获取人才名称并自动搜索
const getTalentNameFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const talentName = urlParams.get('talentName')
  if (talentName) {
    searchForm.talentName = talentName
    // 自动搜索该人才的证书
    searchTalents(talentName)
  }
}

// 生命周期
onMounted(() => {
  getHighlightFromUrl()
  getTalentNameFromUrl()
  loadCertificateTypes()
  loadCertificates()
})
</script>

<style scoped>
.certificates-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.search-section,
.stats-section,
.table-section {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.search-form .el-form-item {
  margin-bottom: 10px;
  margin-right: 15px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.text-danger {
  color: #F56C6C;
}

/* 高亮行样式 */
:deep(.highlight-row) {
  background-color: #fff7e6 !important;
  animation: highlight-fade 3s ease-out;
}

:deep(.highlight-row:hover) {
  background-color: #fff3d9 !important;
}

@keyframes highlight-fade {
  0% {
    background-color: #ffd04b !important;
  }
  100% {
    background-color: #fff7e6 !important;
  }
}
</style>
