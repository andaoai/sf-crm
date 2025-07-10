"""
创建证书类型测试数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.certificate import CertificateType

def create_certificate_types():
    """创建证书类型测试数据"""
    db = next(get_db())
    
    # 检查是否已有数据
    existing_count = db.query(CertificateType).count()
    if existing_count > 0:
        print(f"已存在 {existing_count} 个证书类型，跳过创建")
        return
    
    certificate_types = [
        # 建造师类
        {"type_code": "JZS1", "type_name": "一级建造师", "category": "建造师", "description": "一级建造师执业资格"},
        {"type_code": "JZS2", "type_name": "二级建造师", "category": "建造师", "description": "二级建造师执业资格"},
        
        # 造价工程师类
        {"type_code": "ZJ1", "type_name": "一级造价工程师", "category": "造价工程师", "description": "一级造价工程师执业资格"},
        {"type_code": "ZJ2", "type_name": "二级造价工程师", "category": "造价工程师", "description": "二级造价工程师执业资格"},
        
        # 监理工程师类
        {"type_code": "JL", "type_name": "监理工程师", "category": "监理工程师", "description": "监理工程师执业资格"},
        
        # 结构工程师类
        {"type_code": "JG1", "type_name": "一级结构工程师", "category": "结构工程师", "description": "一级注册结构工程师"},
        {"type_code": "JG2", "type_name": "二级结构工程师", "category": "结构工程师", "description": "二级注册结构工程师"},
        
        # 建筑师类
        {"type_code": "JZS_REG1", "type_name": "一级注册建筑师", "category": "注册建筑师", "description": "一级注册建筑师"},
        {"type_code": "JZS_REG2", "type_name": "二级注册建筑师", "category": "注册建筑师", "description": "二级注册建筑师"},
        
        # 安全工程师类
        {"type_code": "AQ", "type_name": "注册安全工程师", "category": "安全工程师", "description": "注册安全工程师"},
        
        # 消防工程师类
        {"type_code": "XF1", "type_name": "一级消防工程师", "category": "消防工程师", "description": "一级注册消防工程师"},
        {"type_code": "XF2", "type_name": "二级消防工程师", "category": "消防工程师", "description": "二级注册消防工程师"},
        
        # 电气工程师类
        {"type_code": "DQ", "type_name": "注册电气工程师", "category": "电气工程师", "description": "注册电气工程师"},
        
        # 给排水工程师类
        {"type_code": "GPS", "type_name": "给排水工程师", "category": "给排水工程师", "description": "注册给排水工程师"},
        
        # 暖通工程师类
        {"type_code": "NT", "type_name": "暖通工程师", "category": "暖通工程师", "description": "注册暖通工程师"},
        
        # 岩土工程师类
        {"type_code": "YT", "type_name": "岩土工程师", "category": "岩土工程师", "description": "注册岩土工程师"},
        
        # 环保工程师类
        {"type_code": "HB", "type_name": "环保工程师", "category": "环保工程师", "description": "注册环保工程师"},
        
        # 化工工程师类
        {"type_code": "HG", "type_name": "化工工程师", "category": "化工工程师", "description": "注册化工工程师"},
        
        # 城乡规划师类
        {"type_code": "CXGH", "type_name": "城乡规划师", "category": "城乡规划师", "description": "注册城乡规划师"},
        
        # 咨询工程师类
        {"type_code": "ZX", "type_name": "咨询工程师", "category": "咨询工程师", "description": "注册咨询工程师"},
    ]
    
    try:
        for cert_type_data in certificate_types:
            cert_type = CertificateType(**cert_type_data)
            db.add(cert_type)
        
        db.commit()
        print(f"✓ 成功创建 {len(certificate_types)} 个证书类型")
        
        # 显示创建的证书类型
        print("\n创建的证书类型:")
        for cert_type in certificate_types:
            print(f"  {cert_type['category']}: {cert_type['type_name']}")
            
    except Exception as e:
        db.rollback()
        print(f"✗ 创建证书类型失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_certificate_types()
