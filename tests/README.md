# 测试文件夹

这个文件夹包含了项目的所有测试脚本。

## 文件说明

### test_final_features.py
- **功能**: 测试最终功能
- **描述**: 测试创建不同类型的人才，包括建造师、工程师等各种证书类型的人才创建和查询功能
- **运行方式**: `python test_final_features.py`

### test_frontend_api.py  
- **功能**: 测试前端API连接
- **描述**: 测试前端代理是否正常工作，验证前端与后端API的连接状态
- **运行方式**: `python test_frontend_api.py`

### test_new_certificates.py
- **功能**: 测试新的证书类型识别功能
- **描述**: 测试证书识别功能，验证系统能否正确识别和分类各种证书信息
- **运行方式**: `python test_new_certificates.py`

## 运行测试

### 前提条件
1. 确保后端服务正在运行 (http://localhost:8000)
2. 确保前端服务正在运行 (http://localhost:3001) - 仅对 test_frontend_api.py 需要
3. 安装必要的依赖包：
   ```bash
   pip install requests
   ```

### 运行单个测试
```bash
cd tests
python test_final_features.py
python test_frontend_api.py  
python test_new_certificates.py
```

### 运行所有测试
```bash
cd tests
python test_final_features.py && python test_frontend_api.py && python test_new_certificates.py
```

## 测试内容

- **API连接测试**: 验证与后端API的连接
- **数据创建测试**: 测试人才信息的创建功能
- **证书识别测试**: 测试证书信息的自动识别和分类
- **前端代理测试**: 测试前端代理服务的工作状态
- **搜索功能测试**: 测试各种搜索和筛选功能

## 注意事项

- 测试前请确保数据库服务正常运行
- 某些测试可能会创建测试数据，请在测试环境中运行
- 如果测试失败，请检查API服务状态和网络连接
