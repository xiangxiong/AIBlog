import json
from login import main

# Test input with the new format
test_input = {
   "arg1": '{"code":200,"success":true,"data":{"accessToken":"test_token_456","tokenType":"bearer","userName":"biubiubiu"}}'
}

# Convert test input to JSON string
test_input_json = json.dumps(test_input)

# Call the main function
result = main(test_input_json)

# Print the result
print("Test Result (new format):")
print(json.dumps(result, indent=2))