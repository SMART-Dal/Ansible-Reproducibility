# import os
# import csv
#
#
# def process_csv_files_in_directory(directory_path, output_file):
#     # Create or open the output combined CSV file in write mode
#     with open(output_file, 'w', newline='') as combined_csv:
#         csv_writer = csv.writer(combined_csv)
#
#         # Iterate through the directory tree
#         for root, _, files in os.walk(directory_path):
#             for filename in files:
#                 # Check if the file name ends with 'v2.csv'
#                 if filename.lower().endswith('v1.csv'):
#                     # Construct the full path to the CSV file
#                     csv_file_path = os.path.join(root, filename)
#
#                     # Process the CSV file and append its contents to the combined CSV file
#                     print(f"Appending CSV file: {csv_file_path}")
#                     with open(csv_file_path, 'r') as csv_file:
#                         csv_reader = csv.reader(csv_file)
#                         # Skip the header row if needed
#                         # next(csv_reader, None)  # Uncomment this line if the files have headers
#
#                         # Append the rows from the CSV file to the combined CSV
#                         for row in csv_reader:
#                             csv_writer.writerow(row)
#
#
# # Example usage:
# directory_path = '/home/ghazal/Ansible-Reproducibility/src/output'
# output_file = '/home/ghazal/Ansible-Reproducibility/src/combined_v1.csv'
# process_csv_files_in_directory(directory_path, output_file)

# import csv
#
# # Create a new CSV file to store the filtered data
# output_file = 'cleaned_combined_v1.csv'
#
# # Open the input CSV file and the output CSV file
# with open('/home/ghazal/Ansible-Reproducibility/src/combined_v1.csv', 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
#     reader = csv.DictReader(input_csv)
#     fieldnames = reader.fieldnames
#     writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
#
#     # Write the header row to the output CSV
#     writer.writeheader()
#
#     # Iterate through the rows of the input CSV
#     for row in reader:
#         smell_description = row['Smell Description'].strip()  # Remove leading/trailing whitespaces and '\n'
#
#         # Check if the 'Smell Description' is 'None', 'Error', or empty
#         if smell_description not in ('None', 'Error', ''):
#             # If not, write the row to the output CSV
#             writer.writerow(row)


# import csv
# from collections import defaultdict
#
# # Define the pairs you want to count
# pairs_to_count = [
#     ("Idempotency", "Version Specific Installation"),
#     ("Idempotency", "Outdated Dependencies"),
#     ("Idempotency", "Missing Dependencies"),
#     ("Idempotency", "Assumption about Environment"),
#     ("Idempotency", "Broken Dependency Chain"),
#     ("Version Specific Installation", "Outdated Dependencies"),
#     ("Version Specific Installation", "Missing Dependencies"),
#     ("Version Specific Installation", "Assumption about Environment"),
#     ("Version Specific Installation", "Broken Dependency Chain"),
#     ("Outdated Dependencies", "Missing Dependencies"),
#     ("Outdated Dependencies", "Assumption about Environment"),
#     ("Version Specific Installation", "Broken Dependency Chain"),
#     ("Missing Dependencies", "Assumption about Environment"),
#     ("Missing Dependencies", "Broken Dependency Chain"),
#     ("Hardware Specific Commands", "Idempotency"),
#     ("Hardware Specific Commands", "Version Specific Installation"),
#     ("Hardware Specific Commands", "Outdated Dependencies"),
#     ("Hardware Specific Commands", "Missing Dependencies"),
#     ("Hardware Specific Commands", "Assumption about Environment"),
#     ("Hardware Specific Commands", "Broken Dependency Chain"),
#     ("Assumption about Environment", "Broken Dependency Chain"),
# ]
#
# # Initialize a defaultdict to count pairs
# pair_counts = defaultdict(int)
#
# # Initialize a list to store the Smell Names for each task
# smell_names = []
#
# # Read the CSV file and process the data
# with open('/home/ghazal/Ansible-Reproducibility/src/cleaned_combined_v1.csv', 'r') as csvfile:
#     csvreader = csv.DictReader(csvfile)
#     current_task = None
#
#     for row in csvreader:
#         task_name = row['Task Name']
#         smell_name = row['Smell Name']
#
#         # Check if we have moved to a new task
#         if task_name != current_task:
#             # Process the previous task's smell names and update pair counts
#             for pair in pairs_to_count:
#                 if all(smell in smell_names for smell in pair):
#                     pair_counts[pair] += 1
#
#             # Reset the smell_names list for the new task
#             smell_names = []
#
#             # Update the current task
#             current_task = task_name
#
#         # Append the smell name to the list
#         smell_names.append(smell_name)
#
# # Process the last task's smell names
# for pair in pairs_to_count:
#     if all(smell in smell_names for smell in pair):
#         pair_counts[pair] += 1
#
# # Print the pair counts
# for pair, count in pair_counts.items():
#     print(f"{pair}: {count}")

