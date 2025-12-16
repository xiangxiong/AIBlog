import json
import requests
import time
from collections import Counter

def main(arg1: dict,arg2:str) -> dict:

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
        if 'remark' in record and record['remark'] and record['remark'].strip():
            remark = record['remark'].strip()
            remark_counter[remark] += 1
    
    # 生成echarts饼状图配置
    pie_data = [
        {
            "name": remark,
            "value": count
        }
        for remark, count in remark_counter.items()
    ]
    
    echarts_option = {
        "title": {
            "text": "调账原因分布",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: ({d}%)"
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
                    "formatter": " {d}%：{b}"
                },
                 "color": [
                "#E63946", "#457B9D", "#FFB703", "#219EBC", "#FF595E",
                "#10B981", "#F59E0B", "#EF4444", "#3B82F6", "#8B5CF6",
                "#EC4899", "#14B8A6", "#F97316", "#0EA5E9", "#D946EF",
                "#FBBF24", "#34D399", "#6366F1", "#06B6D4", "#10B981",
                "#FF8C00", "#00BFFF", "#FF6347", "#9370DB", "#2E8B57",
                "#FFD700", "#00FA9A", "#DC143C", "#1E90FF", "#FF1493"
                ]
            }
        ]
    }

    # 生成输出文件
    output = "```echarts\n" + json.dumps(echarts_option, ensure_ascii=False, indent=2) + "\n```"
    
    return {
        "result": output,
        "total_count": len(final_records)
    }
