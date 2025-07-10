"""
数据库迁移脚本：为沟通记录表添加新字段
添加沟通日期、沟通方式、跟进相关字段
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
        
        # 添加沟通日期字段
        cursor.execute("""
            ALTER TABLE communications 
            ADD COLUMN IF NOT EXISTS communication_date DATE;
        """)
        
        # 添加沟通方式字段
        cursor.execute("""
            ALTER TABLE communications 
            ADD COLUMN IF NOT EXISTS communication_type VARCHAR(50);
        """)
        
        # 添加是否需要跟进字段
        cursor.execute("""
            ALTER TABLE communications 
            ADD COLUMN IF NOT EXISTS follow_up_required BOOLEAN DEFAULT FALSE;
        """)
        
        # 添加跟进日期字段
        cursor.execute("""
            ALTER TABLE communications 
            ADD COLUMN IF NOT EXISTS follow_up_date DATE;
        """)
        
        # 提交更改
        conn.commit()
        print("迁移成功完成！已为沟通记录表添加新字段。")
        
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
