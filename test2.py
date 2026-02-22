import requests

# Simple connectivity test
try:
    r = requests.get("http://127.0.0.1:8000/docs")
    print("GET /docs:", r.status_code)
except Exception as e:
    print("Connection error:", e)

# Test upload endpoint
try:
    with open("q-fastapi-file-validation.csv", "rb") as f:
        r = requests.post(
            "http://127.0.0.1:8000/upload",
            files={"file": ("q-fastapi-file-validation.csv", f, "text/csv")},
            headers={"X-Upload-Token-5889": "ocj4rq3opn4c934t"},
        )
    print("POST /upload:", r.status_code)
    print(r.json())
except Exception as e:
    print("Upload error:", e)