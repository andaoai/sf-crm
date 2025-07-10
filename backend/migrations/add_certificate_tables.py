"""
数据库迁移脚本：添加证书相关表
创建时间：2025-07-10
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine

def create_certificate_tables():
    """创建证书相关表"""
    
    # 创建证书类型表
    create_certificate_types_sql = """
    CREATE TABLE IF NOT EXISTS certificate_types (
        type_code VARCHAR(50) PRIMARY KEY,
        type_name VARCHAR(100) NOT NULL UNIQUE,
        category VARCHAR(50),
        description TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        sort_order INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_certificate_types_type_name ON certificate_types(type_name);
    CREATE INDEX IF NOT EXISTS idx_certificate_types_category ON certificate_types(category);
    CREATE INDEX IF NOT EXISTS idx_certificate_types_is_active ON certificate_types(is_active);
    """
    
    # 创建证书状态枚举类型
    create_status_enum_sql = """
    DO $$ BEGIN
        CREATE TYPE certificate_status AS ENUM ('valid', 'expired', 'revoked');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """

    # 创建具体证书表
    create_certificates_sql = """
    CREATE TABLE IF NOT EXISTS certificates (
        certificate_id VARCHAR(50) PRIMARY KEY,
        talent_id BIGINT NOT NULL,
        certificate_type VARCHAR(100) NOT NULL,
        certificate_name VARCHAR(200),
        certificate_number VARCHAR(100),
        issue_date DATE,
        expiry_date DATE,
        issuing_authority VARCHAR(100),
        specialty VARCHAR(100),
        level VARCHAR(50),
        status certificate_status DEFAULT 'valid',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (talent_id) REFERENCES talents(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_certificates_talent_id ON certificates(talent_id);
    CREATE INDEX IF NOT EXISTS idx_certificates_certificate_type ON certificates(certificate_type);
    CREATE INDEX IF NOT EXISTS idx_certificates_status ON certificates(status);
    """
    
    with engine.connect() as connection:
        # 创建表
        connection.execute(text(create_certificate_types_sql))
        connection.execute(text(create_status_enum_sql))
        connection.execute(text(create_certificates_sql))
        connection.commit()
        print("证书表创建成功")

def insert_default_certificate_types():
    """插入默认证书类型数据"""
    
    certificate_types_data = [
        # 建造师类
        ('JZS_1', '一级建造师', '建造师', '建筑工程施工管理最高级别', True, 1),
        ('JZS_2', '二级建造师', '建造师', '建筑工程施工管理', True, 2),
        
        # 造价工程师
        ('ZJS_1', '一级造价工程师', '造价工程师', '工程造价咨询最高级别', True, 3),
        ('ZJS_2', '二级造价工程师', '造价工程师', '工程造价咨询', True, 4),
        
        # 监理工程师
        ('JLS_1', '监理工程师', '监理工程师', '工程监理', True, 5),
        
        # 注册建筑师
        ('ZJZ_1', '一级注册建筑师', '注册建筑师', '建筑设计最高级别', True, 6),
        ('ZJZ_2', '二级注册建筑师', '注册建筑师', '建筑设计', True, 7),
        
        # 注册结构工程师
        ('JGS_1', '一级注册结构工程师', '注册结构工程师', '结构设计最高级别', True, 8),
        ('JGS_2', '二级注册结构工程师', '注册结构工程师', '结构设计', True, 9),
        
        # 安全工程师
        ('AQS_1', '注册安全工程师', '安全工程师', '安全管理', True, 10),
        
        # 三类人员
        ('SLR_A', '三类人员A证', '三类人员', '企业主要负责人', True, 11),
        ('SLR_B', '三类人员B证', '三类人员', '项目负责人', True, 12),
        ('SLR_C', '三类人员C证', '三类人员', '专职安全员', True, 13),
        
        # 其他常见证书
        ('ZTG_1', '注册土木工程师(岩土)', '注册土木工程师', '岩土工程设计', True, 14),
        ('ZDQ_1', '注册电气工程师', '注册电气工程师', '电气工程设计', True, 15),
        ('ZGS_1', '注册公用设备工程师', '注册公用设备工程师', '公用设备工程设计', True, 16),
    ]
    
    insert_sql = """
    INSERT INTO certificate_types
    (type_code, type_name, category, description, is_active, sort_order)
    VALUES (:type_code, :type_name, :category, :description, :is_active, :sort_order)
    ON CONFLICT (type_code) DO NOTHING
    """

    with engine.connect() as connection:
        for data in certificate_types_data:
            connection.execute(text(insert_sql), {
                'type_code': data[0],
                'type_name': data[1],
                'category': data[2],
                'description': data[3],
                'is_active': data[4],
                'sort_order': data[5]
            })
        connection.commit()
        print(f"插入了 {len(certificate_types_data)} 个默认证书类型")

def migrate_existing_certificate_data():
    """迁移现有的证书数据到新表结构"""
    
    # 查询现有人才的证书信息
    query_sql = """
    SELECT id, certificate_info, certificate_expiry_date, certificate_level, certificate_specialty
    FROM talents 
    WHERE certificate_info IS NOT NULL AND certificate_info != ''
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query_sql))
        talents_with_certificates = result.fetchall()
        
        migrated_count = 0
        for talent in talents_with_certificates:
            talent_id, cert_info, expiry_date, cert_level, cert_specialty = talent
            
            # 根据证书信息推断证书类型
            certificate_type = infer_certificate_type(cert_info, cert_level, cert_specialty)
            
            if certificate_type:
                # 生成证书ID
                certificate_id = f"MIGRATED_{talent_id}_{migrated_count + 1}"
                
                # 插入证书记录
                insert_cert_sql = """
                INSERT INTO certificates
                (certificate_id, talent_id, certificate_type, certificate_name,
                 expiry_date, specialty, level, status, notes)
                VALUES (:certificate_id, :talent_id, :certificate_type, :certificate_name,
                        :expiry_date, :specialty, :level, :status, :notes)
                """

                connection.execute(text(insert_cert_sql), {
                    'certificate_id': certificate_id,
                    'talent_id': talent_id,
                    'certificate_type': certificate_type,
                    'certificate_name': cert_info,
                    'expiry_date': expiry_date,
                    'specialty': cert_specialty,
                    'level': cert_level,
                    'status': 'valid',
                    'notes': f"从原证书信息迁移: {cert_info}"
                })
                migrated_count += 1
        
        connection.commit()
        print(f"迁移了 {migrated_count} 个证书记录")

def infer_certificate_type(cert_info, cert_level, cert_specialty):
    """根据证书信息推断证书类型"""
    if not cert_info:
        return None
    
    cert_info_lower = cert_info.lower()
    
    # 建造师
    if '建造师' in cert_info:
        if '一级' in cert_info or cert_level == '一级':
            return '一级建造师'
        elif '二级' in cert_info or cert_level == '二级':
            return '二级建造师'
    
    # 造价工程师
    if '造价' in cert_info:
        if '一级' in cert_info or cert_level == '一级':
            return '一级造价工程师'
        elif '二级' in cert_info or cert_level == '二级':
            return '二级造价工程师'
    
    # 监理工程师
    if '监理' in cert_info:
        return '监理工程师'
    
    # 注册建筑师
    if '建筑师' in cert_info and '注册' in cert_info:
        if '一级' in cert_info or cert_level == '一级':
            return '一级注册建筑师'
        elif '二级' in cert_info or cert_level == '二级':
            return '二级注册建筑师'
    
    # 三类人员
    if '三类' in cert_info or 'A证' in cert_info or 'B证' in cert_info or 'C证' in cert_info:
        if 'A' in cert_info:
            return '三类人员A证'
        elif 'B' in cert_info:
            return '三类人员B证'
        elif 'C' in cert_info:
            return '三类人员C证'
    
    # 安全工程师
    if '安全' in cert_info and '工程师' in cert_info:
        return '注册安全工程师'
    
    return None

def remove_old_certificate_columns():
    """移除人才表中的旧证书字段"""
    
    alter_sql = """
    ALTER TABLE talents 
    DROP COLUMN IF EXISTS certificate_info,
    DROP COLUMN IF EXISTS certificate_expiry_date,
    DROP COLUMN IF EXISTS certificate_level,
    DROP COLUMN IF EXISTS certificate_specialty
    """
    
    with engine.connect() as connection:
        connection.execute(text(alter_sql))
        connection.commit()
        print("移除了人才表中的旧证书字段")

def run_migration():
    """执行完整的迁移流程"""
    print("开始证书表迁移...")
    
    try:
        # 1. 创建新表
        create_certificate_tables()
        
        # 2. 插入默认证书类型
        insert_default_certificate_types()
        
        # 3. 迁移现有数据
        migrate_existing_certificate_data()
        
        # 4. 移除旧字段（可选，建议先备份）
        # remove_old_certificate_columns()
        
        print("证书表迁移完成！")
        
    except Exception as e:
        print(f"迁移过程中出现错误: {e}")
        raise

if __name__ == "__main__":
    run_migration()
