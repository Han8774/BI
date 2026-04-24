<template>
  <div class="page-card">
    <div class="page-title">数据资产管理</div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索资产名称或类型" style="width: 200px" @keyup.enter="loadData" />
      <el-button type="primary" @click="loadData">查询</el-button>
      <el-button type="success" @click="openDialog()">新增资产</el-button>
    </div>

    <!-- 数据表格 -->
    <el-table :data="tableData" stripe border>
      <el-table-column prop="asset_code" label="资产编号" width="150" />
      <el-table-column prop="asset_name" label="资产名称" min-width="150" />
      <el-table-column prop="asset_type" label="资产类型" width="120" />
      <el-table-column prop="department" label="所属部门" width="120" />
      <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="table-pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadData"
      />
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑资产' : '新增资产'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="资产编号" prop="asset_code">
          <el-input v-model="form.asset_code" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="资产名称" prop="asset_name">
          <el-input v-model="form.asset_name" />
        </el-form-item>
        <el-form-item label="资产类型" prop="asset_type">
          <el-select v-model="form.asset_type" placeholder="请选择" style="width: 100%">
            <el-option label="数据集" value="数据集" />
            <el-option label="数据表" value="数据表" />
            <el-option label="API接口" value="API接口" />
            <el-option label="文件" value="文件" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门" prop="department">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" rows="3" />
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
import { assetsApi } from '../api'

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
  asset_code: '',
  asset_name: '',
  asset_type: '',
  department: '',
  remark: ''
})

const rules = {
  asset_code: [{ required: true, message: '请输入资产编号', trigger: 'blur' }],
  asset_name: [{ required: true, message: '请输入资产名称', trigger: 'blur' }]
}

async function loadData() {
  try {
    const res = await assetsApi.list({ page: page.value, page_size: pageSize.value, search: search.value })
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
    Object.assign(form, { asset_code: '', asset_name: '', asset_type: '', department: '', remark: '' })
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  try {
    if (isEdit.value) {
      await assetsApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await assetsApi.create(form)
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
    await ElMessageBox.confirm(`确定删除资产「${row.asset_name}」吗？`, '删除确认', { type: 'warning' })
    await assetsApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.message)
  }
}

loadData()
</script>
