import json
from accountReq1 import main

# Test data
json_str = '{"code":200,"success":true,"data":{"records":[{"taskId":"RT1440060004091183104","parentErpDeptId":"99999992","parentErpDeptName":"湖南北区","erpDeptId":"542","erpDeptName":"湖南公司长沙新民路口店","channel":"美团O2O","accountDate":"2025-10","originDiffCount":11,"originDiffAmount":382.48,"presentDiffCount":10,"presentDiffAmount":355.11,"channelId":"753844295290589184","userId":"10009613","userName":"周文桃","createTime":"2025-11-17 19:24:20","taskStatus":3,"orderCount":11,"finishOrderCount":11},{"taskId":"RT1440056997022679040","parentErpDeptId":"99999992","parentErpDeptName":"湖南北区","erpDeptId":"542","erpDeptName":"湖南公司长沙新民路口店","channel":"美团O2O","accountDate":"2025-10","originDiffCount":11,"originDiffAmount":382.48,"presentDiffCount":10,"presentDiffAmount":355.11,"channelId":"753844295290589184","userId":"10009613","userName":"周文桃","createTime":"2025-11-17 19:12:23","taskStatus":3,"orderCount":11,"finishOrderCount":11},{"taskId":"RT1435570226020892672","parentErpDeptId":"611","parentErpDeptName":"安徽百姓缘大药房连锁有限公司","erpDeptId":"13273","erpDeptName":"百姓缘淮南银鹭店","channel":"饿百O2O","accountDate":"2025-10","originDiffCount":5,"originDiffAmount":221.60,"presentDiffCount":5,"presentDiffAmount":221.60,"channelId":"753844107780034560","userId":"10009613","userName":"周文桃","createTime":"2025-11-05 10:03:33","taskStatus":3,"orderCount":5,"finishOrderCount":5}],"total":3,"size":10,"current":1},"msg":"操作成功"}'

# Call the function
result = main(json_str)

# Print the result
print("Extracted taskIds:")
print(result)
