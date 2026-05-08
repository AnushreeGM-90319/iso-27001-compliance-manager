import requests

url = "http://127.0.0.1:5000/analyse-document"

data = {
    "text": "The system stores user passwords in plain text and has no authentication checks."
}

response = requests.post(url, json=data)

print(response.json())