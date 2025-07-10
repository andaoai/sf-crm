#!/usr/bin/env python3
"""
测试证书搜索功能
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_certificate_list():
    """测试证书列表API"""
    print("=== 测试证书列表API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/certificates/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取证书列表成功: {len(data)}个证书")
            return True
        else:
            print(f"✗ 获取证书列表失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_certificate_types():
    """测试证书类型API"""
    print("\n=== 测试证书类型API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/certificates/types")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 获取证书类型成功: {len(data)}个类型")
            
            # 显示前5个证书类型
            for i, cert_type in enumerate(data[:5]):
                print(f"  {i+1}. {cert_type['type_name']} ({cert_type['category']})")
            
            return True
        else:
            print(f"✗ 获取证书类型失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_certificate_search_by_type():
    """测试按证书类型搜索"""
    print("\n=== 测试按证书类型搜索 ===")
    
    try:
        params = {"certificate_type": "一级建造师"}
        response = requests.get(f"{BASE_URL}/certificates/", params=params)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 按证书类型搜索成功: {len(data)}个结果")
            return True
        else:
            print(f"✗ 按证书类型搜索失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_certificate_search_by_category():
    """测试按证书大类搜索"""
    print("\n=== 测试按证书大类搜索 ===")
    
    try:
        params = {"category": "建造师"}
        response = requests.get(f"{BASE_URL}/certificates/", params=params)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 按证书大类搜索成功: {len(data)}个结果")
            return True
        else:
            print(f"✗ 按证书大类搜索失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_certificate_search_by_status():
    """测试按证书状态搜索"""
    print("\n=== 测试按证书状态搜索 ===")
    
    try:
        params = {"status": "VALID"}
        response = requests.get(f"{BASE_URL}/certificates/", params=params)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 按证书状态搜索成功: {len(data)}个结果")
            return True
        else:
            print(f"✗ 按证书状态搜索失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_certificate_search_by_talent():
    """测试按人才名称搜索"""
    print("\n=== 测试按人才名称搜索 ===")
    
    try:
        params = {"talent_name": "张工程师"}
        response = requests.get(f"{BASE_URL}/certificates/", params=params)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 按人才名称搜索成功: {len(data)}个结果")
            for cert in data:
                print(f"  - {cert['certificate_type']} ({cert['talent_name']})")
            return True
        else:
            print(f"✗ 按人才名称搜索失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def test_combined_search():
    """测试组合搜索"""
    print("\n=== 测试组合搜索 ===")
    
    try:
        params = {
            "category": "建造师",
            "status": "VALID",
            "talent_name": "张"
        }
        response = requests.get(f"{BASE_URL}/certificates/", params=params)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 组合搜索成功: {len(data)}个结果")
            return True
        else:
            print(f"✗ 组合搜索失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("开始测试证书搜索功能...\n")
    
    tests = [
        test_certificate_list,
        test_certificate_types,
        test_certificate_search_by_type,
        test_certificate_search_by_category,
        test_certificate_search_by_status,
        test_certificate_search_by_talent,
        test_combined_search
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("❌ 部分测试失败，请检查问题")

if __name__ == "__main__":
    main()
