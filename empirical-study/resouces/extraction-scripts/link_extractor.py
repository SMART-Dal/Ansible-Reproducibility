import requests
import json
import re


def extract_git_links(url, output_file):
    try:
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
                with open(output_file, 'w') as txt_file:
                    for link in git_links:
                        txt_file.write(link + '\n')

                print(
                    f"Found {len(git_links)} links containing 'git' in 'results' under 'collection' and 'content' keys (excluding 'issues') and saved them to {output_file}.")

            except json.JSONDecodeError:
                print("Error parsing JSON response.")
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def remove_duplicates(input_file, output_file):
    try:
        # Initialize a set to store unique lines
        unique_lines = set()

        # Open the input file for reading
        with open(input_file, 'r') as infile:
            for line in infile:
                # Strip leading and trailing whitespace from the line
                cleaned_line = line.strip()

                # Check if the line is not already in the set of unique lines
                if cleaned_line not in unique_lines:
                    unique_lines.add(cleaned_line)

        # Open the output file for writing
        with open(output_file, 'w') as outfile:
            # Write the unique lines back to the output file
            for line in unique_lines:
                outfile.write(line + '\n')

        print(f"Removed duplicates from {input_file} and saved the unique lines to {output_file}.")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def remove_git_commits_from_file(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Remove '/git/commits/numbers' from the end of each line
                cleaned_line = line.strip().rsplit('/git/commits/', 1)[0]
                outfile.write(cleaned_line + '\n')
        print(f"Processed {input_file} and saved the cleaned data to {output_file}.")
    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    url = 'https://galaxy.ansible.com/api/internal/ui/search/?deprecated=false&tags=security&keywords=&order_by=-download_count&page=1&page_size=100'
    git_links_file = 'git_links.txt'
    deduplicated_file = 'deduplicated_links.txt'
    final_output_file = 'cleaned_links.txt'

    extract_git_links(url, git_links_file)
    remove_duplicates(git_links_file, deduplicated_file)
    remove_git_commits_from_file(deduplicated_file, final_output_file)


if __name__ == "__main__":
    main()
