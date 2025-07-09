<template>
  <div class="companies-page">
    <div class="page-header">
      <h2>公司管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon>
        添加公司
      </el-button>
    </div>

    <el-table :data="companies" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="公司名称" width="200" />
      <el-table-column prop="contact_info" label="联系方式" width="150" show-overflow-tooltip />
      <el-table-column prop="intention_level" label="意向等级" width="100">
        <template #default="scope">
          <el-tag :type="getIntentionType(scope.row.intention_level)">
            {{ scope.row.intention_level }}级
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="价格" width="120" />
      <el-table-column prop="certificate_requirements" label="证书需求" show-overflow-tooltip />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="editCompany(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteCompany(scope.row.id)">删除</el-button>
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
        <el-form-item label="公司名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="联系方式（可选）" prop="contact_info">
          <el-input v-model="form.contact_info" type="textarea" placeholder="请输入联系方式" />
        </el-form-item>
        <el-form-item label="沟通意向（可选）" prop="intention">
          <el-input v-model="form.intention" type="textarea" placeholder="请输入沟通意向" />
        </el-form-item>
        <el-form-item label="意向等级（可选）" prop="intention_level">
          <el-select v-model="form.intention_level" placeholder="请选择意向等级">
            <el-option label="A级-高意向" value="A" />
            <el-option label="B级-中等意向" value="B" />
            <el-option label="C级-低意向" value="C" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格（可选）" prop="price">
          <el-input v-model="form.price" placeholder="请输入价格" />
        </el-form-item>
        <el-form-item label="证书需求（可选）" prop="certificate_requirements">
          <el-input v-model="form.certificate_requirements" type="textarea" placeholder="请输入证书需求" />
        </el-form-item>
        <el-form-item label="沟通备注（可选）" prop="communication_notes">
          <el-input v-model="form.communication_notes" type="textarea" placeholder="请输入沟通备注" />
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
import { companyAPI } from '../api'

export default {
  name: 'Companies',
  setup() {
    const companies = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加公司')
    const isEdit = ref(false)
    const editId = ref(null)
    const formRef = ref()

    const form = reactive({
      name: '',
      contact_info: '',
      intention: '',
      intention_level: 'C',
      price: '',
      certificate_requirements: '',
      communication_notes: ''
    })

    const rules = {
      name: [{ required: true, message: '请输入公司名称', trigger: 'blur' }]
    }

    const getIntentionType = (level) => {
      const types = { A: 'success', B: 'warning', C: 'info' }
      return types[level] || 'info'
    }

    const loadCompanies = async () => {
      loading.value = true
      try {
        const response = await companyAPI.getList()
        companies.value = response.data.companies
      } catch (error) {
        ElMessage.error('加载公司列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      dialogTitle.value = '添加公司'
      isEdit.value = false
      resetForm()
      dialogVisible.value = true
    }

    const editCompany = (company) => {
      dialogTitle.value = '编辑公司'
      isEdit.value = true
      editId.value = company.id
      Object.assign(form, company)
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(form, {
        name: '',
        contact_info: '',
        intention: '',
        intention_level: 'C',
        price: '',
        certificate_requirements: '',
        communication_notes: ''
      })
    }

    const submitForm = async () => {
      if (!formRef.value) return

      try {
        await formRef.value.validate()

        // 处理空字符串字段，将其转换为null
        const submitData = { ...form }
        // 清理空字符串字段
        Object.keys(submitData).forEach(key => {
          if (submitData[key] === '') {
            submitData[key] = null
          }
        })

        if (isEdit.value) {
          await companyAPI.update(editId.value, submitData)
          ElMessage.success('更新成功')
        } else {
          await companyAPI.create(submitData)
          ElMessage.success('添加成功')
        }

        dialogVisible.value = false
        loadCompanies()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }

    const deleteCompany = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这个公司吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await companyAPI.delete(id)
        ElMessage.success('删除成功')
        loadCompanies()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    onMounted(() => {
      loadCompanies()
    })

    return {
      companies,
      loading,
      dialogVisible,
      dialogTitle,
      form,
      rules,
      formRef,
      getIntentionType,
      showAddDialog,
      editCompany,
      submitForm,
      deleteCompany
    }
  }
}
</script>

<style scoped>
.companies-page {
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
</style>
