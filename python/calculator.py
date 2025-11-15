def calculator():
    num1 = float(input("请输入第一个数字："))
    operator = input("运算符(+-*/): ")
    num2 = float(input("请输入第二个数字："))

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2
    else:
        print("无效的运算符")
        return

    print(f"{num1} {operator} {num2} = {result}")

calculator();
