"""
创建公司测试数据脚本
生成公司和相关沟通记录的测试数据
"""

import requests
import json
import random
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000/api"

# 公司名称数据
COMPANY_NAMES = [
    "中建集团有限公司",
    "中国铁建股份有限公司", 
    "中国交通建设集团有限公司",
    "中国电力建设集团有限公司",
    "中国能源建设集团有限公司",
    "上海建工集团股份有限公司",
    "北京建工集团有限责任公司",
    "广州建筑集团有限公司",
    "深圳市建筑工务署",
    "杭州市建设集团有限公司",
    "南京建工集团有限公司",
    "成都建工集团有限公司",
    "重庆建工集团股份有限公司",
    "西安建工集团有限公司",
    "青岛建设集团有限公司",
    "大连建设集团有限公司",
    "天津建工集团有限公司",
    "苏州建设集团有限公司",
    "无锡建设集团股份有限公司",
    "宁波建工集团有限公司"
]

# 联系方式模板
CONTACT_TEMPLATES = [
    "联系人：{name}\n电话：{phone}\n邮箱：{email}\n地址：{address}",
    "负责人：{name}\n手机：{phone}\n办公电话：{office_phone}\n公司地址：{address}",
    "项目经理：{name}\n联系电话：{phone}\n微信：{wechat}\n办公地址：{address}"
]

# 联系人姓名
CONTACT_NAMES = [
    "张经理", "李总监", "王主任", "刘部长", "陈经理", "杨总", "赵主管", 
    "孙经理", "周总监", "吴主任", "郑经理", "王总", "李主管", "张总监"
]

# 城市地址
CITIES_ADDRESSES = {
    "北京": ["朝阳区建国门外大街", "海淀区中关村大街", "西城区金融街", "东城区王府井大街"],
    "上海": ["浦东新区陆家嘴", "黄浦区南京路", "徐汇区淮海路", "静安区南京西路"],
    "广州": ["天河区珠江新城", "越秀区环市路", "海珠区琶洲", "番禺区万博商务区"],
    "深圳": ["南山区科技园", "福田区中心区", "罗湖区东门", "宝安区新安"],
    "杭州": ["西湖区文三路", "江干区钱江新城", "拱墅区运河新城", "滨江区滨安路"],
    "南京": ["鼓楼区中山路", "玄武区新街口", "建邺区河西新城", "秦淮区夫子庙"],
    "成都": ["锦江区春熙路", "青羊区宽窄巷子", "武侯区天府大道", "高新区软件园"],
    "重庆": ["渝中区解放碑", "江北区观音桥", "南岸区南坪", "沙坪坝区三峡广场"]
}

# 证书需求
CERTIFICATE_REQUIREMENTS = [
    "一级建造师（建筑工程）2名",
    "一级建造师（市政工程）1名，二级建造师（机电工程）2名",
    "监理工程师1名，一级造价工程师1名",
    "注册建筑师1名，注册结构师1名",
    "一级建造师（水利工程）1名",
    "二级建造师（公路工程）3名",
    "一级建造师（机电工程）2名，监理工程师1名",
    "注册电气工程师1名，一级建造师（建筑工程）1名"
]

def create_companies():
    """创建公司数据"""
    print("创建公司数据...")
    companies = []
    
    for i, company_name in enumerate(COMPANY_NAMES):
        # 随机选择城市和地址
        city = random.choice(list(CITIES_ADDRESSES.keys()))
        address = random.choice(CITIES_ADDRESSES[city])
        
        # 生成联系信息
        contact_name = random.choice(CONTACT_NAMES)
        phone = f"1{random.randint(3,9)}{random.randint(100000000, 999999999)}"
        email = f"{contact_name.replace('经理', '').replace('总监', '').replace('主任', '').replace('部长', '').replace('总', '').replace('主管', '')}@{company_name[:4].replace('有限公司', '').replace('股份', '').replace('集团', '')}.com"
        
        contact_template = random.choice(CONTACT_TEMPLATES)
        contact_info = contact_template.format(
            name=contact_name,
            phone=phone,
            email=email,
            office_phone=f"010-{random.randint(10000000, 99999999)}",
            wechat=f"wx_{random.randint(100000, 999999)}",
            address=f"{city}{address}{random.randint(1, 999)}号"
        )
        
        company_data = {
            "name": company_name,
            "contact_info": contact_info,
            "communication_notes": f"与{company_name}的初步沟通记录，了解了项目需求和合作意向。",
            "intention": f"有{random.choice(['住宅', '商业', '基础设施', '工业'])}项目合作需求，预计项目周期{random.randint(6, 24)}个月。",
            "intention_level": random.choice(["A", "B", "C"]),
            "price": f"{random.randint(3, 15)}万/年",
            "certificate_requirements": random.choice(CERTIFICATE_REQUIREMENTS)
        }
        
        try:
            response = requests.post(f"{BASE_URL}/companies/", json=company_data)
            if response.status_code == 200:
                company = response.json()
                companies.append(company)
                print(f"✓ 创建公司成功: {company['name']}")
            else:
                print(f"✗ 创建公司失败: {company_name} - {response.text}")
        except Exception as e:
            print(f"✗ 创建公司异常: {company_name} - {e}")
    
    return companies

def create_company_communications(companies):
    """创建公司沟通记录"""
    print("\n创建公司沟通记录...")
    
    for company in companies[:10]:  # 前10个公司有沟通记录
        comm_count = random.randint(1, 4)  # 每个公司1-4条沟通记录
        
        for j in range(comm_count):
            comm_data = {
                "company_id": company["id"],
                "communication_date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                "communication_type": random.choice(["电话", "微信", "面谈", "邮件", "视频会议"]),
                "content": f"与{company['name']}的第{j+1}次沟通：\n" + 
                          random.choice([
                              "讨论了项目具体需求和证书配置方案",
                              "确认了合作价格和服务期限",
                              "了解了项目进度和人员需求时间",
                              "沟通了证书专业要求和人员资质",
                              "商讨了长期合作的可能性"
                          ]),
                "follow_up_required": random.choice([True, False]),
                "follow_up_date": (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d") if random.choice([True, False]) else None
            }
            
            try:
                response = requests.post(f"{BASE_URL}/communications/", json=comm_data)
                if response.status_code == 200:
                    print(f"✓ 创建沟通记录成功: {company['name']}")
                else:
                    print(f"✗ 创建沟通记录失败: {company['name']} - {response.text}")
            except Exception as e:
                print(f"✗ 创建沟通记录异常: {company['name']} - {e}")

def main():
    """主函数"""
    print("开始创建公司测试数据...")
    
    # 创建公司
    companies = create_companies()
    print(f"\n成功创建 {len(companies)} 个公司")
    
    # 创建公司沟通记录
    if companies:
        create_company_communications(companies)
    
    print("\n=== 公司测试数据创建完成 ===")

if __name__ == "__main__":
    main()
