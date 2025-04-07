import requests

# API endpoint
url = "http://0.0.0.0:8000"

# Request payload
payload = {
    "prompt": "What is the capital of France?",
    "max_tokens": 50,
    "temperature": 0.7,
}

# Send the request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    print(response.json()["choices"][0]["text"])
else:
    print(f"Error: {response.status_code}, {response.text}")
