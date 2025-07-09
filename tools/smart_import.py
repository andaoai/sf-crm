#!/usr/bin/env python3
"""
智能数据导入脚本 - 分析证书信息并自动分类
"""

import pandas as pd
import requests
import re
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api"

def extract_certificate_level(text):
    """提取证书等级"""
    if not text:
        return None
    text = str(text).lower()

    # 建造师等级
    if any(keyword in text for keyword in ["一建", "一级建造师", "考一建", "备考一建", "增项一建"]):
        return "一级"
    elif any(keyword in text for keyword in ["二建", "二级建造师", "2建", "二级"]):
        return "二级"

    # 工程师等级
    elif any(keyword in text for keyword in ["高级工程师", "高工", "正高级工程师"]):
        return "高级工程师"
    elif any(keyword in text for keyword in ["中级工程师", "中工", "工程师"]) and "高级" not in text and "初级" not in text:
        return "中级工程师"
    elif any(keyword in text for keyword in ["初级工程师", "助理工程师", "技术员"]):
        return "初级工程师"

    # 三类人员
    elif any(keyword in text for keyword in ["三类人员a", "a类", "企业主要负责人", "法定代表人"]):
        return "三类人员A类"
    elif any(keyword in text for keyword in ["三类人员b", "b类", "项目负责人", "项目经理"]):
        return "三类人员B类"
    elif any(keyword in text for keyword in ["三类人员c", "c类", "安全员", "专职安全", "c1", "c2", "c3"]):
        return "三类人员C类"

    return None

def extract_certificate_specialty(text):
    """提取证书专业"""
    if not text:
        return None

    text = str(text)

    # 专业关键词映射，按优先级排序（长关键词优先）
    specialty_mapping = [
        # 建造师专业
        ("建筑工程", "建筑工程"),
        ("市政公用工程", "市政公用工程"),
        ("机电工程", "机电工程"),
        ("公路工程", "公路工程"),
        ("水利水电工程", "水利水电工程"),
        ("矿业工程", "矿业工程"),
        ("铁路工程", "铁路工程"),
        ("民航机场工程", "民航机场工程"),
        ("港口与航道工程", "港口与航道工程"),
        ("通信与广电工程", "通信与广电工程"),
        # 建造师简称映射
        ("房建", "建筑工程"),
        ("建筑", "建筑工程"),
        ("市政", "市政公用工程"),
        ("机电", "机电工程"),
        ("公路", "公路工程"),
        ("水利水电", "水利水电工程"),
        ("水利", "水利水电工程"),
        ("矿业", "矿业工程"),
        ("铁路", "铁路工程"),
        ("民航机场", "民航机场工程"),
        ("民航", "民航机场工程"),
        ("港口与航道", "港口与航道工程"),
        ("港口", "港口与航道工程"),
        ("航道", "港口与航道工程"),
        ("通信与广电", "通信与广电工程"),
        ("通信", "通信与广电工程"),
        ("广电", "通信与广电工程"),

        # 工程师专业
        ("建筑工程师", "建筑工程师"),
        ("结构工程师", "结构工程师"),
        ("电气工程师", "电气工程师"),
        ("给排水工程师", "给排水工程师"),
        ("暖通工程师", "暖通工程师"),
        ("建筑设计工程师", "建筑设计工程师"),
        ("工程造价工程师", "工程造价工程师"),
        ("造价工程师", "工程造价工程师"),
        ("测绘工程师", "测绘工程师"),
        ("岩土工程师", "岩土工程师"),
        ("建筑材料工程师", "建筑材料工程师"),

        # 三类人员
        ("安全员", "安全管理"),
        ("安全管理", "安全管理"),
        ("专职安全", "安全管理")
    ]

    # 按关键词长度排序，优先匹配长关键词
    for keyword, specialty in specialty_mapping:
        if keyword in text:
            return specialty

    return None

def extract_social_security_status(text):
    """提取社保情况"""
    if not text:
        return None
    text = str(text).lower()

    # 检查无社保的关键词
    no_social_keywords = ["无社保", "没有社保", "社保不配合", "不配合", "社保公积金"]
    if any(keyword in text for keyword in no_social_keywords):
        return "无社保"

    # 检查唯一社保的关键词
    unique_social_keywords = ["唯一社保", "独立社保", "单独社保"]
    if any(keyword in text for keyword in unique_social_keywords):
        return "唯一社保"

    return None

def extract_expiry_date(text):
    """提取证书到期时间"""
    if not text:
        return None
    
    # 匹配各种日期格式
    date_patterns = [
        r'(\d{4})年(\d{1,2})月',
        r'(\d{1,2})月(\d{1,2})[号日]',
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
        r'(\d{1,2})/(\d{1,2})/(\d{4})',
        r'(\d{1,2})月.*?到期',
        r'(\d{4})年.*?到期'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, str(text))
        if match:
            try:
                # 这里可以根据匹配的格式进行日期解析
                # 暂时返回None，需要更复杂的日期解析逻辑
                return None
            except:
                continue
    return None

def extract_contract_price(text):
    """提取合同价格"""
    if not text:
        return None

    text_str = str(text)

    # 更精确的价格匹配模式
    price_patterns = [
        r'挂了(\d+\.?\d*)[万w]',           # 挂了2w
        r'挂.*?(\d+\.?\d*)[万w]',          # 挂xxx2w
        r'报价.*?(\d+\.?\d*)[万w]?',       # 报价3.5, 报价2.2
        r'价格.*?(\d+\.?\d*)[万w]?',       # 价格2.7w
        r'(\d+\.?\d*)[万w]',               # 直接的数字+万
        r'(\d+\.?\d*)w',                   # 数字+w
        r'当时挂了(\d+\.?\d*)[万w]',       # 当时挂了2w
    ]

    for pattern in price_patterns:
        match = re.search(pattern, text_str)
        if match:
            try:
                price = float(match.group(1))
                # 判断是否需要转换单位
                if 'w' in text_str.lower() or '万' in text_str or price < 100:
                    price = price * 10000
                return price
            except:
                continue
    return None

