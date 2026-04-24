# 仙津数据中台

前后端分离的数据中台管理系统，包含数据资产管理、模型结构管理、元数据管理、报表应用管理四大模块。

## 技术栈

- **前端**: Vue 3 + Element Plus + Vue Router + Vite
- **后端**: Python Flask + SQLite
- **数据库**: SQLite（自动创建）

## 项目结构

```
BI-project/
├── backend/              # 后端Flask项目
│   ├── app.py           # 主应用文件
│   └── requirements.txt  # Python依赖
├── frontend/            # 前端Vue项目
│   ├── src/
│   │   ├── main.js      # 入口文件
│   │   ├── App.vue      # 根组件
│   │   ├── router/      # 路由配置
│   │   ├── views/       # 页面组件
│   │   └── api/         # API调用
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 快速启动

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端启动后会自动创建 SQLite 数据库 `xianjin_platform.db`。

后端地址: http://localhost:5000

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端地址: http://localhost:3000

> Vite 开发服务器已配置 API 代理，访问 `/api/*` 会自动转发到后端。

## 功能模块

### 1. 资产登记
- 管理数据资产信息
- 支持按名称/类型搜索
- 包含编号唯一性校验

### 2. 模型管理
- 管理AI/ML模型信息
- 支持按名称/类型筛选
- 记录算法、负责人等

### 3. 元数据管理
- 管理元数据条目
- 支持按类型/业务域过滤
- 记录来源系统信息

### 4. 报表管理
- 管理报表应用
- 支持按类型/状态筛选
- 状态流转：草稿 → 已发布 → 停用

## API接口

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 资产 | /api/assets | GET | 列表查询 |
| 资产 | /api/assets | POST | 新增 |
| 资产 | /api/assets/:id | GET | 详情 |
| 资产 | /api/assets/:id | PUT | 更新 |
| 资产 | /api/assets/:id | DELETE | 删除 |
| 模型 | /api/models | GET/POST | 列表/新增 |
| 模型 | /api/models/:id | GET/PUT/DELETE | CRUD |
| 元数据 | /api/metadata | GET/POST | 列表/新增 |
| 元数据 | /api/metadata/:id | GET/PUT/DELETE | CRUD |
| 报表 | /api/reports | GET/POST | 列表/新增 |
| 报表 | /api/reports/:id | GET/PUT/DELETE | CRUD |

## 返回格式

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```
