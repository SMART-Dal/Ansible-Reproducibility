import requests
import json
import datetime

# GitHub API base URL
api_base_url = 'https://api.github.com/repos/'


# Function to check if a repository meets the criteria
def check_repository_criteria(repo_url):
    try:
        # Extract the GitHub username and repository name from the URL
        username, reponame = repo_url.split('/')[-2:]

        # Construct the API URL for the repository
        repo_api_url = f"{api_base_url}{username}/{reponame}"

        # Send a GET request to the GitHub API for repository details
        response = requests.get(repo_api_url)

        # Check if the request was successful
        if response.status_code == 200:
            repo_data = json.loads(response.text)

            # Check the criteria: more than 5 stars, 50 commits, last commit not older than 1 year ago
            if repo_data['stargazers_count'] > 5 and repo_data['commits'] > 50:
                last_commit_date = datetime.datetime.strptime(repo_data['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
                if last_commit_date > one_year_ago:
                    return True

        return False

    except Exception as e:
        print(f"Error checking repository {repo_url}: {str(e)}")
        return False


# Function to process a file containing GitHub repository links
def process_github_links_file(input_file, output_file):
    qualifying_links = []

    try:
        with open(input_file, 'r') as file:
            for line in file:
                repo_url = line.strip()
                if check_repository_criteria(repo_url):
                    qualifying_links.append(repo_url)

        # Save the qualifying links to the output file
        with open(output_file, 'w') as outfile:
            for link in qualifying_links:
                outfile.write(link + '\n')

        print(f"Saved {len(qualifying_links)} qualifying links to {output_file}.")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage:
github_links_file = 'development.txt'  # Replace with the name of your input file
output_file = 'qualifying_links.txt'  # Replace with the name of the output file

process_github_links_file(github_links_file, output_file)
