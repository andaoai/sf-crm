"""
测试CRUD操作脚本
验证人才和证书的增删改查功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api"

def test_talent_crud():
    """测试人才CRUD操作"""
    print("=== 测试人才CRUD操作 ===")
    
    # 1. 创建人才
    print("1. 创建人才...")
    talent_data = {
        "name": "CRUD测试人才",
        "gender": "男",
        "age": 35,
        "phone": "13900139000",
        "province": "广东省",
        "city": "深圳市",
        "address": "南山区科技园",
        "wechat_note": "CRUD测试备注",
        "contract_price": 50000,
        "intention_level": "A",
        "social_security_status": "唯一社保",
        "communication_content": "CRUD测试沟通内容"
    }
    
    response = requests.post(f"{BASE_URL}/talents/", json=talent_data)
    if response.status_code == 200:
        talent = response.json()
        talent_id = talent["id"]
        print(f"✓ 创建人才成功: ID={talent_id}, 姓名={talent['name']}")
    else:
        print(f"✗ 创建人才失败: {response.text}")
        return None
    
    # 2. 查询人才
    print("2. 查询人才...")
    response = requests.get(f"{BASE_URL}/talents/{talent_id}")
    if response.status_code == 200:
        talent = response.json()
        print(f"✓ 查询人才成功: {talent['name']}, 地区: {talent.get('province', '')} {talent.get('city', '')}")
    else:
        print(f"✗ 查询人才失败: {response.text}")
    
    # 3. 更新人才
    print("3. 更新人才...")
    update_data = {
        "age": 36,
        "city": "广州市",
        "communication_content": "更新后的沟通内容"
    }
    response = requests.put(f"{BASE_URL}/talents/{talent_id}", json=update_data)
    if response.status_code == 200:
        talent = response.json()
        print(f"✓ 更新人才成功: 年龄={talent['age']}, 城市={talent.get('city', '')}")
    else:
        print(f"✗ 更新人才失败: {response.text}")
    
    return talent_id

def test_certificate_crud(talent_id=None):
    """测试证书CRUD操作"""
    print("\n=== 测试证书CRUD操作 ===")
    
    # 1. 创建证书（关联人才）
    print("1. 创建关联人才的证书...")
    cert_data = {
        "talent_id": talent_id,
        "certificate_type": "一级建造师",
        "certificate_name": "一级建造师（CRUD测试）",
        "certificate_number": "CRUD123456",
        "level": "一级",
        "specialty": "建筑工程",
        "issuing_authority": "住建部",
        "issue_date": "2023-01-01",
        "expiry_date": "2026-01-01",
        "status": "VALID",
        "notes": "CRUD测试证书"
    }
    
    response = requests.post(f"{BASE_URL}/certificates/", json=cert_data)
    if response.status_code == 200:
        cert = response.json()
        cert_id = cert["certificate_id"]
        print(f"✓ 创建关联证书成功: ID={cert_id}, 类型={cert['certificate_type']}")
    else:
        print(f"✗ 创建关联证书失败: {response.text}")
        return None
    
    # 2. 创建未关联证书
    print("2. 创建未关联人才的证书...")
    unlinked_cert_data = {
        "certificate_type": "二级建造师",
        "certificate_name": "二级建造师（未关联测试）",
        "certificate_number": "UNLINKED123456",
        "level": "二级",
        "specialty": "机电工程",
        "issuing_authority": "住建部",
        "issue_date": "2023-06-01",
        "expiry_date": "2026-06-01",
        "status": "VALID",
        "notes": "未关联人才的测试证书"
    }
    
    response = requests.post(f"{BASE_URL}/certificates/", json=unlinked_cert_data)
    if response.status_code == 200:
        unlinked_cert = response.json()
        unlinked_cert_id = unlinked_cert["certificate_id"]
        print(f"✓ 创建未关联证书成功: ID={unlinked_cert_id}")
    else:
        print(f"✗ 创建未关联证书失败: {response.text}")
        unlinked_cert_id = None
    
    # 3. 查询证书列表
    print("3. 查询证书列表...")
    response = requests.get(f"{BASE_URL}/certificates/")
    if response.status_code == 200:
        certificates = response.json()
        print(f"✓ 查询证书列表成功: 共{len(certificates)}个证书")
        for cert in certificates[-3:]:  # 显示最后3个证书
            talent_name = cert.get('talent_name', '未关联')
            print(f"  - {cert['certificate_type']} | 人才: {talent_name}")
    else:
        print(f"✗ 查询证书列表失败: {response.text}")
    
    # 4. 更新证书（关联人才）
    if unlinked_cert_id and talent_id:
        print("4. 将未关联证书关联到人才...")
        update_data = {"talent_id": talent_id}
        response = requests.put(f"{BASE_URL}/certificates/{unlinked_cert_id}", json=update_data)
        if response.status_code == 200:
            print(f"✓ 证书关联成功")
        else:
            print(f"✗ 证书关联失败: {response.text}")
    
    return cert_id

def test_talent_with_certificates():
    """测试人才与证书的关联功能"""
    print("\n=== 测试人才与证书关联功能 ===")
    
    # 查询有证书的人才
    response = requests.get(f"{BASE_URL}/talents/")
    if response.status_code == 200:
        talents_data = response.json()
        if isinstance(talents_data, list):
            talents = talents_data
        else:
            talents = talents_data.get('items', [])

        print(f"✓ 查询人才列表成功: 共{len(talents)}个人才")

        # 显示前5个人才的证书信息
        for talent in talents[:5]:
            print(f"  人才: {talent['name']} | 地区: {talent.get('province', '')} {talent.get('city', '')}")
    else:
        print(f"✗ 查询人才列表失败: {response.text}")

def main():
    """主函数"""
    print("开始CRUD操作测试...")
    
    # 测试人才CRUD
    talent_id = test_talent_crud()
    
    # 测试证书CRUD
    if talent_id:
        cert_id = test_certificate_crud(talent_id)
    
    # 测试关联功能
    test_talent_with_certificates()
    
    print("\n=== CRUD测试完成 ===")

if __name__ == "__main__":
    main()
