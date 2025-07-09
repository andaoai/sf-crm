#!/usr/bin/env python3
"""
重新创建枚举类型 - 清理并重建
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine

def recreate_enums():
    """重新创建枚举类型"""
    
    recreate_sql = """
    -- 删除现有字段的枚举约束
    ALTER TABLE talents ALTER COLUMN certificate_level DROP DEFAULT;
    ALTER TABLE talents ALTER COLUMN certificate_specialty DROP DEFAULT;
    ALTER TABLE talents ALTER COLUMN social_security_status DROP DEFAULT;
    
    -- 将字段改为文本类型
    ALTER TABLE talents ALTER COLUMN certificate_level TYPE TEXT;
    ALTER TABLE talents ALTER COLUMN certificate_specialty TYPE TEXT;
    ALTER TABLE talents ALTER COLUMN social_security_status TYPE TEXT;
    
    -- 删除旧的枚举类型
    DROP TYPE IF EXISTS certificatelevel CASCADE;
    DROP TYPE IF EXISTS certificatespecialty CASCADE;
    DROP TYPE IF EXISTS socialsecuritystatus CASCADE;
    
    -- 创建新的枚举类型
    CREATE TYPE certificatelevel AS ENUM (
        '一级', '二级', 
        '初级工程师', '中级工程师', '高级工程师',
        '三类人员A类', '三类人员B类', '三类人员C类',
        '其他'
    );
    
    CREATE TYPE certificatespecialty AS ENUM (
        '建筑工程', '市政公用工程', '机电工程', '公路工程', 
        '水利水电工程', '矿业工程', '铁路工程', '民航机场工程', 
        '港口与航道工程', '通信与广电工程',
        '建筑工程师', '结构工程师', '电气工程师', '给排水工程师',
        '暖通工程师', '建筑设计工程师', '工程造价工程师', '测绘工程师',
        '岩土工程师', '建筑材料工程师', '安全管理'
    );
    
    CREATE TYPE socialsecuritystatus AS ENUM ('唯一社保', '无社保');
    
    -- 将字段改回枚举类型
    ALTER TABLE talents ALTER COLUMN certificate_level TYPE certificatelevel USING certificate_level::certificatelevel;
    ALTER TABLE talents ALTER COLUMN certificate_specialty TYPE certificatespecialty USING certificate_specialty::certificatespecialty;
    ALTER TABLE talents ALTER COLUMN social_security_status TYPE socialsecuritystatus USING social_security_status::socialsecuritystatus;
    """
    
    try:
        with engine.connect() as connection:
            # 分别执行每个语句
            statements = [stmt.strip() for stmt in recreate_sql.split(';') if stmt.strip()]
            for i, statement in enumerate(statements):
                try:
                    print(f"执行语句 {i+1}/{len(statements)}: {statement[:50]}...")
                    connection.execute(text(statement))
                except Exception as e:
                    print(f"⚠️  语句 {i+1} 执行失败: {e}")
                    # 继续执行其他语句
            
            connection.commit()
            
        print("\n✅ 枚举类型重建完成！")
        
        # 验证新的枚举值
        with engine.connect() as connection:
            print("\n📋 新的证书等级枚举值:")
            result = connection.execute(text("""
                SELECT enumlabel FROM pg_enum 
                WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'certificatelevel')
                ORDER BY enumlabel
            """))
            for row in result:
                print(f"  - {row[0]}")
            
            print("\n📋 新的证书专业枚举值:")
            result = connection.execute(text("""
                SELECT enumlabel FROM pg_enum 
                WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'certificatespecialty')
                ORDER BY enumlabel
            """))
            for row in result:
                print(f"  - {row[0]}")
        
    except Exception as e:
        print(f"❌ 枚举类型重建失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 重建证书枚举类型")
    print("=" * 50)
    
    choice = input("确定要重建枚举类型吗？这将清理所有不一致的数据 (y/N): ").strip().lower()
    
    if choice == 'y':
        if recreate_enums():
            print("\n🎉 重建完成！现在可以重启后端服务。")
        else:
            print("\n💥 重建失败！请检查错误信息。")
    else:
        print("取消操作。")
