import psycopg2

def connectDatabase():
    try:
        conn = psycopg2.connect(
            database="llmops",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        print("数据库连接成功")
        return conn
    except Exception as e:
        print(e)
        return None
    # finally:
    #     if conn:
    #         conn.close();
    #     print("数据库连接关闭");

def insertItem(conn):
    try:
        cursor = conn.cursor();
        # 创建表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER,
            salary DECIMAL(10, 2),
            hire_date DATE,
            email VARCHAR(100)
        )
        """
        cursor.execute(create_table_sql);
        print("Table created successfully");
    
        # 插入数据
        insert_sql = """
        INSERT INTO employees (name, age, salary, hire_date, email) 
        VALUES (%s, %s, %s, %s, %s)
        """

        employees = [
            ('张三', 30, 8000.00, '2020-01-15', 'zhangsan@example.com'),
            ('李四', 25, 7500.50, '2021-03-20', 'lisi@example.com'),
            ('王五', 35, 12000.00, '2019-07-10', 'wangwu@example.com')
        ]

        for emp in employees:
            cursor.execute(insert_sql, emp)
        conn.commit();
        print("Data inserted successfully");

    except Exception as e:
        conn.rollback();
        print(e)
    finally:
        if cursor:
            cursor.close();
            print('connect close');

def queryData(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees ORDER BY id")
        result = cursor.fetchall()
        print("\n=== 所有员工数据 ===")
        for row in result:
            print(f"ID: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 薪资: {row[3]}, 入职日期: {row[4]}")
        cursor.close()
    
    except Exception as e:
        print(e)

def main():
   conn = connectDatabase()
   if conn:
       queryData(conn)

if __name__ == "__main__":
    main()