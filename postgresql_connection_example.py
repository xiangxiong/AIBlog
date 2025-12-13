#!/usr/bin/env python3
"""
PostgreSQL数据库连接示例
使用psycopg2库连接到PostgreSQL数据库
"""

import psycopg2
from psycopg2 import Error


def connect_to_postgresql():
    """
    连接到PostgreSQL数据库
    :return: 数据库连接对象，如果连接失败则返回None
    """
    conn = None
    try:
        # 使用用户提供的连接参数
        conn = psycopg2.connect(
            dbname='llmops',          # 数据库名
            user='postgres',          # 用户名
            password='postgres',      # 密码
            host='localhost',         # 地址
            port='5432'               # 端口
        )
        
        print("✅ 成功连接到PostgreSQL数据库")
        print(f"📦 数据库: {conn.info.dbname}")
        print(f"👤 用户: {conn.info.user}")
        print(f"🏠 主机: {conn.info.host}")
        print(f"🔌 端口: {conn.info.port}")
        
        return conn
    
    except Error as e:
        print(f"❌ 连接失败: {e}")
        print("📝 请检查以下几点:")
        print("   1. PostgreSQL服务是否已启动")
        print("   2. 连接参数是否正确")
        print("   3. PostgreSQL是否允许远程连接")
        print("   4. 防火墙是否允许5432端口访问")
        return None


def basic_operations(conn):
    """
    基本数据库操作示例
    :param conn: 数据库连接对象
    """
    if not conn:
        return
    
    try:
        # 创建游标对象
        cursor = conn.cursor()
        
        # 1. 获取数据库版本
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        print(f"\n📋 PostgreSQL版本: {db_version}")
        
        # 2. 创建测试表（如果不存在）
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ 测试表创建成功")
        
        # 3. 插入测试数据
        insert_query = "INSERT INTO test_users (name, email) VALUES (%s, %s)"
        user_data = [
            ('张三', 'zhangsan@example.com'),
            ('李四', 'lisi@example.com')
        ]
        cursor.executemany(insert_query, user_data)
        conn.commit()
        print(f"✅ 成功插入 {cursor.rowcount} 条记录")
        
        # 4. 查询数据
        select_query = "SELECT id, name, email, created_at FROM test_users ORDER BY id"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print(f"\n📋 查询到 {len(records)} 条记录:")
        for row in records:
            print(f"   ID: {row[0]}, 姓名: {row[1]}, 邮箱: {row[2]}, 创建时间: {row[3]}")
        
        # 5. 更新数据
        update_query = "UPDATE test_users SET email = %s WHERE name = %s"
        cursor.execute(update_query, ('updated_zhangsan@example.com', '张三'))
        conn.commit()
        print(f"✅ 成功更新 {cursor.rowcount} 条记录")
        
        # 6. 删除数据
        delete_query = "DELETE FROM test_users WHERE name = %s"
        cursor.execute(delete_query, ('李四',))
        conn.commit()
        print(f"✅ 成功删除 {cursor.rowcount} 条记录")
        
        # 7. 再次查询验证
        cursor.execute(select_query)
        records = cursor.fetchall()
        print(f"\n📋 更新后的数据:")
        for row in records:
            print(f"   ID: {row[0]}, 姓名: {row[1]}, 邮箱: {row[2]}")
        
    except Error as e:
        print(f"❌ 操作失败: {e}")
        # 发生错误时回滚
        conn.rollback()
    finally:
        # 关闭游标
        if cursor:
            cursor.close()


def context_manager_example():
    """
    使用上下文管理器连接数据库（推荐方式）
    自动处理连接和游标关闭
    """
    print("\n=== 使用上下文管理器示例 ===")
    try:
        # 使用with语句自动关闭连接
        with psycopg2.connect(
            dbname='llmops',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        ) as conn:
            # 使用with语句自动关闭游标
            with conn.cursor() as cursor:
                cursor.execute("SELECT count(*) FROM test_users")
                count = cursor.fetchone()[0]
                print(f"👥 测试表中的用户数量: {count}")
        
    except Error as e:
        print(f"❌ 上下文管理器示例失败: {e}")


if __name__ == "__main__":
    print("📚 PostgreSQL数据库连接示例")
    print("=" * 50)
    
    # 连接到数据库
    conn = connect_to_postgresql()
    
    if conn:
        # 执行基本操作
        basic_operations(conn)
        
        # 上下文管理器示例
        context_manager_example()
        
        # 关闭连接
        conn.close()
        print("\n✅ 数据库连接已关闭")
    
    print("\n🎉 示例结束")
