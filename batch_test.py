import requests

url = "http://127.0.0.1:5000/batch-process"

data = {
    "items": [
        "AI",
        "Cybersecurity",
        "Cloud Computing"
    ]
}

response = requests.post(url, json=data)

print(response.json())