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

      <!-- 证书类型搜索 -->
      <el-row :gutter="20" style="margin-top: 10px;">
        <el-col :span="6">
          <el-select
            v-model="filterCertificateType"
            placeholder="按证书类型搜索人才"
            clearable
            @change="handleCertificateTypeFilter"
            style="width: 100%"
          >
            <el-option
              v-for="type in certificateTypes"
              :key="type.type_code"
              :label="type.type_name"
              :value="type.type_name"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="filterCertificateCategory"
            placeholder="按证书大类搜索"
            clearable
            @change="handleCertificateCategoryFilter"
            style="width: 100%"
          >
            <el-option
              v-for="category in certificateCategories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <el-table :data="talents" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="wechat_note" label="微信备注" width="150" show-overflow-tooltip />

      <el-table-column prop="certificate_info" label="证书信息" width="400" show-overflow-tooltip>
        <template #default="scope">
          <div class="certificate-tags">
            <el-tag
              v-for="cert in getOptimizedCertificateTags(scope.row.id)"
              :key="cert.id"
              size="small"
              :type="cert.type"
              class="cert-tag clickable-cert-tag"
              @click="goToCertificateDetail(cert.certificate_id)"
              :title="`点击查看证书详情: ${cert.display}`"
            >
              {{ cert.display }}
            </el-tag>
            <span v-if="getOptimizedCertificateTags(scope.row.id).length === 0" class="no-certificates">
              暂无证书
            </span>
          </div>
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
      <el-table-column label="地区" width="120">
        <template #default="scope">
          <div v-if="scope.row.province || scope.row.city">
            <div style="font-size: 12px; color: #606266;">
              {{ scope.row.province }}{{ scope.row.province && scope.row.city ? ' ' : '' }}{{ scope.row.city }}
            </div>
          </div>
          <span v-else>-</span>
        </template>
      </el-table-column>

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

        <!-- 地区信息 -->
        <el-divider content-position="left">地区信息（可选）</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="省份" prop="province">
              <el-select v-model="form.province" placeholder="请选择省份" filterable>
                <el-option label="北京市" value="北京市" />
                <el-option label="天津市" value="天津市" />
                <el-option label="河北省" value="河北省" />
                <el-option label="山西省" value="山西省" />
                <el-option label="内蒙古自治区" value="内蒙古自治区" />
                <el-option label="辽宁省" value="辽宁省" />
                <el-option label="吉林省" value="吉林省" />
                <el-option label="黑龙江省" value="黑龙江省" />
                <el-option label="上海市" value="上海市" />
                <el-option label="江苏省" value="江苏省" />
                <el-option label="浙江省" value="浙江省" />
                <el-option label="安徽省" value="安徽省" />
                <el-option label="福建省" value="福建省" />
                <el-option label="江西省" value="江西省" />
                <el-option label="山东省" value="山东省" />
                <el-option label="河南省" value="河南省" />
                <el-option label="湖北省" value="湖北省" />
                <el-option label="湖南省" value="湖南省" />
                <el-option label="广东省" value="广东省" />
                <el-option label="广西壮族自治区" value="广西壮族自治区" />
                <el-option label="海南省" value="海南省" />
                <el-option label="重庆市" value="重庆市" />
                <el-option label="四川省" value="四川省" />
                <el-option label="贵州省" value="贵州省" />
                <el-option label="云南省" value="云南省" />
                <el-option label="西藏自治区" value="西藏自治区" />
                <el-option label="陕西省" value="陕西省" />
                <el-option label="甘肃省" value="甘肃省" />
                <el-option label="青海省" value="青海省" />
                <el-option label="宁夏回族自治区" value="宁夏回族自治区" />
                <el-option label="新疆维吾尔自治区" value="新疆维吾尔自治区" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="城市" prop="city">
              <el-input v-model="form.city" placeholder="请输入城市" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="详细地址" prop="address">
          <el-input v-model="form.address" type="textarea" placeholder="请输入详细地址" />
        </el-form-item>

        <el-form-item label="微信添加备注（可选）" prop="wechat_note">
          <el-input v-model="form.wechat_note" type="textarea" placeholder="例如：建造师交流群添加" />
        </el-form-item>

        <!-- 证书管理区域 -->
        <el-divider content-position="left">证书信息（可选）</el-divider>

        <!-- 关联已有证书 -->
        <el-form-item label="关联已有证书" prop="certificate_ids">
          <el-select
            v-model="form.certificate_ids"
            placeholder="搜索并选择已有证书"
            filterable
            remote
            multiple
            :remote-method="searchCertificates"
            :loading="certificateSearchLoading"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="cert in certificateOptions"
              :key="cert.certificate_id"
              :label="`${cert.certificate_type} - ${cert.certificate_name || cert.certificate_id}`"
              :value="cert.certificate_id"
            />
          </el-select>
          <div class="form-tip">搜索未关联人才的证书</div>
        </el-form-item>

        <!-- 添加新证书 -->
        <el-form-item label="添加新证书">
          <el-button type="primary" plain @click="showAddCertificateDialog">
            <el-icon><Plus /></el-icon>
            添加新证书
          </el-button>
          <div v-if="form.new_certificates.length > 0" class="new-certificates-list">
            <div class="form-tip">待添加的新证书：</div>
            <el-tag
              v-for="(cert, index) in form.new_certificates"
              :key="index"
              closable
              @close="removeNewCertificate(index)"
              style="margin: 2px 4px 2px 0;"
            >
              {{ cert.certificate_type }} - {{ cert.certificate_name }}
            </el-tag>
          </div>
        </el-form-item>

        <el-row :gutter="20">
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

    <!-- 添加新证书对话框 -->
    <el-dialog v-model="certificateDialogVisible" title="添加新证书" width="600px">
      <el-form ref="certificateFormRef" :model="certificateForm" :rules="certificateRules" label-width="120px">
        <el-form-item label="证书类型" prop="certificate_type">
          <el-select v-model="certificateForm.certificate_type" placeholder="请选择证书类型">
            <el-option label="一级建造师" value="一级建造师" />
            <el-option label="二级建造师" value="二级建造师" />
            <el-option label="一级造价工程师" value="一级造价工程师" />
            <el-option label="监理工程师" value="监理工程师" />
            <el-option label="注册建筑师" value="注册建筑师" />
            <el-option label="注册结构师" value="注册结构师" />
          </el-select>
        </el-form-item>

        <el-form-item label="证书名称" prop="certificate_name">
          <el-input v-model="certificateForm.certificate_name" placeholder="请输入证书名称" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="证书编号" prop="certificate_number">
              <el-input v-model="certificateForm.certificate_number" placeholder="请输入证书编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="等级" prop="level">
              <el-select v-model="certificateForm.level" placeholder="请选择等级">
                <el-option label="一级" value="一级" />
                <el-option label="二级" value="二级" />
                <el-option label="注册" value="注册" />
                <el-option label="高级" value="高级" />
                <el-option label="中级" value="中级" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业" prop="specialty">
              <el-input v-model="certificateForm.specialty" placeholder="请输入专业" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="颁发机构" prop="issuing_authority">
              <el-input v-model="certificateForm.issuing_authority" placeholder="请输入颁发机构" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="颁发日期" prop="issue_date">
              <el-date-picker
                v-model="certificateForm.issue_date"
                type="date"
                placeholder="选择颁发日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到期日期" prop="expiry_date">
              <el-date-picker
                v-model="certificateForm.expiry_date"
                type="date"
                placeholder="选择到期日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="状态" prop="status">
          <el-select v-model="certificateForm.status" placeholder="请选择状态">
            <el-option label="有效" value="VALID" />
            <el-option label="过期" value="EXPIRED" />
            <el-option label="暂停" value="SUSPENDED" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input v-model="certificateForm.notes" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="certificateDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addNewCertificate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { talentAPI, certificateAPI } from '../api'

