import json

def main(arg1:str) -> dict:

    # Parse the JSON string
    data = json.loads(arg1)
    
    # Get the list of task objects from arg1 field
    task_list = data.get('arg1', [])
    
    # Extract all taskIds into a list
    task_ids = [task['taskId'] for task in task_list]

    return {
        "taskId": task_ids
    }