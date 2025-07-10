<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑证书' : '添加证书'"
    width="600px"
    @update:model-value="$emit('update:modelValue', $event)"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="人才" prop="talent_id">
        <el-select
          v-model="form.talent_id"
          placeholder="选择人才"
          filterable
          remote
          :remote-method="searchTalents"
          :loading="talentLoading"
          style="width: 100%"
        >
          <el-option
            v-for="talent in talents"
            :key="talent.id"
            :label="`${talent.name} (${talent.phone || '无电话'})`"
            :value="talent.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="证书类型" prop="certificate_type">
        <el-select
          v-model="form.certificate_type"
          placeholder="选择证书类型"
          style="width: 100%"
        >
          <el-option
            v-for="type in certificateTypes"
            :key="type.type_code"
            :label="type.type_name"
            :value="type.type_name"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="证书名称" prop="certificate_name">
        <el-input
          v-model="form.certificate_name"
          placeholder="请输入证书名称"
        />
      </el-form-item>

      <el-form-item label="证书编号" prop="certificate_number">
        <el-input
          v-model="form.certificate_number"
          placeholder="请输入证书编号"
        />
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="颁发日期" prop="issue_date">
            <el-date-picker
              v-model="form.issue_date"
              type="date"
              placeholder="选择颁发日期"
              style="width: 100%"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="到期日期" prop="expiry_date">
            <el-date-picker
              v-model="form.expiry_date"
              type="date"
              placeholder="选择到期日期"
              style="width: 100%"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="发证机构" prop="issuing_authority">
        <el-input
          v-model="form.issuing_authority"
          placeholder="请输入发证机构"
        />
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="专业方向" prop="specialty">
            <el-input
              v-model="form.specialty"
              placeholder="请输入专业方向"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="等级" prop="level">
            <el-select
              v-model="form.level"
              placeholder="选择等级"
              style="width: 100%"
            >
              <el-option label="一级" value="一级" />
              <el-option label="二级" value="二级" />
              <el-option label="三级" value="三级" />
              <el-option label="初级" value="初级" />
              <el-option label="中级" value="中级" />
              <el-option label="高级" value="高级" />
              <el-option label="注册级" value="注册级" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="证书状态" prop="status">
        <el-select
          v-model="form.status"
          placeholder="选择状态"
          style="width: 100%"
        >
          <el-option label="有效" value="VALID" />
          <el-option label="过期" value="EXPIRED" />
          <el-option label="注销" value="REVOKED" />
        </el-select>
      </el-form-item>

      <el-form-item label="备注" prop="notes">
        <el-input
          v-model="form.notes"
          type="textarea"
          :rows="3"
          placeholder="请输入备注信息"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { certificateAPI, talentAPI } from '../api'

// Props
const props = defineProps({
  modelValue: Boolean,
  certificate: Object,
  certificateTypes: Array
})

// Emits
const emit = defineEmits(['update:modelValue', 'success'])

// 响应式数据
const formRef = ref()
const submitting = ref(false)
const talentLoading = ref(false)
const talents = ref([])

// 表单数据
const form = reactive({
  talent_id: null,
  certificate_type: '',
  certificate_name: '',
  certificate_number: '',
  issue_date: '',
  expiry_date: '',
  issuing_authority: '',
  specialty: '',
  level: '',
  status: 'VALID',
  notes: ''
})

// 表单验证规则
const rules = {
  certificate_type: [
    { required: true, message: '请选择证书类型', trigger: 'change' }
  ]
}

// 计算属性
const isEdit = computed(() => !!props.certificate?.certificate_id)

// 监听器
watch(() => props.certificate, (newVal) => {
  if (newVal) {
    Object.assign(form, newVal)
    // 如果是编辑模式，加载对应的人才信息
    if (newVal.talent_id) {
      loadTalentById(newVal.talent_id)
    }
  }
}, { immediate: true })

watch(() => props.modelValue, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})

// 方法
const searchTalents = async (query) => {
  if (!query) return
  
  talentLoading.value = true
  try {
    const response = await talentAPI.getList({ 
      search: query,
      limit: 20 
    })
    talents.value = response.data.talents || response.data
  } catch (error) {
    console.error('搜索人才失败:', error)
  } finally {
    talentLoading.value = false
  }
}

const loadTalentById = async (talentId) => {
  try {
    const response = await talentAPI.getById(talentId)
    const talent = response.data
    if (talent && !talents.value.find(t => t.id === talent.id)) {
      talents.value.push(talent)
    }
  } catch (error) {
    console.error('加载人才信息失败:', error)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    submitting.value = true
    
    if (isEdit.value) {
      await certificateAPI.update(form.certificate_id, form)
      ElMessage.success('证书更新成功')
    } else {
      await certificateAPI.create(form)
      ElMessage.success('证书创建成功')
    }
    
    emit('success')
  } catch (error) {
    if (error.response) {
      ElMessage.error(error.response.data.detail || '操作失败')
    } else {
      console.error('提交失败:', error)
    }
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}

const resetForm = () => {
  Object.assign(form, {
    talent_id: null,
    certificate_type: '',
    certificate_name: '',
    certificate_number: '',
    issue_date: '',
    expiry_date: '',
    issuing_authority: '',
    specialty: '',
    level: '',
    status: 'VALID',
    notes: ''
  })
  talents.value = []
  formRef.value?.resetFields()
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
