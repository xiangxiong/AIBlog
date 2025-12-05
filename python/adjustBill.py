import requests
import json

# Define the URL
url = "https://mall-admin-uat.lbxcn.com/scc-finance/finance/reconciliation/task/pageList"

# Define the headers
headers = {
    "appId": "836021804215570432",
    "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0",
    "sec-ch-ua-platform": "Windows",
    "Referer": "",
    "sec-ch-ua": 'Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "scc-auth": "bearer eyJ0eXAiOiJKc29uV2ViVG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIxMDAwMDAxIiwiZGVwdF9jb2RlIjoiIiwidXNlcl9pZCI6IjE4IiwidXNlcl9uYW1lIjoiYml1Yml1Yml1IiwiZW52IjoidWF0IiwiZGVwdF9pZCI6Ii0xIiwiYWNjb3VudCI6ImJpdWJpdWJpdSIsInJvbGVfaWRzIjoiW3tcInJvbGVJZFwiOjgzNjAyNTk1NDM0OTM1NTAwOCxcInRlbmFudElkXCI6LTEsXCJ0ZW5hbnRDb2RlXCI6XCJcIixcImRhdGFTY29wZVwiOjEsXCJyb2xlVHlwZVwiOjEsXCJjaGFubmVsU2NvcGVcIjotMSxcImRlcHREVE9MaXN0XCI6W10sXCJjaGFubmVsRFRPTGlzdFwiOltdfV0iLCJjbGllbnRfaWQiOiJzYWJlciIsImV4cCI6MTc2NDk2MTIwMCwibmJmIjoxNzY0ODk4MzI0fQ.FwmQXtsNPpPYc22DlL8mZ5lsa6VYyRG82_B5fYpCx2A"
}

# Define the request body
payload = {
    "appId": "836021804215570432",
    "current": 1,
    "isPage": 1,
    "page": 1,
    "pageSize": 10,
    "roleId": "836025954349355008",
    "tenantId": 1000001,
    "userId": "18"
}

try:
    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Print the response status code
    print(f"Response Status Code: {response.status_code}")
    
    # Print the response content in a readable format
    print("Response Content:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
