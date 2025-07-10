"""
创建测试数据脚本
生成人才、证书和沟通记录的测试数据
"""

import requests
import json
import random
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000/api"

# 测试数据
PROVINCES = [
    "北京市", "上海市", "广东省", "江苏省", "浙江省", 
    "山东省", "河南省", "四川省", "湖北省", "湖南省"
]

CITIES = {
    "北京市": ["北京市"],
    "上海市": ["上海市"],
    "广东省": ["广州市", "深圳市", "珠海市", "佛山市", "东莞市"],
    "江苏省": ["南京市", "苏州市", "无锡市", "常州市", "徐州市"],
    "浙江省": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市"],
    "山东省": ["济南市", "青岛市", "烟台市", "潍坊市", "临沂市"],
    "河南省": ["郑州市", "洛阳市", "开封市", "安阳市", "新乡市"],
    "四川省": ["成都市", "绵阳市", "德阳市", "南充市", "宜宾市"],
    "湖北省": ["武汉市", "宜昌市", "襄阳市", "荆州市", "黄石市"],
    "湖南省": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市"]
}

NAMES = [
    "张伟", "李娜", "王强", "刘敏", "陈杰", "杨丽", "赵磊", "孙静",
    "周涛", "吴琳", "郑浩", "王芳", "李明", "张静", "刘伟", "陈丽",
    "杨强", "赵敏", "孙杰", "周琳", "吴浩", "郑静", "王涛", "李丽"
]

CERTIFICATE_TYPES = [
    "一级建造师", "二级建造师", "一级造价工程师", "监理工程师",
    "注册建筑师", "注册结构师", "注册电气工程师", "注册给排水工程师"
]

SPECIALTIES = [
    "建筑工程", "市政工程", "机电工程", "公路工程", "水利工程",
    "矿业工程", "通信工程", "港口工程", "民航工程", "铁路工程"
]

LEVELS = ["一级", "二级", "高级", "中级", "初级"]

def create_talents():
    """创建人才数据"""
    print("创建人才数据...")
    talents = []
    
    for i in range(20):
        province = random.choice(PROVINCES)
        city = random.choice(CITIES[province])
        
        talent_data = {
            "name": random.choice(NAMES) + str(i+1),
            "gender": random.choice(["男", "女"]),
            "age": random.randint(25, 55),
            "phone": f"1{random.randint(3,9)}{random.randint(100000000, 999999999)}",
            "province": province,
            "city": city,
            "address": f"{city}某某区某某街道{random.randint(1, 999)}号",
            "wechat_note": f"微信备注{i+1}",
            "contract_price": random.randint(20000, 80000),
            "intention_level": random.choice(["A", "B", "C"]),
            "social_security_status": random.choice(["唯一社保", "无社保", "有社保"]),
            "communication_content": f"初次沟通记录{i+1}，人才表现积极"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/talents/", json=talent_data)
            if response.status_code == 200:
                talent = response.json()
                talents.append(talent)
                print(f"创建人才成功: {talent['name']}")
            else:
                print(f"创建人才失败: {response.text}")
        except Exception as e:
            print(f"创建人才异常: {e}")
    
    return talents

def create_certificates(talents):
    """创建证书数据"""
    print("创建证书数据...")
    certificates = []
    
    # 创建一些关联人才的证书
    for talent in talents[:15]:  # 前15个人才有证书
        cert_count = random.randint(1, 3)  # 每个人才1-3个证书
        
        for j in range(cert_count):
            cert_data = {
                "talent_id": talent["id"],
                "certificate_type": random.choice(CERTIFICATE_TYPES),
                "certificate_name": f"{random.choice(CERTIFICATE_TYPES)}（{random.choice(SPECIALTIES)}）",
                "certificate_number": f"CERT{random.randint(100000, 999999)}",
                "level": random.choice(LEVELS),
                "specialty": random.choice(SPECIALTIES),
                "issuing_authority": random.choice(["住建部", "人社部", "工信部", "交通部"]),
                "issue_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
                "expiry_date": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
                "status": random.choice(["VALID", "VALID", "VALID", "EXPIRED"]),  # 大部分有效
                "notes": f"证书备注{j+1}"
            }
            
            try:
                response = requests.post(f"{BASE_URL}/certificates/", json=cert_data)
                if response.status_code == 200:
                    cert = response.json()
                    certificates.append(cert)
                    print(f"创建证书成功: {cert['certificate_type']} - {talent['name']}")
                else:
                    print(f"创建证书失败: {response.text}")
            except Exception as e:
                print(f"创建证书异常: {e}")
    
    # 创建一些未关联人才的证书
    for i in range(10):
        cert_data = {
            "certificate_type": random.choice(CERTIFICATE_TYPES),
            "certificate_name": f"{random.choice(CERTIFICATE_TYPES)}（{random.choice(SPECIALTIES)}）",
            "certificate_number": f"UNLINKED{random.randint(100000, 999999)}",
            "level": random.choice(LEVELS),
            "specialty": random.choice(SPECIALTIES),
            "issuing_authority": random.choice(["住建部", "人社部", "工信部", "交通部"]),
            "issue_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "expiry_date": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": "VALID",
            "notes": f"未关联人才的证书{i+1}"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/certificates/", json=cert_data)
            if response.status_code == 200:
                cert = response.json()
                certificates.append(cert)
                print(f"创建未关联证书成功: {cert['certificate_type']}")
            else:
                print(f"创建未关联证书失败: {response.text}")
        except Exception as e:
            print(f"创建未关联证书异常: {e}")
    
    return certificates

def create_communications(talents):
    """创建沟通记录"""
    print("创建沟通记录...")
    
    for talent in talents[:10]:  # 前10个人才有沟通记录
        comm_count = random.randint(1, 3)
        
        for j in range(comm_count):
            comm_data = {
                "talent_id": talent["id"],
                "communication_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "communication_type": random.choice(["电话", "微信", "面谈", "邮件"]),
                "content": f"与{talent['name']}的第{j+1}次沟通，讨论了合作意向和薪资待遇。",
                "follow_up_required": random.choice([True, False]),
                "follow_up_date": (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d") if random.choice([True, False]) else None
            }
            
            try:
                response = requests.post(f"{BASE_URL}/communications/", json=comm_data)
                if response.status_code == 200:
                    print(f"创建沟通记录成功: {talent['name']}")
                else:
                    print(f"创建沟通记录失败: {response.text}")
            except Exception as e:
                print(f"创建沟通记录异常: {e}")

def main():
    """主函数"""
    print("开始创建测试数据...")
    
    # 创建人才
    talents = create_talents()
    print(f"成功创建 {len(talents)} 个人才")
    
    # 创建证书
    certificates = create_certificates(talents)
    print(f"成功创建 {len(certificates)} 个证书")
    
    # 创建沟通记录
    create_communications(talents)
    
    print("测试数据创建完成！")

if __name__ == "__main__":
    main()
