<template>
  <div class="page-card">
    <div class="page-title">模型结构管理</div>
    
    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索模型名称或类型" style="width: 200px" @keyup.enter="loadData" />
      <el-button type="primary" @click="loadData">查询</el-button>
      <el-button type="success" @click="openDialog()">新增模型</el-button>
    </div>

    <el-table :data="tableData" stripe border>
      <el-table-column prop="model_code" label="模型编码" width="150" />
      <el-table-column prop="model_name" label="模型名称" min-width="150" />
      <el-table-column prop="model_type" label="模型类型" width="100" />
      <el-table-column prop="algorithm" label="算法" width="120" />
      <el-table-column prop="owner" label="负责人" width="100" />
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="table-pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadData"
      />
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑模型' : '新增模型'" width="550px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="模型编码" prop="model_code">
          <el-input v-model="form.model_code" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="模型名称" prop="model_name">
          <el-input v-model="form.model_name" />
        </el-form-item>
        <el-form-item label="模型类型" prop="model_type">
          <el-select v-model="form.model_type" placeholder="请选择" style="width: 100%">
            <el-option label="分类" value="分类" />
            <el-option label="回归" value="回归" />
            <el-option label="聚类" value="聚类" />
            <el-option label="推荐" value="推荐" />
          </el-select>
        </el-form-item>
        <el-form-item label="算法" prop="algorithm">
          <el-input v-model="form.algorithm" placeholder="如：随机森林、XGBoost" />
        </el-form-item>
        <el-form-item label="负责人" prop="owner">
          <el-input v-model="form.owner" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modelsApi } from '../api'

const tableData = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const search = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const editingId = ref(null)

const form = reactive({
  model_code: '', model_name: '', model_type: '', algorithm: '', owner: '', description: ''
})

const rules = {
  model_code: [{ required: true, message: '请输入模型编码', trigger: 'blur' }],
  model_name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }]
}

async function loadData() {
  try {
    const res = await modelsApi.list({ page: page.value, page_size: pageSize.value, search: search.value })
    tableData.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    ElMessage.error(e.message)
  }
}

function openDialog(row) {
  if (row) {
    isEdit.value = true
    editingId.value = row.id
    Object.assign(form, row)
  } else {
    isEdit.value = false
    editingId.value = null
    Object.assign(form, { model_code: '', model_name: '', model_type: '', algorithm: '', owner: '', description: '' })
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  try {
    if (isEdit.value) {
      await modelsApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await modelsApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除模型「${row.model_name}」吗？`, '删除确认', { type: 'warning' })
    await modelsApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message)
  }
}

loadData()
</script>
