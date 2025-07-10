#!/usr/bin/env python3
"""
直接数据库插入脚本 - 不依赖API，直接操作数据库
"""

import sys
import os
import psycopg2
import random
from datetime import datetime, timedelta
import uuid

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_db_connection():
    """获取数据库连接"""
    # Docker环境下的数据库连接参数
    db_config = {
        'host': 'postgres',  # Docker服务名
        'port': '5432',
        'database': 'crm_db',
        'user': 'crm_user',
        'password': 'crm_password'
    }
    
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        # 尝试本地连接
        try:
            local_config = {
                'host': 'localhost',
                'port': '5432',
                'database': 'crm_db',
                'user': 'crm_user',
                'password': 'crm_password'
            }
            conn = psycopg2.connect(**local_config)
            print("使用本地数据库连接")
            return conn
        except Exception as e2:
            print(f"本地数据库连接也失败: {e2}")
            raise

# 基础数据
PROVINCES = ["北京", "上海", "广东", "江苏", "浙江", "山东", "河南", "四川", "湖北", "湖南"]
CITIES = {
    "北京": ["朝阳区", "海淀区", "西城区", "东城区"],
    "上海": ["浦东新区", "黄浦区", "徐汇区", "静安区"],
    "广东": ["广州市", "深圳市", "东莞市", "佛山市"],
    "江苏": ["南京市", "苏州市", "无锡市", "常州市"],
    "浙江": ["杭州市", "宁波市", "温州市", "嘉兴市"],
    "山东": ["济南市", "青岛市", "烟台市", "潍坊市"],
    "河南": ["郑州市", "洛阳市", "开封市", "安阳市"],
    "四川": ["成都市", "绵阳市", "德阳市", "南充市"],
    "湖北": ["武汉市", "宜昌市", "襄阳市", "荆州市"],
    "湖南": ["长沙市", "株洲市", "湘潭市", "衡阳市"]
}

NAMES = [
    "张伟", "李娜", "王强", "刘敏", "陈杰", "杨丽", "赵磊", "孙静",
    "周涛", "吴琳", "郑浩", "王芳", "李明", "张静", "刘伟", "陈丽",
    "杨强", "赵敏", "孙杰", "周琳", "吴浩", "郑静", "王涛", "李丽"
]

CERTIFICATE_TYPES_DATA = [
    ("JZS1", "一级建造师", "建造师", "一级建造师执业资格证书"),
    ("JZS2", "二级建造师", "建造师", "二级建造师执业资格证书"),
    ("ZJ1", "一级造价工程师", "造价工程师", "一级造价工程师执业资格证书"),
    ("JL", "监理工程师", "监理工程师", "监理工程师执业资格证书"),
    ("JZS", "注册建筑师", "建筑师", "注册建筑师执业资格证书"),
    ("JGS", "注册结构师", "结构师", "注册结构师执业资格证书"),
    ("DQ", "注册电气工程师", "电气工程师", "注册电气工程师执业资格证书"),
    ("GPS", "注册给排水工程师", "给排水工程师", "注册给排水工程师执业资格证书")
]

CERTIFICATE_TYPES = ["一级建造师", "二级建造师", "一级造价工程师", "监理工程师", "注册建筑师", "注册结构师", "注册电气工程师", "注册给排水工程师"]
SPECIALTIES = ["建筑工程", "市政工程", "机电工程", "公路工程", "水利工程", "矿业工程", "通信工程", "港口工程", "民航工程", "铁路工程"]
LEVELS = ["一级", "二级", "高级", "中级", "初级"]

