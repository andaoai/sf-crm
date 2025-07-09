#!/usr/bin/env python3
"""
测试最终功能
"""

import requests
import json
import urllib.parse

API_BASE_URL = "http://localhost:8000/api"

def test_create_talents():
    """测试创建不同类型的人才"""
    
    test_cases = [
        {
            "name": "李建造师",
            "certificate_level": "一级",
            "certificate_specialty": "建筑工程",
            "social_security_status": "唯一社保",
            "phone": "13800138001"
        },
        {
            "name": "王工程师", 
            "certificate_level": "高级工程师",
            "certificate_specialty": "电气工程师",
            "social_security_status": "无社保",
            "phone": "13800138002"
        },
        {
            "name": "张安全员",
            "certificate_level": "三类人员C类", 
            "certificate_specialty": "安全管理",
            "phone": "13800138003"
        },
        {
            "name": "赵项目经理",
            "certificate_level": "三类人员B类",
            "certificate_specialty": "安全管理", 
            "phone": "13800138004"
        }
    ]
    
    print("🧪 测试创建不同类型人才")
    print("=" * 50)
    
    created_ids = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 创建 {case['name']}")
        
        try:
            response = requests.post(f"{API_BASE_URL}/talents/", json=case)
            
            if response.status_code == 200:
                result = response.json()
                created_ids.append(result['id'])
                print(f"   ✅ 成功创建 ID: {result['id']}")
                print(f"   等级: {result.get('certificate_level', '未设置')}")
                print(f"   专业: {result.get('certificate_specialty', '未设置')}")
                print(f"   社保: {result.get('social_security_status', '未设置')}")
            else:
                print(f"   ❌ 创建失败: {response.status_code}")
                print(f"   错误: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
    
    return created_ids

def test_list_talents():
    """测试获取人才列表"""
    print("\n📋 测试获取人才列表")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/talents/")
        
        if response.status_code == 200:
            data = response.json()
            talents = data.get('talents', [])
            total = data.get('total', 0)
            
            print(f"✅ 成功获取人才列表")
            print(f"总数: {total}")
            
            print("\n人才列表:")
            for talent in talents:
                name = talent.get('name')
                level = talent.get('certificate_level', '未设置')
                specialty = talent.get('certificate_specialty', '未设置')
                social = talent.get('social_security_status', '未设置')
                print(f"- {name}: {level} | {specialty} | {social}")
                
        else:
            print(f"❌ 获取失败: {response.status_code}")
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_filter_by_level():
    """测试按证书等级筛选"""
    print("\n🔍 测试按证书等级筛选")
    print("=" * 50)
    
    levels_to_test = ["一级", "高级工程师", "三类人员C类"]
    
    for level in levels_to_test:
        try:
            # URL编码
            encoded_level = urllib.parse.quote(level)
            response = requests.get(f"{API_BASE_URL}/talents/?certificate_level={encoded_level}")
            
            if response.status_code == 200:
                data = response.json()
                talents = data.get('talents', [])
                count = len(talents)
                print(f"✅ {level}: 找到 {count} 人")
                
                for talent in talents:
                    print(f"   - {talent['name']}")
            else:
                print(f"❌ {level}: 筛选失败 {response.status_code}")
                
        except Exception as e:
            print(f"❌ {level}: 请求异常 {e}")

def test_filter_by_specialty():
    """测试按证书专业筛选"""
    print("\n🔧 测试按证书专业筛选")
    print("=" * 50)
    
    specialties_to_test = ["建筑工程", "电气工程师", "安全管理"]
    
    for specialty in specialties_to_test:
        try:
            # URL编码
            encoded_specialty = urllib.parse.quote(specialty)
            response = requests.get(f"{API_BASE_URL}/talents/?certificate_specialty={encoded_specialty}")
            
            if response.status_code == 200:
                data = response.json()
                talents = data.get('talents', [])
                count = len(talents)
                print(f"✅ {specialty}: 找到 {count} 人")
                
                for talent in talents:
                    print(f"   - {talent['name']}")
            else:
                print(f"❌ {specialty}: 筛选失败 {response.status_code}")
                
        except Exception as e:
            print(f"❌ {specialty}: 请求异常 {e}")

def test_multi_specialty_filter():
    """测试多专业筛选"""
    print("\n🎯 测试多专业筛选")
    print("=" * 50)
    
    try:
        # 测试多选：建筑工程,电气工程师
        specialties = "建筑工程,电气工程师"
        encoded_specialties = urllib.parse.quote(specialties)
        response = requests.get(f"{API_BASE_URL}/talents/?certificate_specialty={encoded_specialties}")
        
        if response.status_code == 200:
            data = response.json()
            talents = data.get('talents', [])
            count = len(talents)
            print(f"✅ 多选筛选 ({specialties}): 找到 {count} 人")
            
            for talent in talents:
                specialty = talent.get('certificate_specialty', '未设置')
                print(f"   - {talent['name']}: {specialty}")
        else:
            print(f"❌ 多选筛选失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 多选筛选异常: {e}")

def main():
    print("🎉 CRM系统功能测试")
    print("=" * 60)
    
    # 检查API连接
    try:
        response = requests.get(f"{API_BASE_URL}/talents/")
        if response.status_code != 200:
            print("❌ API连接失败")
            return
        print("✅ API连接正常")
    except:
        print("❌ 无法连接到API服务")
        return
    
    # 运行测试
    created_ids = test_create_talents()
    test_list_talents()
    test_filter_by_level()
    test_filter_by_specialty()
    test_multi_specialty_filter()
    
    print(f"\n🎊 测试完成！创建了 {len(created_ids)} 个测试人才")
    print("现在可以在前端界面 http://localhost:3001 查看和测试筛选功能")

if __name__ == "__main__":
    main()
