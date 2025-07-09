#!/usr/bin/env python3
"""
数据库迁移脚本 - 为人才表添加新字段
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine, get_db

def migrate_talents_table():
    """为人才表添加新字段"""

    migration_statements = [
        # 添加沟通内容字段
        "ALTER TABLE talents ADD COLUMN IF NOT EXISTS communication_content TEXT",

        # 创建证书等级枚举类型
        """DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'certificatelevel') THEN
        CREATE TYPE certificatelevel AS ENUM ('一级', '二级', '初级工程师', '中级工程师', '高级工程师', '三类人员A类', '三类人员B类', '三类人员C类', '其他');
    END IF;
END $$""",

        # 添加证书等级字段
        "ALTER TABLE talents ADD COLUMN IF NOT EXISTS certificate_level certificatelevel",

        # 创建证书专业枚举类型
        """DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'certificatespecialty') THEN
        CREATE TYPE certificatespecialty AS ENUM (
            '建筑工程', '市政公用工程', '机电工程', '公路工程',
            '水利水电工程', '矿业工程', '铁路工程', '民航机场工程',
            '港口与航道工程', '通信与广电工程',
            '建筑工程师', '结构工程师', '电气工程师', '给排水工程师',
            '暖通工程师', '建筑设计工程师', '工程造价工程师', '测绘工程师',
            '岩土工程师', '建筑材料工程师', '安全管理'
        );
    END IF;
END $$""",

        # 添加证书专业字段
        "ALTER TABLE talents ADD COLUMN IF NOT EXISTS certificate_specialty certificatespecialty",

        # 创建社保情况枚举类型
        """DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'socialsecuritystatus') THEN
        CREATE TYPE socialsecuritystatus AS ENUM ('唯一社保', '无社保');
    END IF;
END $$""",

        # 添加社保情况字段
        "ALTER TABLE talents ADD COLUMN IF NOT EXISTS social_security_status socialsecuritystatus"
    ]

    try:
        with engine.connect() as connection:
            # 执行每个迁移语句
            for statement in migration_statements:
                if statement.strip():
                    connection.execute(text(statement))
            connection.commit()

        print("✅ 数据库迁移成功完成！")
        print("新增字段:")
        print("- communication_content: 沟通内容")
        print("- certificate_level: 证书等级")
        print("- certificate_specialty: 证书专业")
        print("- social_security_status: 社保情况")

    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

    return True

def check_migration_status():
    """检查迁移状态"""
    check_sql = """
    SELECT column_name, data_type, udt_name
    FROM information_schema.columns 
    WHERE table_name = 'talents' 
    AND column_name IN ('communication_content', 'certificate_level', 'certificate_specialty', 'social_security_status')
    ORDER BY column_name;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(check_sql))
            columns = result.fetchall()
            
            if columns:
                print("\n📋 当前新增字段状态:")
                for column in columns:
                    print(f"- {column[0]}: {column[1]} ({column[2]})")
            else:
                print("⚠️  未找到新增字段，需要执行迁移")
                
    except Exception as e:
        print(f"❌ 检查迁移状态失败: {e}")

if __name__ == "__main__":
    print("🔄 人才表数据库迁移工具")
    print("=" * 50)
    
    # 检查当前状态
    check_migration_status()
    
    # 询问是否执行迁移
    choice = input("\n是否执行数据库迁移？(y/N): ").strip().lower()
    
    if choice == 'y':
        if migrate_talents_table():
            print("\n🎉 迁移完成！现在可以重启后端服务以使用新功能。")
        else:
            print("\n💥 迁移失败！请检查错误信息。")
    else:
        print("取消迁移操作。")
