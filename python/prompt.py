import json 
 
def main(dify_json_str: str) -> dict: 
    """ 
    解析Dify返回的JSON字符串，处理必填项校验和字段提取 
    :param dify_json_str: Dify返回的JSON字符串 
    :return: 解析后的字典，包含是否成功的标识 
    """ 
    try: 
        result = json.loads(dify_json_str) 
        # 检查必填项是否齐全 
        if result.get("error_msg"): 
            return { 
                "success": False, 
                "message": result["error_msg"], 
                "data": None 
            } 
        # 提取有效数据 
        data = { 
            "time": result.get("time", ""), 
            "platform": result.get("platform", ""), 
            "creator": result.get("creator", ""), 
            "company_store": result.get("company_store", ""), 
            "task_id": result.get("task_id", "") 
        } 
        return { 
            "success": True, 
            "message": "信息提取成功", 
            "data": data 
        } 
    except json.JSONDecodeError: 
        return { 
            "success": False, 
            "message": "解析返回数据失败，请检查格式", 
            "data": None 
        }