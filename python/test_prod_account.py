import json
import requests
import time
from collections import Counter

# 复制prod_account.py中的main函数到测试脚本中
def main(arg1: dict, arg2: str) -> dict:
    # 输入数据
    input_data = arg1;
    
    # 通用请求头
    headers = {
        'appId': '836021804215570432',
        'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': '',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'scc-auth': arg2
    }

    print(f"发送的请求头 input_data: {input_data}")
    
    # 第一步：获取所有taskId
    # 支持两种输入格式：1. 字典包含arg1键 2. 直接传入列表
    input_list = input_data['arg1'] if isinstance(input_data, dict) else input_data
    task_ids = [item['taskId'] for item in input_list]
    print(f"提取的taskIds: {task_ids}")
    
    # 最终汇总的列表
    final_records = []
    
    # 第二步和第三步：遍历每个taskId，发起请求
    for task_id in task_ids:
        print(f"\n处理taskId: {task_id}")
        
        # 第二个请求：deptCollectPageList
        url1 = 'https://mall-admin.lbxcn.com/scc-finance/finance/reconciliation/result/deptCollectPageList'
        data1 = {
            "_t": int(time.time() * 1000),
            "appId": "836021804215570432",
            "current": 1,
            "isPage": 1,
            "page": 1,
            "pageSize": 100,
            "roleId": "836025954349355008",
            "taskId": task_id,
            "tenantId": 1000001,
            "userId": "18"
        }
        
        print(f"发送的请求数据: {data1}")
        print(f"发送的请求头: {headers}")
        print(f"发送的请求URL: {url1}")

        try:
            response1 = requests.post(url1, headers=headers, json=data1)
            response1.raise_for_status()
            result1 = response1.json()
            
            if result1.get('success'):
                # 获取第二个请求的records
                records1 = result1.get('data', {}).get('records', [])
                print(f"第二个请求返回的records数量: {len(records1)}")
                
                # 遍历第二个请求的records，获取每个taskId并发起第三个请求
                for record1 in records1:
                    sub_task_id = record1.get('taskId')
                    erp_dept_id = record1.get('erpDeptId')
                    if sub_task_id:
                        # 第三个请求：pageList
                        url2 = 'https://mall-admin.lbxcn.com/scc-finance/finance/reconciliation/result/pageList'
                        data2 = {
                            "appId": "836021804215570432",
                            "current": 1,
                            "erpDeptId": erp_dept_id,
                            "isPage": 1,
                            "page": 1,
                            "pageSize": 10000,
                            "roleId": "836025954349355008",
                            "taskId": sub_task_id,
                            "tenantId": 1000001,
                            "userId": "18"
                        }

                        print(f"第三个请求发送的请求数据: {data2}")
                        print(f"第三个请求url2的请求数据: {url2}")
                        print(f"第三个请求data2发送的请求数据: {data2}")

                        try:
                            response2 = requests.post(url2, headers=headers, json=data2)
                            response2.raise_for_status()
                            result2 = response2.json()
                            
                            if result2.get('success'):
                                # 获取第三个请求的records并汇总
                                records2 = result2.get('data', {}).get('records', [])
                                print(f"第三个请求返回的records数量: {len(records2)}")
                                final_records.extend(records2)
                            else:
                                print(f"第三个请求失败: {result2.get('msg')}")
                        except requests.exceptions.RequestException as e:
                            print(f"第三个请求异常: {e}")
            else:
                print(f"第二个请求失败: {result1.get('msg')}")
        except requests.exceptions.RequestException as e:
            print(f"第二个请求异常: {e}")
    
    # 统计remark出现次数
    remark_counter = Counter()
    for record in final_records:
        # adjust值为false或None时统计为未调账
        if not record.get('adjust'):
            remark_counter['未调账'] += 1
        elif 'remark' in record and record['remark']:
            # adjust值为true且remark存在且不为空时，去除前后空格后统计
            clean_remark = record['remark'].strip()
            remark_counter[clean_remark] += 1
        else:
            # adjust值为true但remark为空或仅含空格时，统计为"空调账原因"（确保所有记录都被统计）
            remark_counter['空调账原因'] += 1
    
    # 调试信息：输出总数和统计总和
    print(f"final_records总数: {len(final_records)}")
    print(f"remark_counter总和: {sum(remark_counter.values())}")
    print(f"remark_counter详情: {dict(remark_counter)}")
    # 计算未调账百分比
    total = sum(remark_counter.values())
    unadjusted = remark_counter.get('未调账', 0)
    percentage = (unadjusted / total) * 100 if total > 0 else 0
    print(f"未调账百分比计算: {unadjusted}/{total} = {percentage:.2f}%")
    
    # 生成echarts饼状图配置
    pie_data = []
    # 预定义颜色列表
    colors = [
        "#E63946", "#457B9D", "#FFB703", "#219EBC", "#FF595E",
        "#10B981", "#F59E0B", "#EF4444", "#3B82F6", "#8B5CF6",
        "#EC4899", "#14B8A6", "#F97316", "#0EA5E9", "#D946EF",
        "#FBBF24", "#34D399", "#6366F1", "#06B6D4", "#10B981",
        "#FF8C00", "#00BFFF", "#FF6347", "#9370DB", "#2E8B57",
        "#FFD700", "#00FA9A", "#DC143C", "#1E90FF", "#FF1493"
    ]
    color_index = 0
    
    for remark, count in remark_counter.items():
        item = {
            "name": remark,
            "value": count
        }
        # 为"未调账"项设置白色，其他项使用预定义颜色
        if remark == "未调账":
            item["itemStyle"] = {
                "color": "#FFFFFF"  # 白色
            }
        else:
            item["itemStyle"] = {
                "color": colors[color_index % len(colors)]
            }
            color_index += 1
        pie_data.append(item)
    
    echarts_option = {
        "title": {
            "text": "调账原因分布",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": " {d}%：{b}（{c}条）",
            "zIndex": 9999
        },
        "series": [
            {
                "name": "调账原因",
                "type": "pie",
                "radius": "50%",
                "center": ["50%", "50%"],
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "label": {
                    "position": "outside", # 标签放置在外部
                    "show": True,
                    "formatter": " {d}%：{b}（{c}条）"
                }
            }
        ]
    }

    # 生成输出文件
    output = "```echarts\n" + json.dumps(echarts_option, ensure_ascii=False, indent=2) + "\n```"
    
    return {
        "result": output,
        "total_count": len(final_records)
    }

