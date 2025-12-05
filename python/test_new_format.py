import json
from accountReq1 import main

# New test data format
json_str = '{"arg1": [{"taskId": "RT1440060004091183104"}, {"taskId": "RT1440056997022679040"}, {"taskId": "RT1435570226020892672"}]}'

# Call the function
result = main(json_str)

# Print the result
print("Result:")
print(result)
