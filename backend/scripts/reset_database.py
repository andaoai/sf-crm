#!/usr/bin/env python3
"""
数据库重置脚本 - 清空所有数据并重新录入测试数据
"""

import sys
import os
import psycopg2
from datetime import datetime

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

def clear_all_data():
    """清空所有表的数据，保留表结构"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("开始清空数据库数据...")
        
        # 禁用外键约束检查
        cursor.execute("SET session_replication_role = replica;")
        
        # 获取所有用户表
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'pg_%' 
            AND tablename NOT LIKE 'sql_%'
            ORDER BY tablename;
        """)
        
        tables = cursor.fetchall()
        
        # 清空每个表的数据
        for (table_name,) in tables:
            print(f"清空表: {table_name}")
            cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
        
        # 重新启用外键约束检查
        cursor.execute("SET session_replication_role = DEFAULT;")
        
        # 提交更改
        conn.commit()
        print("✓ 数据库数据清空完成！")
        
        return True
        
    except Exception as e:
        print(f"✗ 清空数据库失败: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def run_data_creation_scripts():
    """运行数据创建脚本"""
    print("\n开始创建新的测试数据...")

    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    # 运行直接数据库插入脚本
    print("1. 运行数据插入脚本...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable,
            os.path.join(scripts_dir, 'direct_data_insert.py')
        ], capture_output=True, text=True, cwd=scripts_dir)

        if result.returncode == 0:
            print("✓ 数据插入成功")
            print(result.stdout)
        else:
            print(f"✗ 数据插入失败: {result.stderr}")
    except Exception as e:
        print(f"✗ 运行数据插入脚本失败: {e}")

def verify_data():
    """验证数据是否正确录入"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("\n验证数据录入结果...")
        
        # 检查各表的数据量
        tables_to_check = [
            ('talents', '人才'),
            ('companies', '公司'),
            ('certificates', '证书'),
            ('certificate_types', '证书类型'),
            ('communications', '沟通记录')
        ]
        
        for table_name, display_name in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"✓ {display_name}表: {count} 条记录")
            except Exception as e:
                print(f"✗ 检查{display_name}表失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 验证数据失败: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def main():
    """主函数"""
    print("=" * 50)
    print("CRM数据库重置工具")
    print("=" * 50)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 第一步：清空数据
    if not clear_all_data():
        print("数据清空失败，终止操作")
        return
    
    # 第二步：重新录入数据
    run_data_creation_scripts()
    
    # 第三步：验证数据
    verify_data()
    
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print("数据库重置完成！")

if __name__ == "__main__":
    main()
