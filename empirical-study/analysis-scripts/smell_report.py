import os
import csv
from collections import defaultdict

SMELLS = [
    "Idempotency",
    "Version Specific Installation",
    "Outdated Dependencies",
    "Missing Dependencies",
    "Hardware Specific Commands",
    "Assumption about Environment",
    "Broken Dependency Chain"
]


def read_csv(file_path):
    data = defaultdict(list)
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = (row['Repository Name'], row['File Name'], row['Line Number'], row['Task Name'])
            data[key].append(row['Smell Name'])
    return data


def calculate_metrics(cleaned_data, manual_data, smell):
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for key, cleaned_smells in cleaned_data.items():
        manual_smells = manual_data.get(key, [])

        for c_smell in cleaned_smells:
            if c_smell == smell:
                if c_smell in manual_smells:
                    true_positive += 1
                else:
                    false_positive += 1

        for m_smell in manual_smells:
            if m_smell == 'None':
                true_negative += 1

        for m_smell in manual_smells:
            if m_smell == smell:
                if smell not in cleaned_smells:
                    false_negative += 1

    return true_positive, false_positive, true_negative, false_negative


def main():
    directory_path = "/Replication Package/Manual validation"

    smell_data = defaultdict(int)
    total_true_positive = defaultdict(int)
    total_false_positive = defaultdict(int)
    total_true_negative = defaultdict(int)
    total_false_negative = defaultdict(int)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('_cleaned.csv'):
                cleaned_path = os.path.join(root, file)
                manual_path = os.path.join(root, file.replace('_cleaned.csv', '_manual.csv'))

                cleaned_data = read_csv(cleaned_path)
                manual_data = read_csv(manual_path)

                for smell in SMELLS:
                    true_positive, false_positive, true_negative, false_negative = calculate_metrics(cleaned_data,
                                                                                                     manual_data, smell)

                    smell_data[smell] += 1
                    total_true_positive[smell] += true_positive
                    total_false_positive[smell] += false_positive
                    total_true_negative[smell] += true_negative
                    total_false_negative[smell] += false_negative

    for smell in SMELLS:
        total_samples = total_true_positive[smell] + total_false_positive[smell] + total_true_negative[smell] + \
                        total_false_negative[smell]

        if total_samples == 0:
            print(f"No samples found for {smell}.")
            continue

        print(f"Metrics for Smell: {smell}")
        print(f"Total True Positive: {total_true_positive[smell]}")
        print(f"Total False Positive: {total_false_positive[smell]}")
        print(f"Total True Negative: {total_true_negative[smell]}")
        print(f"Total False Negative: {total_false_negative[smell]}")

        smell_accuracy = (total_true_positive[smell] + total_true_negative[smell]) / total_samples * 100
        smell_false_positive_percentage = (total_false_positive[smell] / total_samples) * 100
        smell_false_negative_percentage = (total_false_negative[smell] / total_samples) * 100
        smell_true_positive_percentage = (total_true_positive[smell] / total_samples) * 100
        smell_true_negative_percentage = (total_true_negative[smell] / total_samples) * 100

        print(f"Accuracy for {smell}: {smell_accuracy:.2f}%")
        print(f"False Positive Percentage: {smell_false_positive_percentage:.2f}%")
        print(f"False Negative Percentage: {smell_false_negative_percentage:.2f}%")
        print(f"True Positive Percentage: {smell_true_positive_percentage:.2f}%")
        print(f"True Negative Percentage: {smell_true_negative_percentage:.2f}%")
        print()


if __name__ == "__main__":
    main()
