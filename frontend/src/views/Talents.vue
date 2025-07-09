<template>
  <div class="talents-page">
    <div class="page-header">
      <h2>人才管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon>
        添加人才
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchQuery"
            placeholder="搜索姓名、电话、证书信息..."
            prefix-icon="Search"
            @input="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterCertificateLevel" placeholder="证书等级" @change="handleFilter">
            <el-option label="全部等级" value="" />
            <el-option label="一级建造师" value="一级" />
            <el-option label="二级建造师" value="二级" />
            <el-option label="初级工程师" value="初级工程师" />
            <el-option label="中级工程师" value="中级工程师" />
            <el-option label="高级工程师" value="高级工程师" />
            <el-option label="三类人员A类" value="三类人员A类" />
            <el-option label="三类人员B类" value="三类人员B类" />
            <el-option label="三类人员C类" value="三类人员C类" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-col>
        <el-col :span="5">
          <el-select
            v-model="filterCertificateSpecialty"
            placeholder="证书专业"
            multiple
            collapse-tags
            collapse-tags-tooltip
            @change="handleFilter">
            <el-option-group label="建造师专业">
              <el-option label="建筑工程" value="建筑工程" />
              <el-option label="市政公用工程" value="市政公用工程" />
              <el-option label="机电工程" value="机电工程" />
              <el-option label="公路工程" value="公路工程" />
              <el-option label="水利水电工程" value="水利水电工程" />
              <el-option label="矿业工程" value="矿业工程" />
              <el-option label="铁路工程" value="铁路工程" />
              <el-option label="民航机场工程" value="民航机场工程" />
              <el-option label="港口与航道工程" value="港口与航道工程" />
              <el-option label="通信与广电工程" value="通信与广电工程" />
            </el-option-group>
            <el-option-group label="工程师专业">
              <el-option label="建筑工程师" value="建筑工程师" />
              <el-option label="结构工程师" value="结构工程师" />
              <el-option label="电气工程师" value="电气工程师" />
              <el-option label="给排水工程师" value="给排水工程师" />
              <el-option label="暖通工程师" value="暖通工程师" />
              <el-option label="建筑设计工程师" value="建筑设计工程师" />
              <el-option label="工程造价工程师" value="工程造价工程师" />
              <el-option label="测绘工程师" value="测绘工程师" />
              <el-option label="岩土工程师" value="岩土工程师" />
              <el-option label="建筑材料工程师" value="建筑材料工程师" />
            </el-option-group>
            <el-option-group label="三类人员">
              <el-option label="安全管理" value="安全管理" />
            </el-option-group>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterSocialSecurity" placeholder="社保情况" @change="handleFilter">
            <el-option label="全部" value="" />
            <el-option label="唯一社保" value="唯一社保" />
            <el-option label="无社保" value="无社保" />
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-button @click="clearFilters">清空筛选</el-button>
        </el-col>
      </el-row>
    </div>

    <el-table :data="talents" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="wechat_note" label="微信备注" width="150" show-overflow-tooltip />
      <el-table-column prop="certificate_level" label="证书等级" width="100">
        <template #default="scope">
          <el-tag v-if="scope.row.certificate_level" size="small">
            {{ scope.row.certificate_level }}
          </el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="certificate_specialty" label="证书专业" width="120" show-overflow-tooltip>
        <template #default="scope">
          {{ scope.row.certificate_specialty || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="social_security_status" label="社保情况" width="100">
        <template #default="scope">
          <el-tag v-if="scope.row.social_security_status"
                  :type="scope.row.social_security_status === '唯一社保' ? 'success' : 'warning'"
                  size="small">
            {{ scope.row.social_security_status }}
          </el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="certificate_info" label="证书信息" width="150" show-overflow-tooltip />
      <el-table-column prop="certificate_expiry_date" label="证书到期" width="120" />
      <el-table-column prop="contract_price" label="合同价格" width="120">
        <template #default="scope">
          {{ scope.row.contract_price ? `¥${scope.row.contract_price}` : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="intention_level" label="意向等级" width="100">
        <template #default="scope">
          <el-tag :type="getIntentionType(scope.row.intention_level)">
            {{ scope.row.intention_level }}级
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editTalent(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteTalent(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" placeholder="请选择">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="18" :max="70" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电话（可选）" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入电话号码" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="微信添加备注（可选）" prop="wechat_note">
          <el-input v-model="form.wechat_note" type="textarea" placeholder="例如：建造师交流群添加" />
        </el-form-item>

        <el-form-item label="证书信息（可选）" prop="certificate_info">
          <el-input v-model="form.certificate_info" type="textarea" placeholder="例如：一级建造师-建筑工程" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书等级（可选）" prop="certificate_level">
              <el-select v-model="form.certificate_level" placeholder="请选择证书等级">
                <el-option-group label="建造师">
                  <el-option label="一级建造师" value="一级" />
                  <el-option label="二级建造师" value="二级" />
                </el-option-group>
                <el-option-group label="工程师">
                  <el-option label="初级工程师" value="初级工程师" />
                  <el-option label="中级工程师" value="中级工程师" />
                  <el-option label="高级工程师" value="高级工程师" />
                </el-option-group>
                <el-option-group label="三类人员">
                  <el-option label="A类-企业主要负责人" value="三类人员A类" />
                  <el-option label="B类-项目负责人" value="三类人员B类" />
                  <el-option label="C类-专职安全员" value="三类人员C类" />
                </el-option-group>
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="证书专业（可选）" prop="certificate_specialty">
              <el-select v-model="form.certificate_specialty" placeholder="请选择证书专业">
                <el-option-group label="建造师专业">
                  <el-option label="建筑工程" value="建筑工程" />
                  <el-option label="市政公用工程" value="市政公用工程" />
                  <el-option label="机电工程" value="机电工程" />
                  <el-option label="公路工程" value="公路工程" />
                  <el-option label="水利水电工程" value="水利水电工程" />
                  <el-option label="矿业工程" value="矿业工程" />
                  <el-option label="铁路工程" value="铁路工程" />
                  <el-option label="民航机场工程" value="民航机场工程" />
                  <el-option label="港口与航道工程" value="港口与航道工程" />
                  <el-option label="通信与广电工程" value="通信与广电工程" />
                </el-option-group>
                <el-option-group label="工程师专业">
                  <el-option label="建筑工程师" value="建筑工程师" />
                  <el-option label="结构工程师" value="结构工程师" />
                  <el-option label="电气工程师" value="电气工程师" />
                  <el-option label="给排水工程师" value="给排水工程师" />
                  <el-option label="暖通工程师" value="暖通工程师" />
                  <el-option label="建筑设计工程师" value="建筑设计工程师" />
                  <el-option label="工程造价工程师" value="工程造价工程师" />
                  <el-option label="测绘工程师" value="测绘工程师" />
                  <el-option label="岩土工程师" value="岩土工程师" />
                  <el-option label="建筑材料工程师" value="建筑材料工程师" />
                </el-option-group>
                <el-option-group label="三类人员">
                  <el-option label="安全管理" value="安全管理" />
                </el-option-group>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书到期日期（可选）" prop="certificate_expiry_date">
              <el-date-picker
                v-model="form.certificate_expiry_date"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同价格（可选）" prop="contract_price">
              <el-input-number v-model="form.contract_price" :precision="2" :step="1000" placeholder="请输入价格" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="意向等级（可选）" prop="intention_level">
              <el-select v-model="form.intention_level" placeholder="请选择意向等级">
                <el-option label="A级-高意向" value="A" />
                <el-option label="B级-中等意向" value="B" />
                <el-option label="C级-低意向" value="C" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="社保情况（可选）" prop="social_security_status">
              <el-select v-model="form.social_security_status" placeholder="请选择社保情况">
                <el-option label="唯一社保" value="唯一社保" />
                <el-option label="无社保" value="无社保" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="沟通内容（可选）" prop="communication_content">
          <el-input v-model="form.communication_content" type="textarea" placeholder="请输入沟通记录" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { talentAPI } from '../api'

export default {
  name: 'Talents',
  setup() {
    const talents = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加人才')
    const isEdit = ref(false)
    const editId = ref(null)

    // 筛选相关
    const searchQuery = ref('')
    const filterCertificateLevel = ref('')
    const filterCertificateSpecialty = ref([])  // 改为数组支持多选
    const filterSocialSecurity = ref('')
    const formRef = ref()

    const form = reactive({
      name: '',
      gender: '',
      age: null,
      phone: '',
      wechat_note: '',
      certificate_info: '',
      certificate_expiry_date: '',
      contract_price: null,
      intention_level: 'C',
      communication_content: '',
      certificate_level: '',
      certificate_specialty: '',
      social_security_status: ''
    })

    const rules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
    }

    const getIntentionType = (level) => {
      const types = { A: 'success', B: 'warning', C: 'info' }
      return types[level] || 'info'
    }

    // 筛选相关方法
    const handleSearch = () => {
      loadTalents()
    }

    const handleFilter = () => {
      loadTalents()
    }

    const clearFilters = () => {
      searchQuery.value = ''
      filterCertificateLevel.value = ''
      filterCertificateSpecialty.value = []  // 清空数组
      filterSocialSecurity.value = ''
      loadTalents()
    }

    const loadTalents = async (retryCount = 0) => {
      loading.value = true
      try {
        const params = {}
        if (searchQuery.value) params.search = searchQuery.value
        if (filterCertificateLevel.value) params.certificate_level = filterCertificateLevel.value
        if (filterCertificateSpecialty.value.length > 0) {
          // 多选专业，后端需要支持数组或逗号分隔
          params.certificate_specialty = filterCertificateSpecialty.value.join(',')
        }
        if (filterSocialSecurity.value) params.social_security_status = filterSocialSecurity.value

        const response = await talentAPI.getList(params)
        talents.value = response.data.talents
        console.log(`成功加载 ${talents.value.length} 个人才`)
      } catch (error) {
        console.error('加载人才列表失败:', error)

        // 重试机制
        if (retryCount < 2) {
          console.log(`重试加载人才列表 (${retryCount + 1}/2)`)
          setTimeout(() => {
            loadTalents(retryCount + 1)
          }, 1000)
          return
        }

        ElMessage.error(`加载人才列表失败: ${error.response?.data?.detail || error.message}`)
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      dialogTitle.value = '添加人才'
      isEdit.value = false
      resetForm()
      dialogVisible.value = true
    }

    const editTalent = (talent) => {
      dialogTitle.value = '编辑人才'
      isEdit.value = true
      editId.value = talent.id
      Object.assign(form, talent)
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(form, {
        name: '',
        gender: '',
        age: null,
        phone: '',
        wechat_note: '',
        certificate_info: '',
        certificate_expiry_date: '',
        contract_price: null,
        intention_level: 'C'
      })
    }

    const submitForm = async () => {
      if (!formRef.value) return

      try {
        await formRef.value.validate()

        // 处理空字符串字段，将其转换为null
        const submitData = { ...form }
        if (submitData.certificate_expiry_date === '') {
          submitData.certificate_expiry_date = null
        }
        if (submitData.contract_price === '') {
          submitData.contract_price = null
        }
        if (submitData.age === '') {
          submitData.age = null
        }

        if (isEdit.value) {
          await talentAPI.update(editId.value, submitData)
          ElMessage.success('更新成功')
        } else {
          const response = await talentAPI.create(submitData)
          console.log('创建成功:', response.data)
          ElMessage.success('添加成功')
        }

        dialogVisible.value = false
        // 延迟刷新，确保数据已保存
        setTimeout(() => {
          loadTalents()
        }, 500)
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error(`操作失败: ${error.response?.data?.detail || error.message}`)
      }
    }

    const deleteTalent = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这个人才吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await talentAPI.delete(id)
        ElMessage.success('删除成功')
        loadTalents()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    onMounted(() => {
      loadTalents()
    })

    return {
      talents,
      loading,
      dialogVisible,
      dialogTitle,
      form,
      rules,
      formRef,
      searchQuery,
      filterCertificateLevel,
      filterCertificateSpecialty,
      filterSocialSecurity,
      getIntentionType,
      showAddDialog,
      editTalent,
      submitForm,
      deleteTalent,
      handleSearch,
      handleFilter,
      clearFilters
    }
  }
}
</script>

<style scoped>
.talents-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.filter-section .el-select {
  width: 100%;
}
</style>
