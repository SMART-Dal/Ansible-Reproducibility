import requests

headers = {"Authorization": "Bearer <GITHUB_ACCESS_TOKEN>"}

search_term = "ansible"

# Search for Ansible scripts on GitHub using the GitHub API
url = f"https://github.com/oracle/oci-ansible-collection/tree/master/samples"
url2 = 'https://galaxy.ansible.com/search?deprecated=false&tags=system&keywords=&order_by=-relevance'
url3 = 'https://galaxy.ansible.com/search?deprecated=false&tags=networking&keywords=&order_by=-relevance'
url4 = 'https://galaxy.ansible.com/search?deprecated=false&tags=cloud&keywords=&order_by=-relevance'
url5 = 'https://galaxy.ansible.com/search?deprecated=false&tags=database&keywords=&order_by=-relevance'
url6 = 'https://galaxy.ansible.com/search?deprecated=false&tags=monitoring&keywords=&order_by=-relevance'
url7 = 'https://galaxy.ansible.com/search?deprecated=false&tags=security&keywords=&order_by=-relevance'
url8 = 'https://galaxy.ansible.com/search?deprecated=false&tags=web&keywords=&order_by=-relevance'

response = requests.get(url, headers=headers)

try:
    results = response.json()["items"]
    for result in results:
        repository = result["repository"]["full_name"]
        path = result["path"]
        print(f"{repository}/{path}")
except KeyError:
    print("No results found or error with request.")
