import requests

# URL of the running FastAPI app's OpenAPI endpoint
openapi_url = "http://127.0.0.1:8000/openapi.json"

# Fetch the OpenAPI JSON
response = requests.get(openapi_url)

# Save it to a file
if response.status_code == 200:
    with open("openapi.json", "w") as f:
        f.write(response.text)
    print("OpenAPI JSON saved as openapi.json")
else:
    print("Failed to fetch OpenAPI JSON:", response.status_code)
