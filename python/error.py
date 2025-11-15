try:
    num = int(input("请输入一个数字："))
    result = 10 / num
    print(result)
except ValueError:
    print("请输入一个有效的数字")
except ZeroDivisionError:
    print("除数不能为零")