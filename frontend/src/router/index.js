import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/assets'
  },
  {
    path: '/assets',
    component: () => import('../views/AssetsView.vue'),
    meta: { title: '资产登记' }
  },
  {
    path: '/models',
    component: () => import('../views/ModelsView.vue'),
    meta: { title: '模型管理' }
  },
  {
    path: '/metadata',
    component: () => import('../views/MetadataView.vue'),
    meta: { title: '元数据管理' }
  },
  {
    path: '/reports',
    component: () => import('../views/ReportsView.vue'),
    meta: { title: '报表管理' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
