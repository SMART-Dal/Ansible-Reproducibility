import requests

headers = {"Authorization": "Bearer <GITHUB_ACCESS_TOKEN>"}

search_term = "ansible"

url = f"https://api.github.com/search/code?q=ansible+in:file+language:yaml+language:json+{search_term}"
response = requests.get(url, headers=headers)

# Parse the JSON response and extract the relevant information
results = response.json()["items"]
for result in results:
    repository = result["repository"]["full_name"]
    path = result["path"]
    print(f"{repository}/{path}")
