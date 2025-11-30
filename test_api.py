import requests
import json

url = "http://localhost:8000/career-plan"
payload = {
    "user_id": "123",
    "category": "Android",
    "timeline": "1 week",
    "job_description": '''MVVM'''
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if response is not None:
        print(response.text)
