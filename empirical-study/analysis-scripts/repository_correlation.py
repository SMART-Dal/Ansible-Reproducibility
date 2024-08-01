import csv

from scipy.stats import spearmanr


# Function to calculate Spearman correlation
def calculate_spearman_correlation(file_path, column1_name, column2_name):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append((float(row[column1_name]), float(row[column2_name])))

    # Calculate the Spearman correlation
    correlation, _ = spearmanr(data)
    return correlation


# Provide the file path and column names
file_path = '/home/ghazal/Ansible-Reproducibility/src/output.csv'
column1_name = 'Hardware Specific Commands'
column2_name = 'Broken Dependency Chain'

# Calculate and print the Spearman correlation
correlation = calculate_spearman_correlation(file_path, column1_name, column2_name)
print(f"Spearman Correlation between {column1_name} and {column2_name}: {correlation}")

# import csv
# from collections import defaultdict
#
# # Initialize a dictionary to store smell counts and task counts for each repository
# repository_data = defaultdict(lambda: {'smell_counts': defaultdict(int), 'total_tasks': 0})
#
# # Read the input CSV file
# with open('/home/ghazal/Ansible-Reproducibility/Replication Package/combined csv files/cleaned_combined_v1.csv', mode='r', newline='') as input_file:
#     csv_reader = csv.DictReader(input_file)
#
#     # Iterate through each row in the CSV file
#     for row in csv_reader:
#         repository_name = row['Repository Name']
#         smell_name = row['Smell Name']
#
#         # Increment the count for the specific smell in the repository
#         repository_data[repository_name]['smell_counts'][smell_name] += 1
#
#         # Increment the total task count for the repository
#         repository_data[repository_name]['total_tasks'] += 1
#
# # Create a list to store the rows for the output CSV
# output_rows = []
#
# # Iterate through the repository_data dictionary and create rows for the output CSV
# for repository_name, data in repository_data.items():
#     smell_count = data['smell_counts']
#     total_tasks = data['total_tasks']
#
#     # Calculate the ratio of each smell count to the total tasks
#     smell_ratios = {smell: count / total_tasks for smell, count in smell_count.items()}
#
#     output_row = {
#         'Repository Name': repository_name,
#         'Broken Dependency Chain': smell_ratios.get('Broken Dependency Chain', 0),
#         'Idempotency': smell_ratios.get('Idempotency', 0),
#         'Outdated Dependencies': smell_ratios.get('Outdated Dependencies', 0),
#         'Assumption about Environment': smell_ratios.get('Assumption about Environment', 0),
#         'Version Specific Installation': smell_ratios.get('Version Specific Installation', 0),
#         'Hardware Specific Commands': smell_ratios.get('Hardware Specific Commands', 0)
#     }
#     output_rows.append(output_row)
#
# # Write the output to a new CSV file
# output_file = 'output.csv'
# with open(output_file, mode='w', newline='') as csvfile:
#     fieldnames = ['Repository Name', 'Broken Dependency Chain', 'Idempotency', 'Outdated Dependencies',
#                   'Assumption about Environment', 'Version Specific Installation', 'Hardware Specific Commands']
#     csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     csv_writer.writeheader()
#     csv_writer.writerows(output_rows)
#
# print(f"Output written to {output_file}")

