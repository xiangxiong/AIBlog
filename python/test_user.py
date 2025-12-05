import json
from user import main

# 测试用例1：原始输入格式 - 字典包含arg1键
test_input1 = {
  "arg1": [
    {
      "taskId": "RT1435570531072622592"
    },
    {
      "taskId": "RT1434923069735854080"
    },
    {
      "taskId": "RT1434922522605674496"
    },
    {
      "taskId": "RT1431281757561438208"
    }
  ]
}

# 测试用例2：新输入格式 - 直接传入列表
test_input2 = [
    {"taskId": "test3"},
    {"taskId": "test4"}
]

print("测试用例1：输入为字典，包含arg1键")
print("=" * 50)
try:
    result1 = main(test_input1)
    print("✅ 测试用例1成功")
    print(f"输出：{result1}")
except Exception as e:
    print(f"❌ 测试用例1失败：{e}")

print("\n\n测试用例2：输入直接为列表")
print("=" * 50)
try:
    result2 = main(test_input2)
    print("✅ 测试用例2成功")
    print(f"输出：{result2}")
except Exception as e:
    print(f"❌ 测试用例2失败：{e}")

print("\n\n所有测试完成！")