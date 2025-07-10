"""
数据库迁移脚本：让证书表的talent_id字段可以为空
这样可以支持创建未关联人才的证书
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

        # 修改talent_id列为可空
        cursor.execute("""
            ALTER TABLE certificates
            ALTER COLUMN talent_id DROP NOT NULL;
        """)

        # 提交更改
        conn.commit()
        print("迁移成功完成！talent_id字段现在可以为空。")

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
