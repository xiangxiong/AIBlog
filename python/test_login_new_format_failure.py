import json
from login import main

# Test input with the new format and success=false
test_input = {
   "arg1": '{"code":400,"success":false,"data":{"accessToken":""},"msg":"登录失败"}'
}

# Convert test input to JSON string
test_input_json = json.dumps(test_input)

# Call the main function
result = main(test_input_json)

# Print the result
print("Test Result (new format, success=false):")
print(json.dumps(result, indent=2))