def insert_certificate_types():
    """插入证书类型数据"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("插入证书类型数据...")
        
        for i, (type_code, type_name, category, description) in enumerate(CERTIFICATE_TYPES_DATA):
            cursor.execute("""
                INSERT INTO certificate_types (type_code, type_name, category, description, is_active, sort_order, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (type_code) DO NOTHING
            """, (type_code, type_name, category, description, True, i+1, datetime.now()))
        
        conn.commit()
        print(f"✓ 成功插入 {len(CERTIFICATE_TYPES_DATA)} 个证书类型")
        return True
        
    except Exception as e:
        print(f"✗ 插入证书类型失败: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_talents():
    """插入人才数据"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("插入人才数据...")
        talents = []
        
        for i in range(20):
            province = random.choice(PROVINCES)
            city = random.choice(CITIES[province])
            
            talent_data = (
                random.choice(NAMES) + str(i+1),  # name
                random.choice(["男", "女"]),  # gender
                random.randint(25, 55),  # age
                f"1{random.randint(3,9)}{random.randint(100000000, 999999999)}",  # phone
                f"微信备注{i+1}",  # wechat_note
                random.randint(20000, 80000),  # contract_price
                random.choice(["A", "B", "C"]),  # intention_level
                province,  # province
                city,  # city
                f"{city}某某区某某街道{random.randint(1, 999)}号",  # address
                f"初次沟通记录{i+1}，人才表现积极",  # communication_content
                random.choice(["唯一社保", "无社保"]),  # social_security_status
                datetime.now(),  # created_at
                datetime.now()   # updated_at
            )
            
            cursor.execute("""
                INSERT INTO talents (name, gender, age, phone, wechat_note, contract_price, 
                                   intention_level, province, city, address, communication_content, 
                                   social_security_status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, talent_data)
            
            talent_id = cursor.fetchone()[0]
            talents.append({"id": talent_id, "name": talent_data[0]})
        
        conn.commit()
        print(f"✓ 成功插入 {len(talents)} 个人才")
        return talents
        
    except Exception as e:
        print(f"✗ 插入人才数据失败: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_certificates(talents):
    """插入证书数据"""
    if not talents:
        print("没有人才数据，跳过证书插入")
        return []
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("插入证书数据...")
        certificates = []
        
        for talent in talents:
            cert_count = random.randint(1, 3)  # 每个人才1-3个证书
            
            for j in range(cert_count):
                cert_id = str(uuid.uuid4())[:8].upper()
                cert_data = (
                    cert_id,  # certificate_id
                    talent["id"],  # talent_id
                    random.choice(CERTIFICATE_TYPES),  # certificate_type
                    f"{random.choice(CERTIFICATE_TYPES)}（{random.choice(SPECIALTIES)}）",  # certificate_name
                    f"CERT{random.randint(100000, 999999)}",  # certificate_number
                    (datetime.now() - timedelta(days=random.randint(365, 1825))).date(),  # issue_date
                    (datetime.now() + timedelta(days=random.randint(365, 1825))).date(),  # expiry_date
                    random.choice(["住建部", "人社部", "工信部", "交通部"]),  # issuing_authority
                    random.choice(SPECIALTIES),  # specialty
                    random.choice(LEVELS),  # level
                    random.choice(["VALID", "VALID", "VALID", "EXPIRED"]),  # status (大部分有效)
                    f"证书备注{j+1}",  # notes
                    datetime.now(),  # created_at
                    datetime.now()   # updated_at
                )
                
                cursor.execute("""
                    INSERT INTO certificates (certificate_id, talent_id, certificate_type, certificate_name,
                                            certificate_number, issue_date, expiry_date, issuing_authority,
                                            specialty, level, status, notes, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, cert_data)
                
                certificates.append({"id": cert_id, "talent_id": talent["id"]})
        
        conn.commit()
        print(f"✓ 成功插入 {len(certificates)} 个证书")
        return certificates
        
    except Exception as e:
        print(f"✗ 插入证书数据失败: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 公司数据
COMPANY_NAMES = [
    "北京建工集团有限责任公司", "上海建工集团股份有限公司", "中国建筑股份有限公司",
    "广州建筑集团有限公司", "深圳市建筑工务署", "杭州建工集团有限责任公司",
    "南京建工集团有限公司", "成都建工集团有限公司", "武汉建工集团股份有限公司",
    "长沙建工集团有限公司", "青岛建设集团有限公司", "大连建设集团有限公司",
    "天津建工集团（控股）有限公司", "重庆建工集团股份有限公司", "西安建工集团有限公司"
]

CONTACT_TEMPLATES = [
    "联系人：{name}\n电话：{phone}\n邮箱：{email}\n办公电话：{office_phone}\n微信：{wechat}\n地址：{address}",
    "负责人：{name}\n手机：{phone}\n企业邮箱：{email}\n座机：{office_phone}\n微信号：{wechat}\n公司地址：{address}",
    "项目经理：{name}\n联系电话：{phone}\n电子邮件：{email}\n固定电话：{office_phone}\n微信：{wechat}\n办公地址：{address}"
]

CONTACT_NAMES = [
    "张经理", "李总监", "王主任", "刘部长", "陈经理", "杨总", "赵主管",
    "孙经理", "周总监", "吴主任", "郑经理", "王总", "李主管", "张总监"
]

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

def insert_companies():
    """插入公司数据"""
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print("插入公司数据...")
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

            company_data = (
                company_name,  # name
                contact_info,  # contact_info
                f"与{company_name}的初步沟通记录，了解了项目需求和合作意向。",  # communication_notes
                f"有{random.choice(['住宅', '商业', '基础设施', '工业'])}项目合作需求，预计项目周期{random.randint(6, 24)}个月。",  # intention
                random.choice(["A", "B", "C"]),  # intention_level
                f"{random.randint(3, 15)}万/年",  # price
                random.choice(CERTIFICATE_REQUIREMENTS),  # certificate_requirements
                datetime.now(),  # created_at
                datetime.now()   # updated_at
            )

            cursor.execute("""
                INSERT INTO companies (name, contact_info, communication_notes, intention,
                                     intention_level, price, certificate_requirements, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, company_data)

            company_id = cursor.fetchone()[0]
            companies.append({"id": company_id, "name": company_name})

        conn.commit()
        print(f"✓ 成功插入 {len(companies)} 个公司")
        return companies

    except Exception as e:
        print(f"✗ 插入公司数据失败: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_communications(talents, companies):
    """插入沟通记录数据"""
    if not talents and not companies:
        print("没有人才或公司数据，跳过沟通记录插入")
        return []

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print("插入沟通记录数据...")
        communications = []

        # 为人才创建沟通记录
        for talent in talents[:10]:  # 只为前10个人才创建记录
            comm_data = (
                None,  # company_id
                talent["id"],  # talent_id
                f"与{talent['name']}的沟通记录",  # content
                random.choice(["电话沟通", "微信沟通", "面谈", "邮件沟通"]),  # communication_type
                datetime.now() - timedelta(days=random.randint(1, 30)),  # communication_date
                datetime.now(),  # created_at
                datetime.now()   # updated_at
            )

            cursor.execute("""
                INSERT INTO communications (company_id, talent_id, content, communication_type,
                                          communication_date, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, comm_data)

            comm_id = cursor.fetchone()[0]
            communications.append({"id": comm_id, "type": "talent"})

        # 为公司创建沟通记录
        for company in companies[:10]:  # 只为前10个公司创建记录
            comm_data = (
                company["id"],  # company_id
                None,  # talent_id
                f"与{company['name']}的项目洽谈记录",  # content
                random.choice(["电话沟通", "现场拜访", "邮件沟通", "视频会议"]),  # communication_type
                datetime.now() - timedelta(days=random.randint(1, 30)),  # communication_date
                datetime.now(),  # created_at
                datetime.now()   # updated_at
            )

            cursor.execute("""
                INSERT INTO communications (company_id, talent_id, content, communication_type,
                                          communication_date, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, comm_data)

            comm_id = cursor.fetchone()[0]
            communications.append({"id": comm_id, "type": "company"})

        conn.commit()
        print(f"✓ 成功插入 {len(communications)} 条沟通记录")
        return communications

    except Exception as e:
        print(f"✗ 插入沟通记录失败: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def main():
    """主函数"""
    print("=" * 50)
    print("直接数据库插入工具")
    print("=" * 50)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 插入证书类型
    if not insert_certificate_types():
        print("证书类型插入失败，终止操作")
        return

    # 2. 插入人才数据
    talents = insert_talents()
    if not talents:
        print("人才数据插入失败，终止操作")
        return

    # 3. 插入证书数据
    certificates = insert_certificates(talents)

    # 4. 插入公司数据
    companies = insert_companies()

    # 5. 插入沟通记录
    communications = insert_communications(talents, companies)

    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print("数据插入完成！")
    print(f"证书类型: {len(CERTIFICATE_TYPES_DATA)} 个")
    print(f"人才: {len(talents)} 个")
    print(f"证书: {len(certificates)} 个")
    print(f"公司: {len(companies)} 个")
    print(f"沟通记录: {len(communications)} 条")

if __name__ == "__main__":
    main()
