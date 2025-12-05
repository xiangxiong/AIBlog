import json
import os
import re

def main(json_str: str) -> dict:
    try:
        json_str = '''
            {
                "filename": "shanghai_stock_daily.html",
                "上证指数日线行情": [
                    {
                        "date": "2025-11-17 09:30:00",
                        "open": 3285.42,
                        "close": 3291.76,
                        "low": 3282.15,
                        "high": 3295.38,
                        "volume": 285678000000
                    },
                    {
                        "date": "2025-11-18 09:30:00",
                        "open": 3293.24,
                        "close": 3288.91,
                        "low": 3284.57,
                        "high": 3297.82,
                        "volume": 312456000000
                    },
                    {
                        "date": "2025-11-19 09:30:00",
                        "open": 3289.65,
                        "close": 3296.33,
                        "low": 3286.89,
                        "high": 3302.17,
                        "volume": 348792000000
                    },
                    {
                        "date": "2025-11-20 09:30:00",
                        "open": 3298.41,
                        "close": 3305.78,
                        "low": 3294.26,
                        "high": 3308.55,
                        "volume": 376234000000
                    },
                    {
                        "date": "2025-11-21 09:30:00",
                        "open": 3306.29,
                        "close": 3301.54,
                        "low": 3298.73,
                        "high": 3310.92,
                        "volume": 359871000000
                    },
                    {
                        "date": "2025-11-24 09:30:00",
                        "open": 3303.17,
                        "close": 3312.89,
                        "low": 3300.45,
                        "high": 3316.74,
                        "volume": 412358000000
                    },
                    {
                        "date": "2025-11-25 09:30:00",
                        "open": 3314.22,
                        "close": 3309.67,
                        "low": 3305.81,
                        "high": 3318.93,
                        "volume": 387629000000
                    },
                    {
                        "date": "2025-11-26 09:30:00",
                        "open": 3311.45,
                        "close": 3318.24,
                        "low": 3309.12,
                        "high": 3322.56,
                        "volume": 435187000000
                    },
                    {
                        "date": "2025-11-27 09:30:00",
                        "open": 3319.78,
                        "close": 3325.41,
                        "low": 3315.39,
                        "high": 3329.87,
                        "volume": 468923000000
                    },
                    {
                        "date": "2025-11-28 09:30:00",
                        "open": 3327.15,
                        "close": 3321.89,
                        "low": 3318.64,
                        "high": 3330.52,
                        "volume": 423569000000
                    }
                ]
            }
            '''

        # 预处理：清理非 JSON 部分
        json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if not json_match:
            return {"result": "Error: Invalid JSON format"}
        
        # 提取合法的 JSON 部分
        cleaned_json_str = json_match.group(0)
        
        # 解析JSON数据
        data = json.loads(cleaned_json_str)
        filename = data.get("filename", "stock_chart.html")
        stock_data = data.get("上证指数日线行情", [])
        
        # 准备数据格式
        dates = [item['date'].split(' ')[0] for item in stock_data]  # 提取日期部分（去掉时间）
        open_prices = [item['open'] for item in stock_data]
        close_prices = [item['close'] for item in stock_data]
        low_prices = [item['low'] for item in stock_data]
        high_prices = [item['high'] for item in stock_data]
        volumes = [item['volume'] / 1e8 for item in stock_data]  # 转换为亿单位
        
        # 构建ECharts配置
        echarts_config = {
            "title": {
                "text": "上证指数日线行情"
            },
            "legend": {
                "data": ["开盘价", "最高价", "最低价", "收盘价", "成交量"]
            },
            "tooltip": {},
            "dataset": {
                "source": [
                    ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量"],
                    *[[dates[i], open_prices[i], high_prices[i], low_prices[i], close_prices[i], volumes[i]] 
                      for i in range(len(dates))]
                ]
            },
            "xAxis": [
                {"type": "category", "gridIndex": 0},
                {"type": "category", "gridIndex": 1}
            ],
            "yAxis": [
                {
                    "gridIndex": 0,
                    "name": "价格趋势（单位：点）"
                },
                {
                    "gridIndex": 1,
                    "name": "成交量（单位：亿）"
                }
            ],
            "grid": [
                {"bottom": "55%"},
                {"top": "55%"}
            ],
            "series": [
                # 第一个网格中的折线图系列
                {"type": "line", "seriesLayoutBy": "row", "name": "开盘价"},
                {"type": "line", "seriesLayoutBy": "row", "name": "最高价"},
                {"type": "line", "seriesLayoutBy": "row", "name": "最低价"},
                {"type": "line", "seriesLayoutBy": "row", "name": "收盘价"},
                # 第二个网格中的柱状图系列
                {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1, "name": "成交量"}
            ]
        }
        
        # 生成输出文件
        output = "```echarts\n" + json.dumps(echarts_config, indent=2, ensure_ascii=False) + "\n```"
        
        # 返回结果
        return {
            "result": output
        }
    
    except Exception as e:
        return {
            "result": f"Error: {str(e)}"
        }