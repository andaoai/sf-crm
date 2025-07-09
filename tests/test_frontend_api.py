#!/usr/bin/env python3
"""
测试前端API连接
"""

import requests
import json

def test_frontend_proxy():
    """测试前端代理是否正常工作"""
    
    print("🔗 测试前端代理连接")
    print("=" * 50)
    
    # 测试通过前端代理访问API
    frontend_api_url = "http://localhost:3001/api/talents/"
    
    try:
        print("1. 测试通过前端代理获取人才列表...")
        response = requests.get(frontend_api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('talents', []))
            print(f"   ✅ 成功！找到 {count} 个人才")
            
            # 显示前几个人才
            talents = data.get('talents', [])[:3]
            for talent in talents:
                name = talent.get('name')
                level = talent.get('certificate_level', '未设置')
                specialty = talent.get('certificate_specialty', '未设置')
                print(f"   - {name}: {level} | {specialty}")
        else:
            print(f"   ❌ 失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.Timeout:
        print("   ❌ 请求超时")
    except requests.exceptions.ConnectionError:
        print("   ❌ 连接错误")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 测试创建功能
    print("\n2. 测试通过前端代理创建人才...")
    
    test_data = {
        "name": "API测试用户",
        "certificate_level": "中级工程师",
        "certificate_specialty": "建筑工程师",
        "phone": "13900139000"
    }
    
    try:
        response = requests.post(frontend_api_url, json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 创建成功！ID: {result.get('id')}")
            print(f"   姓名: {result.get('name')}")
            print(f"   等级: {result.get('certificate_level')}")
            print(f"   专业: {result.get('certificate_specialty')}")
        else:
            print(f"   ❌ 创建失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 创建异常: {e}")

def test_direct_backend():
    """测试直接访问后端API"""
    
    print("\n🎯 测试直接后端连接")
    print("=" * 50)
    
    backend_api_url = "http://localhost:8000/api/talents/"
    
    try:
        print("1. 直接访问后端API...")
        response = requests.get(backend_api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('talents', []))
            print(f"   ✅ 后端正常！找到 {count} 个人才")
        else:
            print(f"   ❌ 后端异常: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 后端连接失败: {e}")

def test_cors_and_headers():
    """测试CORS和请求头"""
    
    print("\n🌐 测试CORS和请求头")
    print("=" * 50)
    
    # 模拟浏览器请求
    headers = {
        'Origin': 'http://localhost:3001',
        'Referer': 'http://localhost:3001/',
        'User-Agent': 'Mozilla/5.0 (Test Browser)',
        'Content-Type': 'application/json'
    }
    
    try:
        print("1. 测试带Origin头的请求...")
        response = requests.get("http://localhost:3001/api/talents/", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("   ✅ CORS正常")
        else:
            print(f"   ❌ CORS问题: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ CORS测试失败: {e}")

def main():
    print("🧪 前端API连接测试")
    print("=" * 60)
    
    test_direct_backend()
    test_frontend_proxy()
    test_cors_and_headers()
    
    print("\n📋 测试总结:")
    print("- 如果直接后端访问正常，但前端代理失败，说明是代理配置问题")
    print("- 如果都正常，可能是前端JavaScript的异步处理问题")
    print("- 建议检查浏览器开发者工具的Network和Console标签")

if __name__ == "__main__":
    main()
