import json
from login import main

# Simple test input with a shorter accessToken
test_input = {
   "status_code": 200,
   "body": '{"code":200,"success":true,"data":{"accessToken":"test_token_123","tokenType":"bearer","userName":"biubiubiu"}}'
}

# Convert test input to JSON string
test_input_json = json.dumps(test_input)

# Call the main function
result = main(test_input_json)

# Print the result
print("Test Result:")
print(json.dumps(result, indent=2))