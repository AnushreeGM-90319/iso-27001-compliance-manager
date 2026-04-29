import requests

url = "http://127.0.0.1:5000/describe"

data = {"text": "AI in healthcare"}

response = requests.post(url, json=data)
print(response.json())