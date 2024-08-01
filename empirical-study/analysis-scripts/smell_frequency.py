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
#                 if filename.lower().endswith('v2.csv'):
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
# directory_path = ''
# output_file = ''
# process_csv_files_in_directory(directory_path, output_file)


import csv


def get_column_values(csv_file, column_name):
    column_size = 0
    try:
        column_values = []
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            if column_name not in reader.fieldnames:
                return f"Column '{column_name}' not found in the CSV file."
            for row in reader:
                column_size = column_size + 1
                value = row[column_name].strip()  # Remove leading/trailing whitespace

                # Check if the value should be excluded
                if value not in (None, 'None', 'Error', '', '\n') and (value != column_name):
                    column_values.append(value)
            # percentage = (len(column_values)/(column_size/2))*100
            percentage = len(column_values)
        return percentage
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # Get the path to the CSV file and the column name from the user
    csv_file = '/Replication Package/combined_v2.csv'
    column_name = 'Broken Dependency'

    # Get and print the column values
    percentage = get_column_values(csv_file, column_name)
    print(percentage)

    # if isinstance(values, list):
    #     print(f"Values in column '{column_name}':")
    #     for value in values:
    #         print(value)
    # else:
    #     print(values)





