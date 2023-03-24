import requests

headers = {"Authorization": "Bearer <GITHUB_ACCESS_TOKEN>"}

search_term = "ansible"

# Search for Ansible scripts on GitHub using the GitHub API
url = f"https://api.github.com/search/code?q=ansible+in:file+language:yaml+language:json+{search_term}"
response = requests.get(url, headers=headers)

try:
    results = response.json()["items"]
    for result in results:
        repository = result["repository"]["full_name"]
        path = result["path"]
        print(f"{repository}/{path}")
except KeyError:
    print("No results found or error with request.")
