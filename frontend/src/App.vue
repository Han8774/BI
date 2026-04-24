<template>
  <el-container class="layout-container">
    <!-- 左侧导航 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
      <div class="logo">
        <span v-if="!isCollapse">仙津数据中台</span>
        <span v-else>仙津</span>
      </div>
      <el-menu
        :default-active="$route.path"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        class="menu"
      >
        <el-menu-item index="/assets">
          <span>资产登记</span>
        </el-menu-item>
        <el-menu-item index="/models">
          <span>模型管理</span>
        </el-menu-item>
        <el-menu-item index="/metadata">
          <span>元数据管理</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <span>报表管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- 顶部 -->
      <el-header class="header">
        <el-icon class="collapse-btn" @click="isCollapse = !isCollapse">
          <Fold v-if="!isCollapse" />
          <Expand v-else />
        </el-icon>
        <div class="header-title">{{ $route.meta.title }}</div>
      </el-header>

      <!-- 主内容 -->
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { Fold, Expand } from '@element-plus/icons-vue'

const isCollapse = ref(false)
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { height: 100%; }

.layout-container { height: 100%; }

.aside {
  background: #001529;
  transition: width 0.3s;
  overflow-x: hidden;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  background: #002140;
  white-space: nowrap;
}

.menu {
  border-right: none;
  background: transparent;
}

.menu .el-menu-item {
  color: rgba(255,255,255,0.7);
}

.menu .el-menu-item:hover,
.menu .el-menu-item.is-active {
  background: #1890ff !important;
  color: #fff !important;
}

.header {
  background: #fff;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
}

.main {
  background: #f0f2f5;
  padding: 20px;
}

.page-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
}

.page-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.table-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