# 用户提供的测试参数
arg1 = [
    {
      "taskId": "RT1446203121389436928",
      "erpDeptId": "17198"
    },
    {
      "taskId": "RT1445404562483003392",
      "erpDeptId": "13073"
    },
    {
      "taskId": "RT1441102288324669440",
      "erpDeptId": None
    },
    {
      "taskId": "RT1440701740130983936",
      "erpDeptId": None
    },
    {
      "taskId": "RT1440366959500226560",
      "erpDeptId": "12827"
    },
    {
      "taskId": "RT1440366851544276992",
      "erpDeptId": "17198"
    },
    {
      "taskId": "RT1440366763626229760",
      "erpDeptId": "13"
    },
    {
      "taskId": "RT1438566632649351168",
      "erpDeptId": None
    },
    {
      "taskId": "RT1438566522774122496",
      "erpDeptId": "13073"
    },
    {
      "taskId": "RT1437759068592365568",
      "erpDeptId": None
    },
    {
      "taskId": "RT1437754840514588672",
      "erpDeptId": None
    },
    {
      "taskId": "RT1437752903150034944",
      "erpDeptId": "18773"
    },
    {
      "taskId": "RT1437752784223498240",
      "erpDeptId": "12059"
    },
    {
      "taskId": "RT1437751810986827776",
      "erpDeptId": None
    },
    {
      "taskId": "RT1437743736883277824",
      "erpDeptId": None
    },
    {
      "taskId": "RT1437455610054995968",
      "erpDeptId": None
    },
    {
      "taskId": "RT1437455517641895936",
      "erpDeptId": "12551"
    },
    {
      "taskId": "RT1437431773913444352",
      "erpDeptId": None
    },
    {
      "taskId": "RT1435731738650689536",
      "erpDeptId": None
    }
  ]


