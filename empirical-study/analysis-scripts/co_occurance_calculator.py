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
with open('/Replication Package/cleaned_combined_v1.csv', 'r') as csvfile:
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

