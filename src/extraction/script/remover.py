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


input_file = 'git_links.txt'  # Replace with the name of your input file
output_file = 'dup-sec.txt'  # Replace with the name of the output file you want to create

remove_git_commits_from_file(input_file, output_file)