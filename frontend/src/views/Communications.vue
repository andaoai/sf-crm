<template>
  <div class="communications-page">
    <div class="page-header">
      <h2>沟通记录</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon>
        添加记录
      </el-button>
    </div>

    <div class="filter-bar">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="筛选类型">
          <el-select v-model="filterForm.type" @change="loadCommunications">
            <el-option label="全部" value="" />
            <el-option label="公司相关" value="company" />
            <el-option label="人才相关" value="talent" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="communications" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column label="类型" width="100">
        <template #default="scope">
          <el-tag v-if="scope.row.company_id" type="primary">公司</el-tag>
          <el-tag v-if="scope.row.talent_id" type="success">人才</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="沟通内容" width="300" show-overflow-tooltip />
      <el-table-column prop="result" label="沟通结果" width="200" show-overflow-tooltip />
      <el-table-column prop="communication_time" label="沟通时间" width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.communication_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editCommunication(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteCommunication(scope.row.id)">删除</el-button>
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
        <el-form-item label="关联类型" prop="type">
          <el-radio-group v-model="form.type" @change="handleTypeChange">
            <el-radio label="company">公司</el-radio>
            <el-radio label="talent">人才</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="form.type === 'company'" label="选择公司" prop="company_id">
          <el-select v-model="form.company_id" placeholder="请选择公司" filterable>
            <el-option
              v-for="company in companies"
              :key="company.id"
              :label="company.name"
              :value="company.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item v-if="form.type === 'talent'" label="选择人才" prop="talent_id">
          <el-select v-model="form.talent_id" placeholder="请选择人才" filterable>
            <el-option
              v-for="talent in talents"
              :key="talent.id"
              :label="talent.name"
              :value="talent.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="沟通内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="4" />
        </el-form-item>

        <el-form-item label="沟通结果" prop="result">
          <el-input v-model="form.result" type="textarea" :rows="3" />
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
import { communicationAPI, companyAPI, talentAPI } from '../api'

export default {
  name: 'Communications',
  setup() {
    const communications = ref([])
    const companies = ref([])
    const talents = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加沟通记录')
    const isEdit = ref(false)
    const editId = ref(null)
    const formRef = ref()

    const filterForm = reactive({
      type: ''
    })

    const form = reactive({
      type: 'company',
      company_id: null,
      talent_id: null,
      content: '',
      result: ''
    })

    const rules = {
      content: [{ required: true, message: '请输入沟通内容', trigger: 'blur' }]
    }

    const formatDateTime = (dateTime) => {
      return new Date(dateTime).toLocaleString('zh-CN')
    }

    const loadCommunications = async () => {
      loading.value = true
      try {
        const params = {}
        if (filterForm.type === 'company') {
          params.company_id = 1 // 这里应该根据实际需求调整
        } else if (filterForm.type === 'talent') {
          params.talent_id = 1 // 这里应该根据实际需求调整
        }
        
        const response = await communicationAPI.getList(params)
        communications.value = response.data.communications
      } catch (error) {
        ElMessage.error('加载沟通记录失败')
      } finally {
        loading.value = false
      }
    }

    const loadCompanies = async () => {
      try {
        const response = await companyAPI.getList()
        companies.value = response.data.companies
      } catch (error) {
        console.error('加载公司列表失败')
      }
    }

    const loadTalents = async () => {
      try {
        const response = await talentAPI.getList()
        talents.value = response.data.talents
      } catch (error) {
        console.error('加载人才列表失败')
      }
    }

    const showAddDialog = () => {
      dialogTitle.value = '添加沟通记录'
      isEdit.value = false
      resetForm()
      dialogVisible.value = true
    }

    const editCommunication = (communication) => {
      dialogTitle.value = '编辑沟通记录'
      isEdit.value = true
      editId.value = communication.id
      
      form.content = communication.content
      form.result = communication.result
      
      if (communication.company_id) {
        form.type = 'company'
        form.company_id = communication.company_id
        form.talent_id = null
      } else if (communication.talent_id) {
        form.type = 'talent'
        form.talent_id = communication.talent_id
        form.company_id = null
      }
      
      dialogVisible.value = true
    }

    const handleTypeChange = () => {
      form.company_id = null
      form.talent_id = null
    }

    const resetForm = () => {
      Object.assign(form, {
        type: 'company',
        company_id: null,
        talent_id: null,
        content: '',
        result: ''
      })
    }

    const submitForm = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        
        const submitData = {
          content: form.content,
          result: form.result,
          company_id: form.type === 'company' ? form.company_id : null,
          talent_id: form.type === 'talent' ? form.talent_id : null
        }
        
        if (isEdit.value) {
          await communicationAPI.update(editId.value, submitData)
          ElMessage.success('更新成功')
        } else {
          await communicationAPI.create(submitData)
          ElMessage.success('添加成功')
        }
        
        dialogVisible.value = false
        loadCommunications()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }

    const deleteCommunication = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这条沟通记录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await communicationAPI.delete(id)
        ElMessage.success('删除成功')
        loadCommunications()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    onMounted(() => {
      loadCommunications()
      loadCompanies()
      loadTalents()
    })

    return {
      communications,
      companies,
      talents,
      loading,
      dialogVisible,
      dialogTitle,
      filterForm,
      form,
      rules,
      formRef,
      formatDateTime,
      loadCommunications,
      showAddDialog,
      editCommunication,
      handleTypeChange,
      submitForm,
      deleteCommunication
    }
  }
}
</script>

<style scoped>
.communications-page {
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

.filter-bar {
  margin-bottom: 20px;
}
</style>
