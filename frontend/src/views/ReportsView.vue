<template>
  <div class="page-card">
    <div class="page-title">报表应用管理</div>
    
    <div class="search-bar">
      <el-select v-model="filters.report_type" placeholder="报表类型" clearable style="width: 150px">
        <el-option label="运营报表" value="运营报表" />
        <el-option label="分析报表" value="分析报表" />
        <el-option label="驾驶舱" value="驾驶舱" />
      </el-select>
      <el-select v-model="filters.status" placeholder="状态" clearable style="width: 120px">
        <el-option label="草稿" value="草稿" />
        <el-option label="已发布" value="已发布" />
        <el-option label="停用" value="停用" />
      </el-select>
      <el-button type="primary" @click="loadData">查询</el-button>
      <el-button type="success" @click="openDialog()">新增报表</el-button>
    </div>

    <el-table :data="tableData" stripe border>
      <el-table-column prop="report_name" label="报表名称" min-width="150" />
      <el-table-column prop="report_type" label="类型" width="100" />
      <el-table-column prop="creator" label="创建人" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑报表' : '新增报表'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="报表名称" prop="report_name">
          <el-input v-model="form.report_name" />
        </el-form-item>
        <el-form-item label="报表类型" prop="report_type">
          <el-select v-model="form.report_type" placeholder="请选择" style="width: 100%">
            <el-option label="运营报表" value="运营报表" />
            <el-option label="分析报表" value="分析报表" />
            <el-option label="驾驶舱" value="驾驶舱" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建人" prop="creator">
          <el-input v-model="form.creator" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="草稿" value="草稿" />
            <el-option label="已发布" value="已发布" />
            <el-option label="停用" value="停用" />
          </el-select>
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
import { reportsApi } from '../api'

const tableData = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const filters = reactive({ report_type: '', status: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const editingId = ref(null)

const form = reactive({
  report_name: '', report_type: '', creator: '', status: '草稿', description: ''
})

const rules = {
  report_name: [{ required: true, message: '请输入报表名称', trigger: 'blur' }]
}

function statusType(status) {
  const map = { '已发布': 'success', '草稿': 'info', '停用': 'danger' }
  return map[status] || 'info'
}

async function loadData() {
  try {
    const res = await reportsApi.list({ page: page.value, page_size: pageSize.value, ...filters })
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
    Object.assign(form, { report_name: '', report_type: '', creator: '', status: '草稿', description: '' })
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  try {
    if (isEdit.value) {
      await reportsApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await reportsApi.create(form)
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
    await ElMessageBox.confirm(`确定删除报表「${row.report_name}」吗？`, '删除确认', { type: 'warning' })
    await reportsApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message)
  }
}

loadData()
</script>
