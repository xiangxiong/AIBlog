class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self):
        name = input("学生姓名：")
        score = float(input("学生成绩："))
        self.students.append({'name': name, 'score': score})
        print("添加成功")


    def show_students(self):
        if not self.students:
            print("没有学生信息")
            return

        print("学生列表：")
        for student in self.students:
            print(f"姓名：{student['name']}, 成绩：{student['score']}")


    def run(self):
        while True:
            print("1. 添加学生")
            print("2. 显示学生")
            print("3. 退出系统")
            choice = input("请选择操作：")
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.show_students()
            elif choice == '3':
                print("退出系统")
                break
            else:
                print("无效的选择")



# 启动系统
if __name__ == '__main__':
    manager = StudentManager()
    manager.run();
