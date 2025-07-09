#!/usr/bin/env python3
"""
测试新的证书类型识别功能
"""

import requests
import json

API_BASE_URL = "http://localhost:8000/api"

def test_certificate_recognition():
    """测试证书识别功能"""
    
    # 测试数据
    test_cases = [
        # 工程师类型
        {
            "name": "张工程师",
            "certificate_info": "中级工程师 结构工程师",
            "expected_level": "中级工程师",
            "expected_specialty": "结构工程师"
        },
        {
            "name": "李高工",
            "certificate_info": "高级工程师 电气工程师",
            "expected_level": "高级工程师", 
            "expected_specialty": "电气工程师"
        },
        {
            "name": "王助工",
            "certificate_info": "初级工程师 给排水工程师",
            "expected_level": "初级工程师",
            "expected_specialty": "给排水工程师"
        },
        # 三类人员
        {
            "name": "赵安全员",
            "certificate_info": "三类人员C类 安全员",
            "expected_level": "三类人员C类",
            "expected_specialty": "安全管理"
        },
        {
            "name": "钱项目经理",
            "certificate_info": "三类人员B类 项目负责人",
            "expected_level": "三类人员B类",
            "expected_specialty": "安全管理"
        },
        {
            "name": "孙总经理",
            "certificate_info": "三类人员A类 企业主要负责人",
            "expected_level": "三类人员A类",
            "expected_specialty": "安全管理"
        },
        # 混合类型
        {
            "name": "周建造师",
            "certificate_info": "一建房建 造价工程师",
            "expected_level": "一级",
            "expected_specialty": "建筑工程"  # 应该优先识别建造师专业
        }
    ]
    
    print("🧪 测试新证书类型识别")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {case['name']}")
        print(f"证书信息: {case['certificate_info']}")
        
        # 创建测试数据
        talent_data = {
            "name": case['name'],
            "certificate_info": case['certificate_info'],
            "communication_content": case['certificate_info']
        }
        
        try:
            # 发送API请求
            response = requests.post(f"{API_BASE_URL}/talents/", json=talent_data)
            
            if response.status_code == 200:
                result = response.json()
                
                # 检查识别结果
                actual_level = result.get('certificate_level')
                actual_specialty = result.get('certificate_specialty')
                
                level_correct = actual_level == case['expected_level']
                specialty_correct = actual_specialty == case['expected_specialty']
                
                print(f"预期等级: {case['expected_level']} | 实际等级: {actual_level} {'✓' if level_correct else '✗'}")
                print(f"预期专业: {case['expected_specialty']} | 实际专业: {actual_specialty} {'✓' if specialty_correct else '✗'}")
                
                if level_correct and specialty_correct:
                    success_count += 1
                    print("✅ 识别正确")
                else:
                    print("❌ 识别错误")
                    
            else:
                print(f"❌ API请求失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print(f"\n📊 测试结果统计:")
    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"成功率: {(success_count/total_count)*100:.1f}%")

def test_multi_specialty_filter():
    """测试多专业筛选功能"""
    print("\n🔍 测试多专业筛选功能")
    print("=" * 60)
    
    # 测试单专业筛选
    print("\n1. 测试单专业筛选 (建筑工程):")
    response = requests.get(f"{API_BASE_URL}/talents/?certificate_specialty=建筑工程")
    if response.status_code == 200:
        data = response.json()
        count = len(data.get('talents', []))
        print(f"   找到 {count} 个建筑工程专业人才")
    
    # 测试多专业筛选
    print("\n2. 测试多专业筛选 (建筑工程,机电工程):")
    response = requests.get(f"{API_BASE_URL}/talents/?certificate_specialty=建筑工程,机电工程")
    if response.status_code == 200:
        data = response.json()
        count = len(data.get('talents', []))
        print(f"   找到 {count} 个建筑工程或机电工程专业人才")
        
        # 显示前3个结果
        talents = data.get('talents', [])[:3]
        for talent in talents:
            name = talent.get('name')
            specialty = talent.get('certificate_specialty', '未知')
            print(f"   - {name}: {specialty}")

def test_new_certificate_levels():
    """测试新证书等级筛选"""
    print("\n🏆 测试新证书等级筛选")
    print("=" * 60)
    
    levels_to_test = [
        "初级工程师", "中级工程师", "高级工程师",
        "三类人员A类", "三类人员B类", "三类人员C类"
    ]
    
    for level in levels_to_test:
        response = requests.get(f"{API_BASE_URL}/talents/?certificate_level={level}")
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('talents', []))
            print(f"{level}: {count} 人")
        else:
            print(f"{level}: API请求失败")

if __name__ == "__main__":
    # 检查API连接
    try:
        response = requests.get(f"{API_BASE_URL}/talents/")
        if response.status_code != 200:
            print("❌ API连接失败")
            exit(1)
        print("✅ API连接正常")
    except:
        print("❌ 无法连接到API服务")
        exit(1)
    
    # 运行测试
    test_certificate_recognition()
    test_multi_specialty_filter()
    test_new_certificate_levels()
    
    print("\n🎉 测试完成！")
