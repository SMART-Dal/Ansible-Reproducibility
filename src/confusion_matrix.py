# import os
# import csv
# from collections import defaultdict
#
#
# def read_csv(file_path):
#     data = defaultdict(list)
#     with open(file_path, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             key = (row['Repository Name'], row['File Name'], row['Line Number'], row['Task Name'])
#             data[key].append(row['Smell Name'])
#     return data
#
#
# def calculate_metrics(cleaned_data, manual_data):
#     true_positive = 0
#     false_positive = 0
#     true_negative = 0
#     false_negative = 0
#
#     for key, cleaned_smells in cleaned_data.items():
#         manual_smells = manual_data.get(key, [])
#
#         for smell in cleaned_smells:
#             if smell in manual_smells:
#                 true_positive += 1
#             else:
#                 false_positive += 1
#
#         for smell in manual_smells:
#             if smell == 'None':
#                 true_negative += 1
#
#         for smell in cleaned_smells:
#             if smell == 'None' and smell not in manual_smells:
#                 false_negative += 1
#
#     return true_positive, false_positive, true_negative, false_negative
#
#
# def calculate_accuracy(true_positive, true_negative, total_samples):
#     return (true_positive + true_negative) / total_samples
#
#
# def calculate_overall_metrics(directory_path):
#     overall_true_positive = 0
#     overall_false_positive = 0
#     overall_true_negative = 0
#     overall_false_negative = 0
#
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             if file.endswith('_cleaned.csv'):
#                 cleaned_path = os.path.join(root, file)
#                 manual_path = os.path.join(root, file.replace('_cleaned.csv', '_manual.csv'))
#
#                 cleaned_data = read_csv(cleaned_path)
#                 manual_data = read_csv(manual_path)
#
#                 true_positive, false_positive, true_negative, false_negative = calculate_metrics(cleaned_data,
#                                                                                                  manual_data)
#
#                 overall_true_positive += true_positive
#                 overall_false_positive += false_positive
#                 overall_true_negative += true_negative
#                 overall_false_negative += false_negative
#
#     return overall_true_positive, overall_false_positive, overall_true_negative, overall_false_negative
#
#
# def main():
#     directory_path = "/home/ghazal/Ansible-Reproducibility/Replication Package/Manual validation"
#     overall_true_positive, overall_false_positive, overall_true_negative, overall_false_negative = calculate_overall_metrics(
#         directory_path)
#
#     total_samples = overall_true_positive + overall_false_positive + overall_true_negative + overall_false_negative
#
#     if total_samples == 0:
#         print("No samples found.")
#         return
#
#     overall_accuracy = calculate_accuracy(overall_true_positive, overall_true_negative, total_samples)
#     overall_true_positive_percentage = (overall_true_positive / total_samples) * 100
#     overall_false_positive_percentage = (overall_false_positive / total_samples) * 100
#     overall_true_negative_percentage = (overall_true_negative / total_samples) * 100
#     overall_false_negative_percentage = (overall_false_negative / total_samples) * 100
#
#     print("Overall Metrics:")
#     print(f"Overall True Positive Percentage: {overall_true_positive_percentage:.2f}%")
#     print(f"Overall False Positive Percentage: {overall_false_positive_percentage:.2f}%")
#     print(f"Overall True Negative Percentage: {overall_true_negative_percentage:.2f}%")
#     print(f"Overall False Negative Percentage: {overall_false_negative_percentage:.2f}%")
#     print(f"Overall Accuracy: {overall_accuracy:.2f}%")
#
#
# if __name__ == "__main__":
#     main()

def calculate_metrics(TP, TN, FP, FN):
    # Precision
    precision = TP / (TP + FP)

    # Recall (Sensitivity)
    recall = TP / (TP + FN)

    # Matthews Correlation Coefficient (MCC)
    mcc = (TP * TN - FP * FN) / ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))**0.5

    # F1 Score
    f1_score = 2 * (precision * recall) / (precision + recall)

    return precision, recall, mcc, f1_score


precision, recall, mcc, f1_score = calculate_metrics(574, 203, 61, 6)

print("Precision:", precision)
print("Recall:", recall)
print("MCC:", mcc)
print("F1 Score:", f1_score)