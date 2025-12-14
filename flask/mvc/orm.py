import psycopg2

# 面向过程的orm 类.
class MyOrm:
    def __init__(self):
        conn = psycopg2.connect(
            database="llmops",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        ) 
        # 实例化游标对象
        cursor = conn.cursor();
        self.cursor = cursor;

    def queryUserAll(self):
        sql = "SELECT * FROM employees";
        self.cursor.execute(sql)
        result =self.cursor.fetchall();
        return result;
    def execute(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall();

class User:
    table_name = "employees";
    def getUserList(self):
        sql =  "select * from %s" % (self.table_name);
        return MyOrm().execute(sql);

        

if __name__ == "__main__":
    orm = MyOrm();
    # result = orm.queryUserAll();
    # print(result);
    user = User();
    users =user.getUserList();
    print(users);