# CRM管理系统

一个基于 FastAPI + Vue.js + PostgreSQL 的CRM管理系统，用于管理公司信息和人才信息。

## 功能特性

### 公司管理
- 公司名称、联系方式管理
- 沟通内容备注记录
- 客户沟通意向和意向等级（A/B/C级）
- 价格信息管理
- 建造师证书需求管理

### 人才管理
- 人才基本信息（姓名、性别、年龄）
- 联系方式（电话、微信添加备注）
- 建造师证书信息和到期时间
- 签订合同价格
- 人才意向等级（A/B/C级）

### 沟通记录
- 与公司或人才的沟通历史记录
- 沟通内容和结果跟踪
- 时间戳记录

## 技术栈

- **后端**: Python + FastAPI + SQLAlchemy + PostgreSQL
- **前端**: Vue.js 3 + Element Plus + Vite
- **部署**: Docker + Docker Compose

## 快速开始

### 前置要求
- Docker
- Docker Compose

### 运行步骤

1. 克隆项目
```bash
git clone <repository-url>
cd crm-system
```

2. 启动所有服务
```bash
docker-compose up -d
```

3. 访问应用
- 前端界面: http://localhost:3000
- 后端API文档: http://localhost:8000/docs
- 数据库: localhost:5432

### 开发模式

如果需要开发模式（支持热重载）：

```bash
# 启动数据库
docker-compose up -d postgres

# 后端开发
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端开发
cd frontend
npm install
npm run dev
```

## API接口

### 公司管理
- `GET /api/companies/` - 获取公司列表
- `POST /api/companies/` - 创建公司
- `GET /api/companies/{id}` - 获取公司详情
- `PUT /api/companies/{id}` - 更新公司信息
- `DELETE /api/companies/{id}` - 删除公司

### 人才管理
- `GET /api/talents/` - 获取人才列表
- `POST /api/talents/` - 创建人才
- `GET /api/talents/{id}` - 获取人才详情
- `PUT /api/talents/{id}` - 更新人才信息
- `DELETE /api/talents/{id}` - 删除人才

### 沟通记录
- `GET /api/communications/` - 获取沟通记录列表
- `POST /api/communications/` - 创建沟通记录
- `GET /api/communications/{id}` - 获取沟通记录详情
- `PUT /api/communications/{id}` - 更新沟通记录
- `DELETE /api/communications/{id}` - 删除沟通记录

## 数据库结构

### 公司表 (companies)
- id: 主键
- name: 公司名称
- contact_info: 联系方式
- communication_notes: 沟通备注
- intention: 沟通意向
- intention_level: 意向等级 (A/B/C)
- price: 价格
- certificate_requirements: 证书需求

### 人才表 (talents)
- id: 主键
- name: 姓名
- gender: 性别
- age: 年龄
- phone: 电话
- wechat_note: 微信添加备注
- certificate_info: 证书信息
- certificate_expiry_date: 证书到期时间
- contract_price: 签订合同价格
- intention_level: 意向等级 (A/B/C)

### 沟通记录表 (communications)
- id: 主键
- content: 沟通内容
- result: 沟通结果
- communication_time: 沟通时间
- company_id: 关联公司ID
- talent_id: 关联人才ID

## 停止服务

```bash
docker-compose down
```

## 清理数据

```bash
docker-compose down -v
```
