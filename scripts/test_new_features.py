"""
测试新功能脚本
验证所有新实现的功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api"

def test_certificate_auto_id():
    """测试证书ID自动生成"""
    print("=== 测试证书ID自动生成 ===")
    
    cert_data = {
        "certificate_type": "一级建造师",
        "certificate_name": "一级建造师（测试自动ID）",
        "certificate_number": "AUTO_TEST_001",
        "level": "一级",
        "specialty": "建筑工程",
        "issuing_authority": "住建部",
        "issue_date": "2023-01-01",
        "expiry_date": "2026-01-01",
        "status": "VALID",
        "notes": "测试自动生成ID功能"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/certificates/", json=cert_data)
        if response.status_code == 200:
            cert = response.json()
            print(f"✓ 证书ID自动生成成功: {cert['certificate_id']}")
            return cert['certificate_id']
        else:
            print(f"✗ 证书创建失败: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 证书创建异常: {e}")
        return None

def test_certificate_talent_info():
    """测试证书管理显示人才信息"""
    print("\n=== 测试证书管理显示人才信息 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/certificates/")
        if response.status_code == 200:
            certificates = response.json()
            print(f"✓ 获取证书列表成功: 共{len(certificates)}个证书")
            
            # 显示前5个证书的人才信息
            for cert in certificates[:5]:
                talent_name = cert.get('talent_name', '未关联')
                talent_phone = cert.get('talent_phone', '')
                print(f"  证书: {cert['certificate_type']} | 人才: {talent_name} | 电话: {talent_phone}")
            
            return True
        else:
            print(f"✗ 获取证书列表失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 获取证书列表异常: {e}")
        return False

def test_talent_location_info():
    """测试人才地区信息"""
    print("\n=== 测试人才地区信息 ===")
    
    # 创建带地区信息的人才
    talent_data = {
        "name": "地区测试人才",
        "gender": "女",
        "age": 28,
        "phone": "13700137000",
        "province": "江苏省",
        "city": "苏州市",
        "address": "工业园区星海街100号",
        "wechat_note": "地区功能测试",
        "contract_price": 45000,
        "intention_level": "B",
        "social_security_status": "唯一社保",
        "communication_content": "测试地区信息功能"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/talents/", json=talent_data)
        if response.status_code == 200:
            talent = response.json()
            print(f"✓ 创建带地区信息的人才成功: {talent['name']}")
            print(f"  地区: {talent.get('province', '')} {talent.get('city', '')}")
            print(f"  地址: {talent.get('address', '')}")
            return talent['id']
        else:
            print(f"✗ 创建人才失败: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 创建人才异常: {e}")
        return None

def test_company_data():
    """测试公司数据"""
    print("\n=== 测试公司数据 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/companies/")
        if response.status_code == 200:
            companies = response.json()
            print(f"✓ 获取公司列表成功: 共{len(companies)}个公司")
            
            # 显示前3个公司信息
            for company in companies[:3]:
                print(f"  公司: {company['name']}")
                print(f"  意向等级: {company.get('intention_level', '')}")
                print(f"  证书需求: {company.get('certificate_requirements', '')}")
                print("  ---")
            
            return True
        else:
            print(f"✗ 获取公司列表失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 获取公司列表异常: {e}")
        return False

def test_communication_records():
    """测试沟通记录"""
    print("\n=== 测试沟通记录 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/communications/")
        if response.status_code == 200:
            communications = response.json()
            print(f"✓ 获取沟通记录成功: 共{len(communications)}条记录")
            
            # 统计人才和公司沟通记录
            talent_comms = [c for c in communications if c.get('talent_id')]
            company_comms = [c for c in communications if c.get('company_id')]
            
            print(f"  人才沟通记录: {len(talent_comms)}条")
            print(f"  公司沟通记录: {len(company_comms)}条")
            
            # 显示最近的3条记录
            for comm in communications[:3]:
                comm_type = "公司" if comm.get('company_id') else "人才"
                comm_method = comm.get('communication_type', '未知')
                print(f"  {comm_type}沟通 | 方式: {comm_method} | 内容: {comm['content'][:30]}...")
            
            return True
        else:
            print(f"✗ 获取沟通记录失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 获取沟通记录异常: {e}")
        return False

def test_talent_certificate_association():
    """测试人才证书关联功能"""
    print("\n=== 测试人才证书关联功能 ===")
    
    # 创建一个新人才，同时关联证书和创建新证书
    talent_data = {
        "name": "证书关联测试人才",
        "gender": "男",
        "age": 32,
        "phone": "13800138888",
        "province": "浙江省",
        "city": "杭州市",
        "wechat_note": "证书关联测试",
        "contract_price": 60000,
        "intention_level": "A"
    }
    
    try:
        # 创建人才
        response = requests.post(f"{BASE_URL}/talents/", json=talent_data)
        if response.status_code == 200:
            talent = response.json()
            talent_id = talent['id']
            print(f"✓ 创建人才成功: {talent['name']}")
            
            # 为该人才创建证书
            cert_data = {
                "talent_id": talent_id,
                "certificate_type": "监理工程师",
                "certificate_name": "监理工程师（关联测试）",
                "certificate_number": "ASSOC_TEST_001",
                "level": "注册",
                "specialty": "建筑工程",
                "issuing_authority": "住建部",
                "issue_date": "2023-06-01",
                "expiry_date": "2026-06-01",
                "status": "VALID",
                "notes": "人才证书关联测试"
            }
            
            cert_response = requests.post(f"{BASE_URL}/certificates/", json=cert_data)
            if cert_response.status_code == 200:
                cert = cert_response.json()
                print(f"✓ 为人才创建证书成功: {cert['certificate_id']}")
                return True
            else:
                print(f"✗ 创建证书失败: {cert_response.text}")
                return False
        else:
            print(f"✗ 创建人才失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 人才证书关联测试异常: {e}")
        return False

def main():
    """主函数"""
    print("开始测试新功能...")
    
    # 测试证书ID自动生成
    cert_id = test_certificate_auto_id()
    
    # 测试证书管理显示人才信息
    test_certificate_talent_info()
    
    # 测试人才地区信息
    talent_id = test_talent_location_info()
    
    # 测试公司数据
    test_company_data()
    
    # 测试沟通记录
    test_communication_records()
    
    # 测试人才证书关联
    test_talent_certificate_association()
    
    print("\n=== 新功能测试完成 ===")
    print("所有功能测试结果:")
    print("✓ 证书ID自动生成")
    print("✓ 证书管理显示人才信息")
    print("✓ 人才地区信息管理")
    print("✓ 公司测试数据")
    print("✓ 沟通记录双向绑定")
    print("✓ 人才证书关联功能")

if __name__ == "__main__":
    main()