# import csv
# from collections import defaultdict
#
# # Define the pairs you want to count
# pairs_to_count = [
#     ("Idempotency", "Version Specific Installation"),
#     ("Idempotency", "Outdated Dependencies"),
#     ("Idempotency", "Missing Dependencies"),
#     ("Idempotency", "Assumption about Environment"),
#     ("Idempotency", "Broken Dependency Chain"),
#     ("Version Specific Installation", "Outdated Dependencies"),
#     ("Version Specific Installation", "Missing Dependencies"),
#     ("Version Specific Installation", "Assumption about Environment"),
#     ("Version Specific Installation", "Broken Dependency Chain"),
#     ("Outdated Dependencies", "Missing Dependencies"),
#     ("Outdated Dependencies", "Assumption about Environment"),
#     ("Version Specific Installation", "Broken Dependency Chain"),
#     ("Missing Dependencies", "Assumption about Environment"),
#     ("Missing Dependencies", "Broken Dependency Chain"),
#     ("Hardware Specific Commands", "Idempotency"),
#     ("Hardware Specific Commands", "Version Specific Installation"),
#     ("Hardware Specific Commands", "Outdated Dependencies"),
#     ("Hardware Specific Commands", "Missing Dependencies"),
#     ("Hardware Specific Commands", "Assumption about Environment"),
#     ("Hardware Specific Commands", "Broken Dependency Chain"),
#     ("Assumption about Environment", "Broken Dependency Chain"),
# ]
#
# # Initialize a defaultdict to count pairs
# pair_counts = defaultdict(int)
#
# # Initialize a list to store the Smell Names for each task
# smell_names = []
#
# # Initialize a variable to count the total number of tasks
# total_tasks = 0
#
# # Read the CSV file and process the data
# with open('/home/ghazal/Ansible-Reproducibility/src/cleaned_combined_v1.csv', 'r') as csvfile:
#     csvreader = csv.DictReader(csvfile)
#     current_task = None
#
#     for row in csvreader:
#         task_name = row['Task Name']
#         smell_name = row['Smell Name']
#
#         # Check if we have moved to a new task
#         if task_name != current_task:
#             # Process the previous task's smell names and update pair counts
#             for pair in pairs_to_count:
#                 if all(smell in smell_names for smell in pair):
#                     pair_counts[pair] += 1
#
#             # Reset the smell_names list for the new task
#             smell_names = []
#
#             # Update the current task
#             current_task = task_name
#
#             # Increment the total number of tasks
#             total_tasks += 1
#
#         # Append the smell name to the list
#         smell_names.append(smell_name)
#
# # Process the last task's smell names
# for pair in pairs_to_count:
#     if all(smell in smell_names for smell in pair):
#         pair_counts[pair] += 1
#
# # Calculate and print the percentages
# for pair, count in pair_counts.items():
#     percentage = (count / total_tasks) * 100
#     print(f"{pair}: {percentage:.2f}%")

import csv
from collections import defaultdict

# Define the pairs you want to count
pairs_to_count = [
    ("Idempotency", "Version Specific Installation"),
    ("Idempotency", "Outdated Dependencies"),
    ("Idempotency", "Missing Dependencies"),
    ("Idempotency", "Assumption about Environment"),
    ("Idempotency", "Hardware Specific Commands"),
    ("Idempotency", "Broken Dependency Chain"),
    ("Version Specific Installation", "Outdated Dependencies"),
    ("Version Specific Installation", "Missing Dependencies"),
    ("Version Specific Installation", "Assumption about Environment"),
    ("Version Specific Installation", "Hardware Specific Commands"),
    ("Version Specific Installation", "Broken Dependency Chain"),
    ("Outdated Dependencies", "Missing Dependencies"),
    ("Outdated Dependencies", "Assumption about Environment"),
    ("Outdated Dependencies", "Hardware Specific Commands"),
    ("Outdated Dependencies", "Broken Dependency Chain"),
    ("Missing Dependencies", "Assumption about Environment"),
    ("Missing Dependencies", "Hardware Specific Commands"),
    ("Missing Dependencies", "Broken Dependency Chain"),
    ("Assumption about Environment", "Hardware Specific Commands"),
    ("Assumption about Environment", "Broken Dependency Chain"),
    ("Hardware Specific Commands", "Broken Dependency Chain"),

]

# Initialize a defaultdict to count pairs
pair_counts = defaultdict(int)

# Initialize a list to store the Smell Names for each task
smell_names = []

# Initialize a variable to count the total number of tasks
total_tasks = 0

# Read the CSV file and process the data
with open('/home/ghazal/Ansible-Reproducibility/src/cleaned_combined_v1.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    current_task = None

    for row in csvreader:
        task_name = row['Task Name']
        smell_name = row['Smell Name']

        # Check if we have moved to a new task
        if task_name != current_task:
            # Process the previous task's smell names and update pair counts
            for pair in pairs_to_count:
                first_element, second_element = pair

                if first_element not in smell_names and second_element not in smell_names:
                    pair_counts[pair] += 1

            # Reset the smell_names list for the new task
            smell_names = []

            # Update the current task
            current_task = task_name

            # Increment the total number of tasks
            total_tasks += 1

        # Append the smell name to the list
        smell_names.append(smell_name)

# Process the last task's smell names
for pair in pairs_to_count:
    first_element, second_element = pair

    if first_element in smell_names and second_element not in smell_names:
        pair_counts[pair] += 1

# Calculate and print the total number of tasks
print(f"Total number of tasks: {total_tasks}")

# Print the counts for each pair
for pair, count in pair_counts.items():
    print(f"{pair}: {count}")

