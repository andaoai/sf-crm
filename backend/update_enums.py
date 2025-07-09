#!/usr/bin/env python3
"""
更新枚举类型 - 添加工程师和三类人员分类
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine

def update_certificate_enums():
    """更新证书等级和专业枚举类型"""
    
    update_sql = """
    -- 更新证书等级枚举类型
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '初级工程师';
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '中级工程师';
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '高级工程师';
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '三类人员A类';
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '三类人员B类';
    ALTER TYPE certificatelevel ADD VALUE IF NOT EXISTS '三类人员C类';
    
    -- 更新证书专业枚举类型
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '建筑工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '结构工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '电气工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '给排水工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '暖通工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '建筑设计工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '工程造价工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '测绘工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '岩土工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '建筑材料工程师';
    ALTER TYPE certificatespecialty ADD VALUE IF NOT EXISTS '安全管理';
    """
    
    try:
        with engine.connect() as connection:
            # 分别执行每个ALTER语句
            statements = [stmt.strip() for stmt in update_sql.split(';') if stmt.strip()]
            for statement in statements:
                try:
                    connection.execute(text(statement))
                    print(f"✓ 执行成功: {statement[:50]}...")
                except Exception as e:
                    if "already exists" in str(e) or "duplicate key value" in str(e):
                        print(f"⚠️  已存在: {statement[:50]}...")
                    else:
                        print(f"❌ 执行失败: {statement[:50]}... - {e}")
            
            connection.commit()
            
        print("\n✅ 枚举类型更新完成！")
        print("新增证书等级:")
        print("- 初级工程师、中级工程师、高级工程师")
        print("- 三类人员A类、三类人员B类、三类人员C类")
        print("\n新增证书专业:")
        print("- 建筑工程师、结构工程师、电气工程师、给排水工程师")
        print("- 暖通工程师、建筑设计工程师、工程造价工程师、测绘工程师")
        print("- 岩土工程师、建筑材料工程师、安全管理")
        
    except Exception as e:
        print(f"❌ 枚举类型更新失败: {e}")
        return False
    
    return True

def check_enum_values():
    """检查枚举类型的值"""
    check_sql = """
    SELECT enumlabel 
    FROM pg_enum 
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'certificatelevel')
    ORDER BY enumlabel;
    """
    
    check_specialty_sql = """
    SELECT enumlabel 
    FROM pg_enum 
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'certificatespecialty')
    ORDER BY enumlabel;
    """
    
    try:
        with engine.connect() as connection:
            print("\n📋 当前证书等级枚举值:")
            result = connection.execute(text(check_sql))
            levels = result.fetchall()
            for level in levels:
                print(f"- {level[0]}")
            
            print("\n📋 当前证书专业枚举值:")
            result = connection.execute(text(check_specialty_sql))
            specialties = result.fetchall()
            for specialty in specialties:
                print(f"- {specialty[0]}")
                
    except Exception as e:
        print(f"❌ 检查枚举值失败: {e}")

if __name__ == "__main__":
    print("🔄 更新证书枚举类型")
    print("=" * 50)
    
    # 检查当前状态
    print("检查当前枚举值...")
    check_enum_values()
    
    # 询问是否执行更新
    choice = input("\n是否执行枚举类型更新？(y/N): ").strip().lower()
    
    if choice == 'y':
        if update_certificate_enums():
            print("\n🎉 更新完成！现在可以重启后端服务。")
            check_enum_values()
        else:
            print("\n💥 更新失败！请检查错误信息。")
    else:
        print("取消更新操作。")
