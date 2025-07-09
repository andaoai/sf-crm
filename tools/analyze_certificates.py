#!/usr/bin/env python3
"""
分析证书信息内容，帮助改进分类算法
"""

import requests
import pandas as pd

def analyze_current_data():
    """分析当前数据库中的证书信息"""
    response = requests.get('http://localhost:8000/api/talents/')
    if response.status_code != 200:
        print("❌ 无法获取数据")
        return
    
    talents = response.json().get('talents', [])
    
    print("📋 证书信息详细分析")
    print("=" * 80)
    
    # 按分类状态分组
    classified = []
    unclassified = []
    
    for talent in talents:
        cert_info = talent.get('certificate_info', '')
        level = talent.get('certificate_level')
        specialty = talent.get('certificate_specialty')
        social = talent.get('social_security_status')
        
        if level or specialty or social:
            classified.append(talent)
        else:
            unclassified.append(talent)
    
    print(f"✅ 已分类: {len(classified)} 人")
    print(f"❓ 未分类: {len(unclassified)} 人")
    
    print("\n🔍 未分类人员的证书信息:")
    print("-" * 80)
    for i, talent in enumerate(unclassified):
        cert_info = talent.get('certificate_info', '')
        comm_content = talent.get('communication_content', '')
        print(f"{i+1}. {talent['name']}")
        print(f"   证书信息: {cert_info}")
        if comm_content and comm_content != cert_info:
            print(f"   沟通内容: {comm_content}")
        print()
    
    print("\n🎯 已分类人员样本:")
    print("-" * 80)
    for i, talent in enumerate(classified[:10]):
        cert_info = talent.get('certificate_info', '')
        level = talent.get('certificate_level', '未知')
        specialty = talent.get('certificate_specialty', '未知')
        social = talent.get('social_security_status', '未知')
        print(f"{i+1}. {talent['name']} - 等级:{level} 专业:{specialty} 社保:{social}")
        print(f"   原文: {cert_info}")
        print()

def analyze_excel_data():
    """分析Excel原始数据"""
    try:
        df = pd.read_excel('意向客户表.xlsx')
        print("\n📊 Excel原始数据分析")
        print("=" * 80)
        
        # 分析证书信息列
        cert_column = df.iloc[:, 3] if len(df.columns) > 3 else None
        if cert_column is not None:
            print("🔍 证书信息样本:")
            print("-" * 40)
            
            unique_certs = cert_column.dropna().unique()
            for i, cert in enumerate(unique_certs[:15]):
                print(f"{i+1}. {cert}")
            
            print(f"\n总共 {len(unique_certs)} 种不同的证书信息")
            
            # 关键词分析
            all_text = ' '.join(cert_column.dropna().astype(str))
            
            level_keywords = {
                '一建': all_text.count('一建'),
                '一级建造师': all_text.count('一级建造师'),
                '二建': all_text.count('二建'),
                '二级建造师': all_text.count('二级建造师'),
                '考一建': all_text.count('考一建'),
                '备考一建': all_text.count('备考一建')
            }
            
            specialty_keywords = {
                '房建': all_text.count('房建'),
                '建筑': all_text.count('建筑'),
                '市政': all_text.count('市政'),
                '机电': all_text.count('机电'),
                '公路': all_text.count('公路'),
                '水利': all_text.count('水利'),
                '矿业': all_text.count('矿业')
            }
            
            social_keywords = {
                '社保': all_text.count('社保'),
                '不配合': all_text.count('不配合'),
                '无社保': all_text.count('无社保'),
                '唯一社保': all_text.count('唯一社保')
            }
            
            print("\n📈 关键词频率统计:")
            print("等级关键词:")
            for keyword, count in level_keywords.items():
                if count > 0:
                    print(f"  {keyword}: {count}次")
            
            print("专业关键词:")
            for keyword, count in specialty_keywords.items():
                if count > 0:
                    print(f"  {keyword}: {count}次")
            
            print("社保关键词:")
            for keyword, count in social_keywords.items():
                if count > 0:
                    print(f"  {keyword}: {count}次")
                    
    except Exception as e:
        print(f"❌ 分析Excel数据失败: {e}")

def suggest_improvements():
    """建议改进方案"""
    print("\n💡 改进建议:")
    print("=" * 80)
    print("1. 证书等级识别:")
    print("   - 添加更多一建相关关键词: '考一建', '备考一建', '增项', '一级'")
    print("   - 处理复合描述: '二建转一建', '二建考一建'")
    
    print("\n2. 证书专业识别:")
    print("   - 添加简称映射: '房建'→'建筑工程'")
    print("   - 处理多专业: '双专业', '机电+市政'")
    
    print("\n3. 社保情况识别:")
    print("   - 扩展关键词: '社保公积金', '配合社保'")
    print("   - 地域信息: '在云南有社保'")
    
    print("\n4. 价格信息提取:")
    print("   - 价格模式: '挂了2w', '报价3.5', '价格2.2'")
    print("   - 单位转换: 万元转换为具体数字")
    
    print("\n5. 到期时间提取:")
    print("   - 时间模式: '11月到期', '9月份到期', '25年9月'")

if __name__ == "__main__":
    analyze_current_data()
    analyze_excel_data()
    suggest_improvements()
