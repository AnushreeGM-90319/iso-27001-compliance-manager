import requests
import time

BASE_URL = "http://127.0.0.1:5000"

results = []


# ---------------------------------------------------
# Helper function
# ---------------------------------------------------
def test_endpoint(name, method, endpoint, payload=None):

    start = time.time()

    try:

        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")

        elif method == "POST":
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=payload
            )

        end = time.time()

        response_time = round(end - start, 2)

        print(f"\n{name}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time} seconds")

        results.append({
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_time_seconds": response_time
        })

    except Exception as e:

        print(f"\n{name} FAILED")
        print(str(e))

        results.append({
            "endpoint": endpoint,
            "status_code": "FAILED",
            "response_time_seconds": "ERROR"
        })


# ---------------------------------------------------
# 1. Home Endpoint
# ---------------------------------------------------
test_endpoint(
    "HOME ENDPOINT",
    "GET",
    "/"
)


# ---------------------------------------------------
# 2. Describe Endpoint
# ---------------------------------------------------
test_endpoint(
    "DESCRIBE ENDPOINT",
    "POST",
    "/describe",
    {
        "text": "Artificial Intelligence in Healthcare"
    }
)


# ---------------------------------------------------
# 3. Generate Report Endpoint
# ---------------------------------------------------
test_endpoint(
    "GENERATE REPORT ENDPOINT",
    "POST",
    "/generate-report",
    {
        "text": "ISO 27001 Compliance"
    }
)


# ---------------------------------------------------
# 4. Analyse Document Endpoint
# ---------------------------------------------------
test_endpoint(
    "ANALYSE DOCUMENT ENDPOINT",
    "POST",
    "/analyse-document",
    {
        "text": "Passwords are stored in plain text and authentication is weak."
    }
)


# ---------------------------------------------------
# 5. Batch Process Endpoint
# ---------------------------------------------------
test_endpoint(
    "BATCH PROCESS ENDPOINT",
    "POST",
    "/batch-process",
    {
        "items": [
            "AI",
            "Cloud",
            "Cybersecurity"
        ]
    }
)


# ---------------------------------------------------
# 6. Streaming Endpoint
# ---------------------------------------------------
start = time.time()

response = requests.get(
    f"{BASE_URL}/generate-report-stream?text=Cybersecurity",
    stream=True
)

for line in response.iter_lines():
    if line:
        pass

end = time.time()

stream_time = round(end - start, 2)

print("\nSTREAM ENDPOINT")
print(f"Status Code: {response.status_code}")
print(f"Response Time: {stream_time} seconds")

results.append({
    "endpoint": "/generate-report-stream",
    "status_code": response.status_code,
    "response_time_seconds": stream_time
})


# ---------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------
print("\n============================")
print("FINAL RESPONSE TIME REPORT")
print("============================")

for item in results:
    print(item)