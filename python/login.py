import json

def main(arg1:str) -> dict:
    # Parse the input JSON string
    input_data = json.loads(arg1)
    
    # Determine the input format and extract the body
    if 'arg1' in input_data:
        # New format: input is an object with 'arg1' field containing the response JSON string
        body = json.loads(input_data['arg1'])
    elif 'body' in input_data:
        # Old format 2: input is an object with 'body' field containing the response JSON string
        body = json.loads(input_data['body'])
    else:
        # Old format 1: input is directly the response JSON object
        body = input_data
    
    # Extract success status and accessToken
    success = body.get('success', False)
    access_token = body['data'].get('accessToken', '') if success else ''
    
    return {
        "success": success,
        "accessToken": access_token
    }