def format_phone_number(phone):
    """格式化电话号码"""
    if pd.isna(phone):
        return None
    
    phone_str = str(phone).strip()
    if phone_str == 'nan' or not phone_str:
        return None
    
    # 处理科学计数法
    try:
        if 'e+' in phone_str.lower():
            phone_num = int(float(phone_str))
            return str(phone_num)
        else:
            # 移除非数字字符
            phone_clean = re.sub(r'[^\d]', '', phone_str)
            if len(phone_clean) >= 10:
                return phone_clean
    except:
        pass
    
    return None

def clear_all_data():
    """清空所有现有数据"""
    try:
        # 获取所有人才数据
        response = requests.get(f"{API_BASE_URL}/talents/")
        if response.status_code == 200:
            talents = response.json().get('talents', [])
            print(f"找到 {len(talents)} 条人才记录，开始删除...")
            
            deleted_count = 0
            for talent in talents:
                delete_response = requests.delete(f"{API_BASE_URL}/talents/{talent['id']}")
                if delete_response.status_code == 200:
                    deleted_count += 1
                    print(f"✓ 删除人才记录 {talent['name']} (ID: {talent['id']})")
                else:
                    print(f"✗ 删除失败: {talent['name']} (ID: {talent['id']})")
            
            print(f"\n✅ 成功删除 {deleted_count} 条记录")
            return True
    except Exception as e:
        print(f"❌ 清空数据失败: {e}")
        return False

def analyze_and_import_data():
    """分析Excel数据并智能导入"""
    try:
        # 读取Excel文件
        df = pd.read_excel('意向客户表.xlsx')
        print(f"📊 读取到 {len(df)} 行数据")
        
        success_count = 0
        error_count = 0
        
        # 处理第一行作为标题行的情况
        first_row = df.iloc[0]
        name = str(first_row.iloc[0]).strip() if pd.notna(first_row.iloc[0]) else ""
        
        if name:  # 第一行有姓名，作为数据处理
            all_rows = df
        else:  # 第一行可能是标题，跳过
            all_rows = df.iloc[1:]
        
        for index, row in all_rows.iterrows():
            try:
                # 提取基础信息
                name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
                if not name or name == 'nan':
                    continue
                
                phone = format_phone_number(row.iloc[2]) if len(row) > 2 else None
                cert_info = str(row.iloc[3]).strip() if len(row) > 3 and pd.notna(row.iloc[3]) else ""
                note = str(row.iloc[4]).strip() if len(row) > 4 and pd.notna(row.iloc[4]) else ""
                
                # 合并证书信息和备注
                full_info = cert_info
                if note and note != 'nan':
                    full_info = f"{cert_info} | {note}" if cert_info else note
                
                # 智能提取各字段
                certificate_level = extract_certificate_level(full_info)
                certificate_specialty = extract_certificate_specialty(full_info)
                social_security_status = extract_social_security_status(full_info)
                contract_price = extract_contract_price(full_info)
                
                # 构建人才数据
                talent_data = {
                    "name": name,
                    "phone": phone,
                    "certificate_info": cert_info if cert_info and cert_info != 'nan' else None,
                    "wechat_note": note if note and note != 'nan' else None,
                    "communication_content": full_info if full_info else None,
                    "certificate_level": certificate_level,
                    "certificate_specialty": certificate_specialty,
                    "social_security_status": social_security_status,
                    "contract_price": contract_price,
                    "intention_level": "A" if certificate_level == "一级" else ("B" if certificate_level == "二级" else "C")
                }
                
                # 发送API请求
                response = requests.post(f"{API_BASE_URL}/talents/", json=talent_data)
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"✓ {name} - 等级:{certificate_level or '未知'} 专业:{certificate_specialty or '未知'} 社保:{social_security_status or '未知'}")
                else:
                    error_count += 1
                    print(f"✗ {name} - 导入失败: {response.text}")
                    
            except Exception as e:
                error_count += 1
                print(f"✗ 处理第{index}行数据失败: {e}")
        
        print(f"\n📈 导入完成!")
        print(f"✅ 成功: {success_count} 条")
        print(f"❌ 失败: {error_count} 条")
        
    except Exception as e:
        print(f"❌ 导入过程失败: {e}")

if __name__ == "__main__":
    print("🔄 智能数据导入工具")
    print("=" * 50)
    
    # 检查API连接
    try:
        response = requests.get(f"{API_BASE_URL}/talents/")
        if response.status_code != 200:
            print("❌ API连接失败，请确保后端服务正在运行")
            exit(1)
        print("✅ API连接正常")
    except:
        print("❌ 无法连接到API服务")
        exit(1)
    
    # 确认清空数据
    confirm = input("\n⚠️  确定要删除所有现有数据并重新导入吗？(输入 'YES' 确认): ")
    if confirm == "YES":
        print("\n🗑️  清空现有数据...")
        if clear_all_data():
            print("\n📥 开始智能导入...")
            analyze_and_import_data()
        else:
            print("❌ 清空数据失败，停止导入")
    else:
        print("操作已取消")
