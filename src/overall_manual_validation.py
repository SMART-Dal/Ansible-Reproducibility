import os
import pandas as pd


def calculate_precision_recall(manual_df, cleaned_df):
    true_positives = len(set(manual_df['Smell Name']) & set(cleaned_df['Smell Name']))
    total_predicted_positives = len(set(cleaned_df['Smell Name']))
    total_actual_positives = len(set(manual_df['Smell Name']))

    precision = true_positives / total_predicted_positives if total_predicted_positives > 0 else 0
    recall = true_positives / total_actual_positives if total_actual_positives > 0 else 0

    return precision, recall


def process_subdirectories(root_directory):
    overall_true_positives = 0
    overall_total_predicted_positives = 0
    overall_total_actual_positives = 0

    for subdir, _, files in os.walk(root_directory):
        manual_files = [filename for filename in files if filename.endswith("manual.csv")]

        for manual_file in manual_files:
            cleaned_file = manual_file.replace("manual.csv", "cleaned.csv")
            manual_path = os.path.join(subdir, manual_file)
            cleaned_path = os.path.join(subdir, cleaned_file)

            if os.path.exists(cleaned_path):
                print(f"Processing files: {manual_path} and {cleaned_path}")
                manual_df = pd.read_csv(manual_path)
                cleaned_df = pd.read_csv(cleaned_path)
                tasks = set(manual_df['Task Name'])

                for task in tasks:
                    manual_task_df = manual_df[manual_df['Task Name'] == task]
                    cleaned_task_df = cleaned_df[cleaned_df['Task Name'] == task]

                    precision, recall = calculate_precision_recall(manual_task_df, cleaned_task_df)

                    overall_true_positives += precision * len(cleaned_task_df)
                    overall_total_predicted_positives += len(cleaned_task_df)
                    overall_total_actual_positives += len(manual_task_df)

                    print(f"Task: {task}")
                    print(f"Precision: {precision:.2f}")
                    print(f"Recall: {recall:.2f}")
                    print("=" * 30)

    overall_precision = overall_true_positives / overall_total_predicted_positives if overall_total_predicted_positives > 0 else 0
    overall_recall = overall_true_positives / overall_total_actual_positives if overall_total_actual_positives > 0 else 0

    print("Overall Precision:", overall_precision)
    print("Overall Recall:", overall_recall)


if __name__ == "__main__":
    # Replace "/path/to/root_directory" with the path to the root directory containing subdirectories
    root_directory = "/home/ghazal/Ansible-Reproducibility/src/output"

    process_subdirectories(root_directory)
