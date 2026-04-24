<template>
  <div class="page-card">
    <div class="page-title">元数据管理</div>
    
    <div class="search-bar">
      <el-select v-model="filters.meta_type" placeholder="元数据类型" clearable style="width: 150px">
        <el-option label="表结构" value="表结构" />
        <el-option label="字段" value="字段" />
        <el-option label="数据字典" value="数据字典" />
        <el-option label="指标" value="指标" />
      </el-select>
      <el-input v-model="filters.business_domain" placeholder="业务域" style="width: 150px" clearable />
      <el-button type="primary" @click="loadData">查询</el-button>
      <el-button type="success" @click="openDialog()">新增元数据</el-button>
    </div>

    <el-table :data="tableData" stripe border>
      <el-table-column prop="meta_name" label="元数据名称" min-width="150" />
      <el-table-column prop="meta_type" label="类型" width="120" />
      <el-table-column prop="source_system" label="来源系统" width="150" />
      <el-table-column prop="business_domain" label="业务域" width="150" />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑元数据' : '新增元数据'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="名称" prop="meta_name">
          <el-input v-model="form.meta_name" />
        </el-form-item>
        <el-form-item label="类型" prop="meta_type">
          <el-select v-model="form.meta_type" placeholder="请选择" style="width: 100%">
            <el-option label="表结构" value="表结构" />
            <el-option label="字段" value="字段" />
            <el-option label="数据字典" value="数据字典" />
            <el-option label="指标" value="指标" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源系统" prop="source_system">
          <el-input v-model="form.source_system" />
        </el-form-item>
        <el-form-item label="业务域" prop="business_domain">
          <el-input v-model="form.business_domain" />
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
import { metadataApi } from '../api'

const tableData = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const filters = reactive({ meta_type: '', business_domain: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const editingId = ref(null)

const form = reactive({
  meta_name: '', meta_type: '', source_system: '', business_domain: '', description: ''
})

const rules = {
  meta_name: [{ required: true, message: '请输入元数据名称', trigger: 'blur' }]
}

async function loadData() {
  try {
    const res = await metadataApi.list({ page: page.value, page_size: pageSize.value, ...filters })
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
    Object.assign(form, { meta_name: '', meta_type: '', source_system: '', business_domain: '', description: '' })
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  try {
    if (isEdit.value) {
      await metadataApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await metadataApi.create(form)
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
    await ElMessageBox.confirm(`确定删除元数据「${row.meta_name}」吗？`, '删除确认', { type: 'warning' })
    await metadataApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message)
  }
}

loadData()
</script>