# 用户提供的scc-auth值
arg2 = "bearer eyJ0eXAiOiJKc29uV2ViVG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIxMDAwMDAxIiwiZGVwdF9jb2RlIjoiIiwidXNlcl9pZCI6IjkwNzkyNDQ5OTI0MTU4NjY4OCIsInJvbGVfaWQiOiJXZWJVc2VyUm9sZShpZD05MTI0Nzk1NTU0MTY3MDcwNzIsIHVzZXJJZD05MDc5MjQ0OTkyNDE1ODY2ODgsIGFjY291bnQ9LCBuYW1lPSwgc291cmNlPS0xLCBwYXNzd29yZD0sIHJvbGVOYW1lPSwgcm9sZVR5cGU9LTEsIGRhdGFTY29wZT0tMSwgcm9sZUlkPTg4NjQzNjU4NjA3Mzc5NjYwOCwgcm9sZUlkRXh0PS0xLCB1cGRhdGVUaW1lPW51bGwsIGNyZWF0ZVRpbWU9bnVsbCksV2ViVXNlclJvbGUoaWQ9OTI5NzY3NjM2NDUyODU5OTA0LCB1c2VySWQ9OTA3OTI0NDk5MjQxNTg2Njg4LCBhY2NvdW50PSwgbmFtZT0sIHNvdXJjZT0tMSwgcGFzc3dvcmQ9LCByb2xlTmFtZT0sIHJvbGVUeXBlPS0xLCBkYXRhU2NvcGU9LTEsIHJvbGVJZD05Mjk3NjczOTk2NzE4MTYxOTIsIHJvbGVJZEV4dD0tMSwgdXBkYXRlVGltZT1udWxsLCBjcmVhdGVUaW1lPW51bGwpLFdlYlVzZXJSb2xlKGlkPTkzNTg1NTg4MDU5MjUxNTA3MiwgdXNlcklkPTkwNzkyNDQ5OTI0MTU4NjY4OCwgYWNjb3VudD0sIG5hbWU9LCBzb3VyY2U9LTEsIHBhc3N3b3JkPSwgcm9sZU5hbWU9LCByb2xlVHlwZT0tMSwgZGF0YVNjb3BlPS0xLCByb2xlSWQ9MjMsIHJvbGVJZEV4dD0tMSwgdXBkYXRlVGltZT1udWxsLCBjcmVhdGVUaW1lPW51bGwpLFdlYlVzZXJSb2xlKGlkPTk1MzI3MzEyNjA1OTA3MzUzNiwgdXNlcklkPTkwNzkyNDQ5OTI0MTU4NjY4OCwgYWNjb3VudD0sIG5hbWU9LCBzb3VyY2U9LTEsIHBhc3N3b3JkPSwgcm9sZU5hbWU9LCByb2xlVHlwZT0tMSwgZGF0YVNjb3BlPS0xLCByb2xlSWQ9MjQsIHJvbGVJZEV4dD0tMSwgdXBkYXRlVGltZT1udWxsLCBjcmVhdGVUaW1lPW51bGwpLFdlYlVzZXJSb2xlKGlkPTk1NTU1NDM3NjY2OTAyODM1MiwgdXNlcklkPTkwNzkyNDQ5OTI0MTU4NjY4OCwgYWNjb3VudD0sIG5hbWU9LCBzb3VyY2U9LTEsIHBhc3N3b3JkPSwgcm9sZU5hbWU9LCByb2xlVHlwZT0tMSwgZGF0YVNjb3BlPS0xLCByb2xlSWQ9NzcwMzU4NjEyNjM4ODMwNTkyLCByb2xlSWRFeHQ9LTEsIHVwZGF0ZVRpbWU9bnVsbCwgY3JlYXRlVGltZT1udWxsKSxXZWJVc2VyUm9sZShpZD05NjEyOTQzNjU0MzY5MDc1MjAsIHVzZXJJZD05MDc5MjQ0OTkyNDE1ODY2ODgsIGFjY291bnQ9LCBuYW1lPSwgc291cmNlPS0xLCBwYXNzd29yZD0sIHJvbGVOYW1lPSwgcm9sZVR5cGU9LTEsIGRhdGFTY29wZT0tMSwgcm9sZUlkPTk2MTI5MTY2MjIyNDM1MTIzMiwgcm9sZUlkRXh0PS0xLCB1cGRhdGVUaW1lPW51bGwsIGNyZWF0ZVRpbWU9bnVsbCksV2ViVXNlclJvbGUoaWQ9MTAzMzczNzA3MzczODk2NDk5MiwgdXNlcklkPTkwNzkyNDQ5OTI0MTU4NjY4OCwgYWNjb3VudD0sIG5hbWU9LCBzb3VyY2U9LTEsIHBhc3N3b3JkPSwgcm9sZU5hbWU9LCByb2xlVHlwZT0tMSwgZGF0YVNjb3BlPS0xLCByb2xlSWQ9ODY5MDQzNDkyMzExNDQ1NTA0LCByb2xlSWRFeHQ9LTEsIHVwZGF0ZVRpbWU9bnVsbCwgY3JlYXRlVGltZT1udWxsKSIsInVzZXJfbmFtZSI6IuS9meexs-mmmSIsImVudiI6InByb2QiLCJkZXB0X2lkIjoiLTEiLCJhY2NvdW50IjoiMDAxMTMxNDAiLCJjbGllbnRfaWQiOiJzYWJlciIsImV4cCI6MTc2NTkxMTYwMCwibmJmIjoxNzY1ODQ5OTY0fQ.y5PNs8dgSOtu63Y1S2wzgGuD12Vl7RN5TjrrEubjceU"

print("=== 测试开始 ===")

# 使用用户提供的参数测试函数
try:
    # 构造输入参数，格式为字典包含arg1键
    input_data = {"arg1": arg1}
    
    # 调用main函数
    result = main(input_data, arg2)
    
    print("测试成功！")
    print(f"返回结果类型：{type(result)}")
    print(f"总记录数：{result.get('total_count', 0)}")
    print(f"结果：")
    print(result.get('result', ''))
    
    # 将结果保存到文件
    with open('test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n测试结果已保存到 test_result.json 文件")
    
except Exception as e:
    print(f"测试失败：{e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试结束 ===")
