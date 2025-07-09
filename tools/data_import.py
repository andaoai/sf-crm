#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据导入脚本 - 从Excel文件导入数据到CRM系统
"""

import pandas as pd
import requests
import json
from datetime import datetime
import sys
import os

# API配置
API_BASE_URL = "http://localhost:8000/api"
TALENTS_API = f"{API_BASE_URL}/talents/"
COMPANIES_API = f"{API_BASE_URL}/companies/"

def read_excel_file(file_path):
    """读取Excel文件"""
    try:
        # 读取Excel文件，不使用第一行作为列名
        df = pd.read_excel(file_path, header=None)

        # 根据数据结构设置列名
        if len(df.columns) >= 4:
            df.columns = ['姓名', '身份证', '电话', '证书信息', '备注'][:len(df.columns)]
        else:
            # 如果列数不够，使用通用列名
            df.columns = [f'列{i+1}' for i in range(len(df.columns))]

        print(f"成功读取Excel文件，共 {len(df)} 行数据")
        print("列名:", df.columns.tolist())
        print("\n前5行数据预览:")
        print(df.head())
        return df
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return None

def clean_data(df):
    """清理数据"""
    # 填充空值
    df = df.fillna('')
    
    # 转换数据类型
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    
    return df

def extract_certificate_info(cert_text):
    """从证书信息中提取等级和专业"""
    if not cert_text:
        return None, None

    cert_text = str(cert_text).strip()

    # 提取证书等级
    certificate_level = None
    if "一建" in cert_text or "一级建造师" in cert_text:
        certificate_level = "一级"
    elif "二建" in cert_text or "二级建造师" in cert_text:
        certificate_level = "二级"
    else:
        certificate_level = "其他"

    # 提取证书专业
    certificate_specialty = None
    specialty_mapping = {
        "房建": "建筑工程",
        "建筑": "建筑工程",
        "建筑工程": "建筑工程",
        "市政": "市政公用工程",
        "市政公用工程": "市政公用工程",
        "机电": "机电工程",
        "机电工程": "机电工程",
        "公路": "公路工程",
        "公路工程": "公路工程",
        "水利": "水利水电工程",
        "水利水电": "水利水电工程",
        "水利水电工程": "水利水电工程",
        "矿业": "矿业工程",
        "矿业工程": "矿业工程",
        "铁路": "铁路工程",
        "铁路工程": "铁路工程",
        "民航": "民航机场工程",
        "民航机场": "民航机场工程",
        "民航机场工程": "民航机场工程",
        "港口": "港口与航道工程",
        "航道": "港口与航道工程",
        "港口与航道": "港口与航道工程",
        "港口与航道工程": "港口与航道工程",
        "通信": "通信与广电工程",
        "广电": "通信与广电工程",
        "通信与广电": "通信与广电工程",
        "通信与广电工程": "通信与广电工程"
    }

    for keyword, specialty in specialty_mapping.items():
        if keyword in cert_text:
            certificate_specialty = specialty
            break

    return certificate_level, certificate_specialty

def map_excel_to_talent(row):
    """将Excel行数据映射到人才数据结构"""
    talent_data = {
        "name": "",
        "gender": None,
        "age": None,
        "phone": None,
        "wechat_note": None,
        "certificate_info": None,
        "certificate_expiry_date": None,
        "contract_price": None,
        "intention_level": "C",
        "communication_content": None,
        "certificate_level": None,
        "certificate_specialty": None,
        "social_security_status": None
    }
    
    # 根据Excel列名映射数据
    columns = row.index.tolist()

    # 直接按列位置映射数据（基于观察到的数据结构）
    if len(columns) >= 1 and pd.notna(row.iloc[0]):
        talent_data["name"] = str(row.iloc[0]).strip()

    if len(columns) >= 3 and pd.notna(row.iloc[2]):
        # 电话号码处理
        phone_str = str(row.iloc[2]).strip()
        if phone_str and phone_str != 'nan':
            # 处理科学计数法格式的电话号码
            try:
                if 'e+' in phone_str.lower():
                    phone_num = int(float(phone_str))
                    talent_data["phone"] = str(phone_num)
                else:
                    talent_data["phone"] = phone_str
            except:
                talent_data["phone"] = phone_str

    if len(columns) >= 4 and pd.notna(row.iloc[3]):
        # 证书信息和备注
        cert_info = str(row.iloc[3]).strip()
        if cert_info and cert_info != 'nan':
            talent_data["certificate_info"] = cert_info
            # 提取证书等级和专业
            cert_level, cert_specialty = extract_certificate_info(cert_info)
            if cert_level:
                talent_data["certificate_level"] = cert_level
            if cert_specialty:
                talent_data["certificate_specialty"] = cert_specialty

    if len(columns) >= 5 and pd.notna(row.iloc[4]):
        # 备注信息
        note_info = str(row.iloc[4]).strip()
        if note_info and note_info != 'nan':
            if talent_data["certificate_info"]:
                talent_data["certificate_info"] += " | " + note_info
            else:
                talent_data["wechat_note"] = note_info

    # 根据证书信息推断意向等级
    if talent_data["certificate_info"]:
        cert_lower = talent_data["certificate_info"].lower()
        if '一建' in cert_lower or '一级建造师' in cert_lower:
            talent_data["intention_level"] = "A"
        elif '二建' in cert_lower or '二级建造师' in cert_lower:
            talent_data["intention_level"] = "B"
    
    return talent_data

def map_excel_to_company(row):
    """将Excel行数据映射到公司数据结构"""
    company_data = {
        "name": "",
        "contact_info": None,
        "intention": None,
        "intention_level": "C",
        "price": None,
        "certificate_requirements": None,
        "communication_notes": None
    }
    
    # 根据Excel列名映射数据
    columns = row.index.tolist()
    
    for col in columns:
        col_lower = col.lower()
        if '公司' in col or 'company' in col_lower or '企业' in col:
            company_data["name"] = str(row[col]) if pd.notna(row[col]) else ""
        elif '联系' in col or 'contact' in col_lower:
            company_data["contact_info"] = str(row[col]) if pd.notna(row[col]) else None
        elif '意向' in col and '等级' not in col:
            company_data["intention"] = str(row[col]) if pd.notna(row[col]) else None
        elif '意向等级' in col or 'intention_level' in col_lower:
            intention_str = str(row[col]).upper()
            if 'A' in intention_str or '高' in intention_str:
                company_data["intention_level"] = "A"
            elif 'B' in intention_str or '中' in intention_str:
                company_data["intention_level"] = "B"
            else:
                company_data["intention_level"] = "C"
        elif '价格' in col or 'price' in col_lower:
            company_data["price"] = str(row[col]) if pd.notna(row[col]) else None
        elif '证书需求' in col or 'certificate' in col_lower:
            company_data["certificate_requirements"] = str(row[col]) if pd.notna(row[col]) else None
        elif '备注' in col or 'note' in col_lower:
            company_data["communication_notes"] = str(row[col]) if pd.notna(row[col]) else None
    
    return company_data

def create_talent(talent_data):
    """创建人才记录"""
    try:
        response = requests.post(TALENTS_API, json=talent_data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"创建人才失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"创建人才异常: {e}")
        return None

def create_company(company_data):
    """创建公司记录"""
    try:
        response = requests.post(COMPANIES_API, json=company_data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"创建公司失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"创建公司异常: {e}")
        return None

def import_data(file_path, data_type="talent"):
    """导入数据主函数"""
    # 读取Excel文件
    df = read_excel_file(file_path)
    if df is None:
        return
    
    # 清理数据
    df = clean_data(df)
    
    success_count = 0
    error_count = 0
    
    print(f"\n开始导入 {data_type} 数据...")
    
    for index, row in df.iterrows():
        try:
            if data_type == "talent":
                mapped_data = map_excel_to_talent(row)
                if mapped_data["name"]:  # 确保有姓名
                    result = create_talent(mapped_data)
                    if result:
                        success_count += 1
                        print(f"✓ 成功创建人才: {mapped_data['name']}")
                    else:
                        error_count += 1
                        print(f"✗ 创建人才失败: {mapped_data['name']}")
                else:
                    error_count += 1
                    print(f"✗ 跳过无姓名记录: 行 {index + 1}")
            
            elif data_type == "company":
                mapped_data = map_excel_to_company(row)
                if mapped_data["name"]:  # 确保有公司名
                    result = create_company(mapped_data)
                    if result:
                        success_count += 1
                        print(f"✓ 成功创建公司: {mapped_data['name']}")
                    else:
                        error_count += 1
                        print(f"✗ 创建公司失败: {mapped_data['name']}")
                else:
                    error_count += 1
                    print(f"✗ 跳过无公司名记录: 行 {index + 1}")
        
        except Exception as e:
            error_count += 1
            print(f"✗ 处理第 {index + 1} 行数据时出错: {e}")
    
    print(f"\n导入完成!")
    print(f"成功: {success_count} 条")
    print(f"失败: {error_count} 条")
    print(f"总计: {success_count + error_count} 条")

def check_api_connection():
    """检查API连接"""
    try:
        response = requests.get(f"{API_BASE_URL}/talents/")
        if response.status_code == 200:
            print("✓ API连接正常")
            return True
        else:
            print(f"✗ API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API连接异常: {e}")
        return False

if __name__ == "__main__":
    # 检查文件是否存在
    excel_file = "意向客户表.xlsx"
    if not os.path.exists(excel_file):
        print(f"错误: 找不到文件 {excel_file}")
        sys.exit(1)

    print("CRM数据导入工具")
    print("=" * 50)

    # 检查API连接
    if not check_api_connection():
        print("请确保后端服务正在运行 (http://localhost:8000)")
        sys.exit(1)

    # 让用户选择导入类型
    print("\n请选择导入数据类型:")
    print("1. 人才数据 (talent)")
    print("2. 公司数据 (company)")
    print("3. 先预览数据结构")
    print("4. 清空现有数据后重新导入")

    choice = input("请输入选择 (1/2/3/4): ").strip()

    if choice == "3":
        # 预览数据
        df = read_excel_file(excel_file)
        if df is not None:
            print("\n数据预览完成，请根据列名选择合适的导入类型")
    elif choice == "1":
        import_data(excel_file, "talent")
    elif choice == "2":
        import_data(excel_file, "company")
    elif choice == "4":
        confirm = input("⚠️  确定要清空所有现有数据吗？(输入 'YES' 确认): ")
        if confirm == "YES":
            print("清空数据功能需要手动实现...")
            print("建议通过数据库管理工具清空数据表")
        else:
            print("操作已取消")
    else:
        print("无效选择")
