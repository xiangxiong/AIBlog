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

class Model:

    def field(self,selectparams = None):
        self.columns = ','.join(selectparams);
        return self;

    def query(self,**whereparams):
        table = self.__class__.__getattribute__(self,"table_name");
        if hasattr(self,"columns"):
            sql = "select %s from %s" % (self.columns,table);
        else:
            sql = "select %s from %s" % (table);
        if whereparams is not None:
            sql = sql + " where "
            for k,v in whereparams.items():
                sql += " %s='%s' and" % (k,v);
            sql += " 1=1";
            print(sql);
        # sql = sql % (self.table_name,self.columns);
        return MyOrm().execute(sql);

class User(Model):
    table_name = "employees";
    def getUserList(self):
        sql =  "select * from %s" % (self.table_name);
        return MyOrm().execute(sql);

    def getUserOne(self,selectparams = None,whereparams = None):

        if(selectparams is not None and type(selectparams) is list):
            # 进行 sql 语句的拼接
            sql = "select " 
            for i in selectparams:
                sql += i + ","
            sql = sql[0:-1]
            sql  = sql  + " from " + self.table_name;
            print(sql);
        
        if whereparams is not None:
            sql = sql + " where "
            for k,v in whereparams.items():
                sql += " %s='%s' and" % (k,v);
            sql += " 1=1";
            print(sql);
        
        sql += " limit 1";
        
        return MyOrm().execute(sql);


    # 通过链式操作来制定查询列，调用各种方法
    

if __name__ == "__main__":
    orm = MyOrm();
    # result = orm.queryUserAll();
    # print(result);
    user = User();
    print(user.field(["id","name"]).query());
    # users =user.getUserList();
    # print(users);
    # result = user.getUserOne(["id","name"],{"id":"1"});
    # print(result);