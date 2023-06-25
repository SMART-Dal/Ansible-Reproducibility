import csv


def write_results_csv(output_tasks, new_output_tasks, input_file):
    try:
        # Create lists to generate output file
        csv_columns = ['Task name', 'Idempotency', 'Version specific installation', 'Outdated dependencies',
                       'Missing dependencies', 'Assumption about environment', 'Hardware specific commands',
                       'Broken Dependency']
        new_csv_columns = ['Repository Name', 'File Name', 'Line Number', 'Task Name', 'Smell Name',
                           'Smell Description']
        # Output file name
        output_file = input_file.split('/')[-1] + '_smells_v1.csv'
        output_file2 = input_file.split('/')[-1] + '_smells_v2.csv'

        # Write task smells to CSV file
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_csv_columns)
            writer.writeheader()
            writer.writerows(new_output_tasks)

        with open(output_file2, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(output_tasks)

    except Exception as e:
        print("Error occurred while writing CSV file:", str(e))
