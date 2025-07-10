# CRM 数据库管理脚本

这个目录包含了用于管理CRM系统数据库的实用脚本。

## 脚本说明

### 1. reset_database.py
**数据库重置工具**

功能：
- 清空所有数据库表的数据（保留表结构）
- 自动调用数据插入脚本重新录入测试数据
- 验证数据录入结果

使用方法：
```bash
# 在Docker容器内运行
docker-compose exec backend python scripts/reset_database.py

# 或者进入容器后运行
docker-compose exec backend bash
cd /app
python scripts/reset_database.py
```

### 2. direct_data_insert.py
**直接数据库插入工具**

功能：
- 直接操作数据库插入测试数据（不依赖API）
- 插入证书类型、人才、证书、公司、沟通记录等完整数据
- 生成符合系统要求的随机测试数据

使用方法：
```bash
# 在Docker容器内运行
docker-compose exec backend python scripts/direct_data_insert.py

# 或者进入容器后运行
docker-compose exec backend bash
cd /app
python scripts/direct_data_insert.py
```

### 3. test_certificate_types.py
**证书类型功能测试工具**

功能：
- 测试证书类型自动补全功能
- 验证新证书类型的创建和使用
- 展示证书类型统计信息

使用方法：
```bash
# 在Docker容器内运行
docker-compose exec backend python scripts/test_certificate_types.py
```

## 数据说明

插入的测试数据包括：
- **证书类型**: 8种（建造师、工程师等各类证书）
- **人才**: 20个（包含完整的个人信息、地区信息、社保状态）
- **证书**: 36个（每个人才1-3个证书，包含等级、专业、状态等）
- **公司**: 15个（包含联系信息、意向等级、证书需求）
- **沟通记录**: 20条（与人才和公司的沟通记录）

## 注意事项

1. 这些脚本会清空现有数据，请在测试环境中使用
2. 确保Docker服务正在运行
3. 脚本需要在后端容器内执行
4. 数据插入后可以在前端界面 http://localhost:3001 查看结果

## 故障排除

如果遇到数据库连接问题：
1. 确认PostgreSQL容器正在运行：`docker-compose ps`
2. 检查数据库连接配置是否正确
3. 确认在正确的容器内执行脚本

如果遇到枚举类型错误：
1. 检查数据库迁移是否完成
2. 确认枚举类型定义与模型一致
3. 重启后端服务：`docker-compose restart backend`
