import csv
import os


def write_results_csv(output_tasks, new_output_tasks, input_file):
    try:
        # Define the output file names
        output_file_v1 = f"{os.path.basename(input_file)}_smells_v1.csv"
        output_file_v2 = f"{os.path.basename(input_file)}_smells_v2.csv"

        # Define the CSV column names
        csv_columns = ['Task name', 'Idempotency', 'Version specific installation', 'Outdated dependencies',
                       'Missing dependencies', 'Assumption about environment', 'Hardware specific commands',
                       'Broken Dependency']
        new_csv_columns = ['Repository Name', 'File Name', 'Line Number', 'Task Name', 'Smell Name',
                           'Smell Description']

        # Write task smells to CSV files
        with open(output_file_v1, 'w', newline='') as file_v1, open(output_file_v2, 'w', newline='') as file_v2:
            writer_v1 = csv.DictWriter(file_v1, fieldnames=new_csv_columns)
            writer_v1.writeheader()
            writer_v1.writerows(new_output_tasks)

            writer_v2 = csv.DictWriter(file_v2, fieldnames=csv_columns)
            writer_v2.writeheader()
            writer_v2.writerows(output_tasks)

    except Exception as e:
        print("Error occurred while writing CSV files:", str(e))
