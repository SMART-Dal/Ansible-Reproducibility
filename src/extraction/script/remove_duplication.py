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


# Example usage:
input_file = 'dup-sec.txt'  # Replace with the name of your input file
output_file = 'security.txt'  # Replace with the name of the output file you want to create

remove_duplicates(input_file, output_file)
