import requests
import json
import re
import datetime

def extract_git_links():

    # URL to fetch the JSON response
    url = 'https://galaxy.ansible.com/api/internal/ui/search/?deprecated=false&tags=security&keywords=&order_by=-download_count&page=1&page_size=100'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = json.loads(response.text)

            # Regular expression pattern to match URLs containing 'git'
            git_url_pattern = r'(https?://[^\s/$.?#].[^\s]*)'

            # List to store matching URLs
            git_links = []

            # Function to check if a URL contains 'issues'
            def contains_issues(url):
                return 'issues' not in url

            # Function to recursively search for 'git' URLs in nested dictionaries
            def search_git_urls(data_dict):
                for key, value in data_dict.items():
                    if isinstance(value, dict):
                        search_git_urls(value)
                    elif isinstance(value, str) and re.search(git_url_pattern, value) and contains_issues(value):
                        git_links.append(value)

            # Iterate through the 'results' list in the 'collection' dictionary
            for item in data['collection']['results']:
                search_git_urls(item)

            # Iterate through the 'results' list in the 'content' dictionary
            for item in data['content']['results']:
                search_git_urls(item)

            # Save the matching links to a text file
            with open('git_links.txt', 'w') as txt_file:
                for link in git_links:
                    txt_file.write(link + '\n')

            print(
                f"Found {len(git_links)} links containing 'git' in 'results' under 'collection' and 'content' keys (excluding 'issues') and saved them to git_links.txt.")

        except json.JSONDecodeError:
            print("Error parsing JSON response.")
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")


extract_git_links()