export default {
  name: 'Talents',
  components: {
    Plus
  },
  setup() {
    const talents = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加人才')
    const isEdit = ref(false)
    const editId = ref(null)

    // 证书相关状态
    const certificateLoading = ref({})
    const talentCertificates = ref({})
    const certificateTypes = ref([])
    const certificateCategories = ref([])
    const filterCertificateType = ref('')
    const filterCertificateCategory = ref('')

    // 筛选相关
    const searchQuery = ref('')
    const filterCertificateLevel = ref('')
    const filterCertificateSpecialty = ref([])  // 改为数组支持多选
    const filterSocialSecurity = ref('')
    const formRef = ref()

    // 证书搜索相关
    const certificateOptions = ref([])
    const certificateSearchLoading = ref(false)

    // 新证书对话框相关
    const certificateDialogVisible = ref(false)
    const certificateFormRef = ref()

    const form = reactive({
      name: '',
      gender: '',
      age: null,
      phone: '',
      wechat_note: '',
      contract_price: null,
      intention_level: 'C',
      communication_content: '',
      social_security_status: '',
      province: '',
      city: '',
      address: '',
      certificate_ids: [],  // 关联的证书ID数组
      new_certificates: []   // 新添加的证书数组
    })

    const certificateForm = reactive({
      certificate_type: '',
      certificate_name: '',
      certificate_number: '',
      level: '',
      specialty: '',
      issuing_authority: '',
      issue_date: '',
      expiry_date: '',
      status: 'VALID',
      notes: ''
    })

    const rules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
    }

    const certificateRules = {
      certificate_type: [{ required: true, message: '请选择证书类型', trigger: 'change' }],
      certificate_name: [{ required: true, message: '请输入证书名称', trigger: 'blur' }],
      status: [{ required: true, message: '请选择状态', trigger: 'change' }]
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
      filterCertificateType.value = ''
      filterCertificateCategory.value = ''
      loadTalents()
    }

    // 加载证书类型
    const loadCertificateTypes = async () => {
      try {
        const response = await certificateAPI.getTypes()
        certificateTypes.value = response.data

        // 提取证书大类
        const categories = new Set()
        response.data.forEach(type => {
          if (type.category) categories.add(type.category)
        })
        certificateCategories.value = Array.from(categories)
      } catch (error) {
        console.error('加载证书类型失败:', error)
      }
    }

    // 按证书类型搜索人才
    const handleCertificateTypeFilter = async () => {
      if (!filterCertificateType.value) {
        loadTalents()
        return
      }

      loading.value = true
      try {
        const response = await certificateAPI.searchByType(filterCertificateType.value)
        const talentIds = response.data.map(item => item.talent_id)

        // 根据搜索到的人才ID过滤人才列表
        const allTalentsResponse = await talentAPI.getList()
        talents.value = allTalentsResponse.data.talents.filter(talent =>
          talentIds.includes(talent.id)
        )
      } catch (error) {
        ElMessage.error('搜索失败')
        console.error(error)
      } finally {
        loading.value = false
      }
    }

    // 按证书大类搜索人才
    const handleCertificateCategoryFilter = async () => {
      if (!filterCertificateCategory.value) {
        loadTalents()
        return
      }

      loading.value = true
      try {
        const response = await certificateAPI.searchByCategory(filterCertificateCategory.value)
        const talentIds = response.data.map(item => item.talent_id)

        // 根据搜索到的人才ID过滤人才列表
        const allTalentsResponse = await talentAPI.getList()
        talents.value = allTalentsResponse.data.talents.filter(talent =>
          talentIds.includes(talent.id)
        )
      } catch (error) {
        ElMessage.error('搜索失败')
        console.error(error)
      } finally {
        loading.value = false
      }
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

        // 为每个人才加载证书信息
        await loadTalentsCertificates()
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

    // 批量加载人才证书信息
    const loadTalentsCertificates = async () => {
      const promises = talents.value.map(async (talent) => {
        try {
          const response = await certificateAPI.getTalentCertificates(talent.id)
          talentCertificates.value[talent.id] = response.data
        } catch (error) {
          console.error(`Error loading certificates for talent ${talent.id}:`, error)
          talentCertificates.value[talent.id] = []
        }
      })

      await Promise.all(promises)
    }

    // 获取人才的证书名称信息
    const getTalentCertificateNames = (talentId) => {
      const certificates = talentCertificates.value[talentId] || []
      if (certificates.length === 0) return '-'

      const names = [...new Set(certificates.map(cert => cert.certificate_name || cert.certificate_type).filter(name => name))]
      return names.length > 0 ? names.slice(0, 3).join(', ') + (names.length > 3 ? '...' : '') : '-'
    }

    // 获取人才的证书标签信息（去重后的前5个证书的名称和专业）
    const getTalentCertificateTags = (talentId) => {
      const certificates = talentCertificates.value[talentId] || []
      if (certificates.length === 0) return []

      const tags = []
      const seenNames = new Set()
      const seenSpecialties = new Set()

      // 去重处理：相同名称的证书只显示一次
      const uniqueCerts = []
      const certNames = new Set()

      certificates.forEach(cert => {
        const certName = cert.certificate_name || cert.certificate_type
        if (certName && !certNames.has(certName)) {
          certNames.add(certName)
          uniqueCerts.push(cert)
        }
      })

      // 取前5个不重复的证书
      const displayedCerts = uniqueCerts.slice(0, 5)

      displayedCerts.forEach((cert, index) => {
        // 证书名称标签
        const certName = cert.certificate_name || cert.certificate_type
        if (certName && !seenNames.has(certName)) {
          seenNames.add(certName)
          tags.push({
            id: `name-${cert.certificate_id}-${index}`,
            display: certName,
            type: 'primary'
          })
        }

        // 证书专业标签（也去重）
        if (cert.specialty && !seenSpecialties.has(cert.specialty)) {
          seenSpecialties.add(cert.specialty)
          tags.push({
            id: `specialty-${cert.certificate_id}-${index}`,
            display: cert.specialty,
            type: 'success'
          })
        }
      })

      return tags
    }

    // 获取优化后的证书标签信息（证书类型 + 专业 + 等级）
    const getOptimizedCertificateTags = (talentId) => {
      const certificates = talentCertificates.value[talentId] || []
      if (certificates.length === 0) return []

      const tags = []
      const seenCombinations = new Set()

      // 去重处理：相同证书类型只显示一次
      const uniqueCerts = []
      const certTypes = new Set()

      certificates.forEach(cert => {
        if (cert.certificate_type && !certTypes.has(cert.certificate_type)) {
          certTypes.add(cert.certificate_type)
          uniqueCerts.push(cert)
        }
      })

      // 取前5个不重复的证书
      const displayedCerts = uniqueCerts.slice(0, 5)

      displayedCerts.forEach((cert, index) => {
        // 证书类型标签（主要信息）
        if (cert.certificate_type) {
          tags.push({
            id: `type-${cert.certificate_id}-${index}`,
            certificate_id: cert.certificate_id,
            display: cert.certificate_type,
            type: 'primary'
          })
        }

        // 专业标签（如果有且不重复）
        if (cert.specialty) {
          const specialtyKey = cert.specialty
          if (!seenCombinations.has(specialtyKey)) {
            seenCombinations.add(specialtyKey)
            tags.push({
              id: `specialty-${cert.certificate_id}-${index}`,
              certificate_id: cert.certificate_id,
              display: cert.specialty,
              type: 'success'
            })
          }
        }

        // 等级标签（如果有且值得显示）
        if (cert.level && cert.level !== '一级' && cert.level !== cert.certificate_type) {
          tags.push({
            id: `level-${cert.certificate_id}-${index}`,
            certificate_id: cert.certificate_id,
            display: cert.level,
            type: 'warning'
          })
        }
      })

      return tags
    }

    // 获取人才的证书类型信息
    const getTalentCertificateTypes = (talentId) => {
      const certificates = talentCertificates.value[talentId] || []
      if (certificates.length === 0) return []

      return [...new Set(certificates.map(cert => cert.certificate_type).filter(type => type))]
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
        contract_price: null,
        intention_level: 'C',
        communication_content: '',
        social_security_status: '',
        province: '',
        city: '',
        address: '',
        certificate_ids: [],
        new_certificates: []
      })
      // 清空证书搜索选项
      certificateOptions.value = []
    }

    // 新证书相关方法
    const showAddCertificateDialog = () => {
      resetCertificateForm()
      certificateDialogVisible.value = true
    }

    const resetCertificateForm = () => {
      Object.assign(certificateForm, {
        certificate_type: '',
        certificate_name: '',
        certificate_number: '',
        level: '',
        specialty: '',
        issuing_authority: '',
        issue_date: '',
        expiry_date: '',
        status: 'VALID',
        notes: ''
      })
    }

    const addNewCertificate = async () => {
      if (!certificateFormRef.value) return

      try {
        await certificateFormRef.value.validate()

        // 添加到新证书列表
        form.new_certificates.push({ ...certificateForm })

        // 关闭对话框并重置表单
        certificateDialogVisible.value = false
        resetCertificateForm()

        ElMessage.success('证书添加成功')
      } catch (error) {
        console.error('证书表单验证失败:', error)
      }
    }

    const removeNewCertificate = (index) => {
      form.new_certificates.splice(index, 1)
    }

    // 跳转到证书详情
    const goToCertificateDetail = (certificateId) => {
      if (certificateId) {
        // 跳转到证书管理页面并高亮显示指定证书
        window.open(`/certificates?highlight=${certificateId}`, '_blank')
      }
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

        let talentId = editId.value

        if (isEdit.value) {
          await talentAPI.update(editId.value, submitData)
          ElMessage.success('更新成功')
        } else {
          const response = await talentAPI.create(submitData)
          talentId = response.data.id
          console.log('创建成功:', response.data)
          ElMessage.success('添加成功')
        }

        // 处理证书关联
        if (form.certificate_ids && form.certificate_ids.length > 0) {
          try {
            for (const certificateId of form.certificate_ids) {
              await fetch(`http://localhost:8000/api/certificates/${certificateId}`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  talent_id: talentId
                })
              })
            }
            console.log(`成功关联 ${form.certificate_ids.length} 个已有证书`)
          } catch (error) {
            console.error('关联证书失败:', error)
            ElMessage.warning('人才创建成功，但证书关联失败')
          }
        }

        // 处理新证书创建
        if (form.new_certificates && form.new_certificates.length > 0) {
          try {
            for (const cert of form.new_certificates) {
              const certificateData = {
                ...cert,
                talent_id: talentId
              }

              await fetch('http://localhost:8000/api/certificates/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(certificateData)
              })
            }
            console.log(`成功创建 ${form.new_certificates.length} 个新证书`)
          } catch (error) {
            console.error('创建新证书失败:', error)
            ElMessage.warning('人才创建成功，但新证书创建失败')
          }
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

    // 证书搜索方法
    const searchCertificates = async (query) => {
      if (!query) {
        certificateOptions.value = []
        return
      }

      certificateSearchLoading.value = true
      try {
        // 搜索未关联人才的证书
        const response = await fetch(`http://localhost:8000/api/certificates/?search=${encodeURIComponent(query)}`)
        const data = await response.json()

        // 过滤出未关联人才的证书
        certificateOptions.value = data.filter(cert => !cert.talent_id)
      } catch (error) {
        console.error('搜索证书失败:', error)
        ElMessage.error('搜索证书失败')
      } finally {
        certificateSearchLoading.value = false
      }
    }



    onMounted(() => {
      loadTalents()
      loadCertificateTypes()
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
      clearFilters,
      // 证书相关
      certificateLoading,
      certificateTypes,
      certificateCategories,
      filterCertificateType,
      filterCertificateCategory,
      handleCertificateTypeFilter,
      handleCertificateCategoryFilter,
      // 证书搜索相关
      certificateOptions,
      certificateSearchLoading,
      searchCertificates,
      // 新证书对话框相关
      certificateDialogVisible,
      certificateForm,
      certificateRules,
      certificateFormRef,
      showAddCertificateDialog,
      addNewCertificate,
      removeNewCertificate,
      goToCertificateDetail,
      // 证书显示函数
      getTalentCertificateNames,
      getTalentCertificateTags,
      getOptimizedCertificateTags,
      getTalentCertificateTypes
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

.certificate-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-height: 80px;
  overflow: hidden;
  line-height: 1.2;
}

.cert-tag {
  margin: 2px 0;
  font-size: 12px;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.new-certificates-list {
  margin-top: 8px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.new-certificates-list .form-tip {
  margin-bottom: 8px;
  margin-top: 0;
}

.clickable-cert-tag {
  cursor: pointer;
  transition: all 0.3s ease;
}

.clickable-cert-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 0.8;
}
</style>
