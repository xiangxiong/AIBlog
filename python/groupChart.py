import json
from collections import Counter

def generate_diff_types_pie_chart(final_records: list) -> dict:
    """
    基于final_records中的diffTypes生成饼状图数据，支持dify中echarts图表
    
    参数:
    final_records: list - 包含diffTypes字段的记录列表
    
    返回:
    dict - echarts饼状图配置
    """
    
    # 统计所有diffTypes的出现次数
    diff_types_counter = Counter()
    
    for record in final_records:
        if 'diffTypes' in record and record['diffTypes']:
            # diffTypes是一个列表，遍历每个类型进行计数
            for diff_type in record['diffTypes']:
                diff_types_counter[diff_type] += 1
    
    # 准备饼图数据
    pie_data = [
        {
            "name": diff_type,
            "value": count
        }
        for diff_type, count in diff_types_counter.items()
    ]
    
    # 生成echarts配置
    echarts_option = {
        "title": {
            "text": "调账差异类型分布",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": [item["name"] for item in pie_data]
        },
        "series": [
            {
                "name": "差异类型",
                "type": "pie",
                "radius": "50%",
                "center": ["50%", "60%"],
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "label": {
                    "show": True,
                    "formatter": "{b}: {d}%"
                }
            }
        ]
    }
    
    return {
        "echarts_option": echarts_option,
        "diff_types_count": dict(diff_types_counter),
        "total_count": sum(diff_types_counter.values())
    }

# 测试代码
if __name__ == "__main__":
    # 模拟final_records数据，基于之前运行结果的结构
    test_final_records = [
        {
            "taskId": "RT1445818378583564288",
            "diffTypes": ["有账单未提单", "平台账单异常"]
        },
        {
            "taskId": "RT1445784435763208192",
            "diffTypes": ["有账单未提单"]
        },
        {
            "taskId": "RT1445784351931654144",
            "diffTypes": ["平台账单异常"]
        },
        {
            "taskId": "RT1445784271208079360",
            "diffTypes": ["有账单未提单", "平台账单异常"]
        }
    ]
    
    result = generate_diff_types_pie_chart(test_final_records)
    print("饼状图配置:")
    print(json.dumps(result["echarts_option"], ensure_ascii=False, indent=2))
    print("\n差异类型统计:")
    print(result["diff_types_count"])
    print(f"\n总差异数: {result['total_count']}")