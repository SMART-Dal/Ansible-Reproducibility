# import numpy as np
# from scipy.stats import pearsonr
#
# # smell categories and corresponding metrics
# smell_categories = ["idempotency", "vsi", "od", "md", "aae", "hsc", "bd"]
# number_of_individual_detection = [5246, 15, 1047, 1603, 5438, 41, 12198]
#
# correlation_coefficients = []
# p_values = []
#
# # Calculate the Pearson correlation
# for category in smell_categories:
#     r, p = pearsonr(number_of_individual_detection, number_of_individual_detection)
#     correlation_coefficients.append(r)
#     p_values.append(p)
#
# # Print the correlation coefficients and p-values for each smell category
# for i, category in enumerate(smell_categories):
#     print(f"Correlation with {category}: {correlation_coefficients[i]} (p-value: {p_values[i]})")
# import numpy as np
# from scipy.stats import pearsonr
#
# smell_categories = ["idempotency", "vsi", "od", "md", "aae", "hsc", "bd"]
# counts = [5246, 15, 1047, 1603, 5438, 41, 12198]
#
# # Create a NumPy array from the counts
# data = np.array(counts)
#
# # Calculate the Pearson correlation coefficient and p-value
# correlation_coefficient, p_value = pearsonr(data, data)
#
# # Print the correlation coefficient and p-value
# print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
# print(f"P-Value: {p_value}")


# import numpy as np
# from scipy.stats import pearsonr
#
# # Define your smell categories
# smell_categories = ["idemp", "vsi", "od", "md", "aae", "hsc", "bd"]
#
# # Define the total number of times each category was detected individually
# individual_counts = [5246, 15, 1047, 1603, 5438, 41, 12198]  # Replace with your actual counts
#
# # Define the total number of times each pair of categories was detected
# pair_counts = [
#     [14, 938, 998, 1550, 31, 3307],
#     [14, 0, 10, 0, 12],
#     [0, 463, 0, 0],
#     [101, 0, 802],
#     [4, 3625],
#     [28],
# ]
#
# # Initialize correlation matrices for coefficients and p-values
# correlation_matrix = np.zeros((len(smell_categories), len(smell_categories)))
# p_value_matrix = np.zeros((len(smell_categories), len(smell_categories)))
#
# # Calculate correlation coefficients and populate the matrix
# for i in range(len(smell_categories)):
#     for j in range(i + 1, len(smell_categories)):
#         # Calculate the Pearson correlation coefficient
#         r, _ = pearsonr(individual_counts, pair_counts[i])
#         correlation_matrix[i, j] = r
#         correlation_matrix[j, i] = r  # Since the correlation is symmetric
#
# # Calculate p-values and populate the matrix
# for i in range(len(smell_categories)):
#     for j in range(i + 1, len(smell_categories)):
#         _, p = pearsonr(individual_counts, pair_counts[j])
#         p_value_matrix[i, j] = p
#         p_value_matrix[j, i] = p  # Since the p-value is symmetric
#
# # Print the correlation matrix and p-value matrix
# print("Correlation Matrix:")
# print(correlation_matrix)
# print("\nP-Value Matrix:")
# print(p_value_matrix)


import numpy as np
from scipy.stats import pearsonr

# both_present = [14, 938, 998, 1550, 31, 3307,
# 14, 0, 10, 0, 6,
# 0, 463, 549, 0,
# 101, 0, 802,
# 4, 3625,
# 28]
#
# neither_present = [26571, 26458, 25956, 22611, 26561, 17624,
# 30814, 30238, 26351, 31810, 19603,
# 29201, 25767, 30773, 19109,
# 24843, 30211, 18800,
# 26318, 17726,
# 19598]
#
# cat1_without_cat2 = [5281, 4357, 4297, 3745, 5264, 1988,
# 1, 15, 5, 15, 9,
# 1052, 589, 1052, 503,
# 1513, 1614, 812,
# 5507,1886,
# 14]
#
# cat2_without_cat1 = [1, 114, 616, 3961, 11, 8948,
# 1038, 1614, 5501, 42, 12249,
# 1614, 5048, 42, 11706,
# 5410, 42, 11453,
# 38, 8630,
# 1227]
#
#
# # Calculate the Pearson correlation coefficient and p-value
# correlation_coefficient, p_value = pearsonr(cat1_without_cat2, cat2_without_cat1)
#
# print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
# print(f"P-value: {p_value}")

# import numpy as np
# from scipy.stats import pearsonr
#
# cat1_without_cat2_idemp = [5281, 4357, 4297, 3745, 5264, 1988]
# cat1_without_cat2_vsi = [0, 1, 15, 11453, 8630, 12227]
# cat1_without_cat2_od = [8948, 12249, 11706, 11453, 8630, 12227]
# cat1_without_cat2_md = [8948, 12249, 11706, 11453, 8630, 12227]
# cat1_without_cat2_aae = [8948, 12249, 11706, 11453, 8630, 12227]
# cat1_without_cat2_hsc = [8948, 12249, 11706, 11453, 8630, 12227]
# cat1_without_cat2_bd = [8948, 12249, 11706, 11453, 8630, 12227]
#
# # Calculate the Pearson correlation coefficient and p-value
# correlation_coefficient, p_value = pearsonr(both_present, cat1_without_cat2)

# print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
# print(f"P-value: {p_value}")


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
                if value != column_name:
                    if value not in (None, 'None', 'Error', '', '\n'):
                        column_values.append(1)
                    else:
                        column_values.append(0)
            # percentage = (len(column_values)/(column_size/2))*100
            # percentage = len(column_values)
        return column_values
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # Get the path to the CSV file and the column name from the user
    csv_file = '/home/ghazal/Ansible-Reproducibility/Replication Package/combined_v2.csv'
    # column_name = 'Idempotency'

    # Get and print the column values
    # percentage = get_column_values(csv_file, column_name)
    # print(percentage)

    # Calculate the Pearson correlation coefficient and p-value
    correlation_coefficient, p_value = pearsonr(get_column_values(csv_file,'Version specific installation'), get_column_values(csv_file,'Idempotency'))

    print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
    print(f"P-value: {p_value}")
