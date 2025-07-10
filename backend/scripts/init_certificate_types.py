"""
初始化证书类型数据
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api"

# 证书类型数据
CERTIFICATE_TYPES = [
    {
        "type_code": "JZS1",
        "type_name": "一级建造师",
        "category": "建造师",
        "description": "一级建造师执业资格证书",
        "is_active": True,
        "sort_order": 1
    },
    {
        "type_code": "JZS2",
        "type_name": "二级建造师",
        "category": "建造师",
        "description": "二级建造师执业资格证书",
        "is_active": True,
        "sort_order": 2
    },
    {
        "type_code": "ZJ1",
        "type_name": "一级造价工程师",
        "category": "造价工程师",
        "description": "一级造价工程师执业资格证书",
        "is_active": True,
        "sort_order": 3
    },
    {
        "type_code": "JL",
        "type_name": "监理工程师",
        "category": "监理工程师",
        "description": "监理工程师执业资格证书",
        "is_active": True,
        "sort_order": 4
    },
    {
        "type_code": "JZS",
        "type_name": "注册建筑师",
        "category": "建筑师",
        "description": "注册建筑师执业资格证书",
        "is_active": True,
        "sort_order": 5
    },
    {
        "type_code": "JGS",
        "type_name": "注册结构师",
        "category": "结构师",
        "description": "注册结构师执业资格证书",
        "is_active": True,
        "sort_order": 6
    },
    {
        "type_code": "DQ",
        "type_name": "注册电气工程师",
        "category": "电气工程师",
        "description": "注册电气工程师执业资格证书",
        "is_active": True,
        "sort_order": 7
    },
    {
        "type_code": "GPS",
        "type_name": "注册给排水工程师",
        "category": "给排水工程师",
        "description": "注册给排水工程师执业资格证书",
        "is_active": True,
        "sort_order": 8
    }
]

def create_certificate_types():
    """创建证书类型"""
    print("创建证书类型...")
    
    for cert_type in CERTIFICATE_TYPES:
        try:
            response = requests.post(f"{BASE_URL}/certificates/types", json=cert_type)
            if response.status_code == 200:
                print(f"创建证书类型成功: {cert_type['type_name']}")
            else:
                print(f"创建证书类型失败: {cert_type['type_name']} - {response.text}")
        except Exception as e:
            print(f"创建证书类型异常: {cert_type['type_name']} - {e}")

def main():
    """主函数"""
    print("开始初始化证书类型...")
    create_certificate_types()
    print("证书类型初始化完成！")

if __name__ == "__main__":
    main()
