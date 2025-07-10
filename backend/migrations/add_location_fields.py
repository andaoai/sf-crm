"""
数据库迁移脚本：为人才表添加地区字段
添加省份、城市和详细地址字段
"""

import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def migrate():
    """执行迁移"""
    # 数据库连接参数（Docker环境）
    db_config = {
        'host': 'postgres',  # Docker服务名
        'port': '5432',
        'database': 'crm_db',
        'user': 'crm_user',
        'password': 'crm_password'
    }
    
    conn = None
    cursor = None
    
    try:
        # 连接数据库
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        print("开始执行迁移...")
        
        # 添加省份字段
        cursor.execute("""
            ALTER TABLE talents 
            ADD COLUMN IF NOT EXISTS province VARCHAR(50);
        """)
        
        # 添加城市字段
        cursor.execute("""
            ALTER TABLE talents 
            ADD COLUMN IF NOT EXISTS city VARCHAR(50);
        """)
        
        # 添加详细地址字段
        cursor.execute("""
            ALTER TABLE talents 
            ADD COLUMN IF NOT EXISTS address TEXT;
        """)
        
        # 提交更改
        conn.commit()
        print("迁移成功完成！已为人才表添加地区字段。")
        
    except Exception as e:
        print(f"迁移失败: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate()
