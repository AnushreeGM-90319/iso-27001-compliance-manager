import requests

BASE_URL = "http://127.0.0.1:5000"


# ---------------------------------------------------
# 1. HOME ENDPOINT
# ---------------------------------------------------
print("\nTesting /")

response = requests.get(f"{BASE_URL}/")

print(response.json())


# ---------------------------------------------------
# 2. DESCRIBE
# ---------------------------------------------------
print("\nTesting /describe")

response = requests.post(
    f"{BASE_URL}/describe",
    json={
        "text": "Artificial Intelligence in Healthcare"
    }
)

print(response.json())


# ---------------------------------------------------
# 3. GENERATE REPORT
# ---------------------------------------------------
print("\nTesting /generate-report")

response = requests.post(
    f"{BASE_URL}/generate-report",
    json={
        "text": "ISO 27001 Compliance"
    }
)

print(response.json())


# ---------------------------------------------------
# 4. ANALYSE DOCUMENT
# ---------------------------------------------------
print("\nTesting /analyse-document")

response = requests.post(
    f"{BASE_URL}/analyse-document",
    json={
        "text": "Passwords are stored in plain text and authentication is weak."
    }
)

print(response.json())


# ---------------------------------------------------
# 5. BATCH PROCESS
# ---------------------------------------------------
print("\nTesting /batch-process")

response = requests.post(
    f"{BASE_URL}/batch-process",
    json={
        "items": [
            "AI",
            "Cloud",
            "Cybersecurity"
        ]
    }
)

print(response.json())


# ---------------------------------------------------
# 6. STREAM ENDPOINT
# ---------------------------------------------------
print("\nTesting /generate-report-stream")

response = requests.get(
    f"{BASE_URL}/generate-report-stream?text=Cybersecurity",
    stream=True
)

for line in response.iter_lines():

    if line:
        print(line.decode())