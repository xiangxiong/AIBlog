class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"我叫{self.name}, 我今年{self.age}岁了")

# 使用类
student = Student('张三', 25)
student.introduce()