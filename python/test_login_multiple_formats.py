import json
from login import main

print("Testing multiple input formats...\n")

# Test 1: New format - input with 'arg1' field
print("Test 1: New format with 'arg1' field")
test_input_1 = {
   "arg1": '{"code":200,"success":true,"data":{"accessToken":"test_token_new_format","tokenType":"bearer","userName":"biubiubiu"}}'
}
test_input_json_1 = json.dumps(test_input_1)
result_1 = main(test_input_json_1)
print(json.dumps(result_1, indent=2))
print()

# Test 2: Old format 1 - directly the response object (no outer structure)
print("Test 2: Old format - directly the response object")
test_input_2 = {
    "code": 200,
    "success": True,
    "data": {
        "accessToken": "test_token_old_format_1",
        "tokenType": "bearer",
        "userName": "biubiubiu"
    }
}
test_input_json_2 = json.dumps(test_input_2)
result_2 = main(test_input_json_2)
print(json.dumps(result_2, indent=2))
print()

# Test 3: Old format 2 - with 'body' field
print("Test 3: Old format with 'body' field")
test_input_3 = {
    "status_code": 200,
    "body": '{"code":200,"success":true,"data":{"accessToken":"test_token_old_format_2","tokenType":"bearer","userName":"biubiubiu"}}'
}
test_input_json_3 = json.dumps(test_input_3)
result_3 = main(test_input_json_3)
print(json.dumps(result_3, indent=2))
print()

# Test 4: Success=false case with new format
print("Test 4: New format with success=false")
test_input_4 = {
   "arg1": '{"code":400,"success":false,"data":{"accessToken":""},"msg":"登录失败"}'
}
test_input_json_4 = json.dumps(test_input_4)
result_4 = main(test_input_json_4)
print(json.dumps(result_4, indent=2))
print()

print("All tests completed!")