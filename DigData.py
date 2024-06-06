import re
import csv


def extract_and_save_metrics(filenames, output_csv):
    # Regex patterns to extract the required metrics
    training_time_pattern = re.compile(r'Training time:\s+(\d+\.\d+)\s+seconds')
    rules_pattern = re.compile(r'rules:\s+(\d+)')
    accuracy_pattern = re.compile(r'Accuracy:\s+(\d+\.\d+)%')
    precision_pattern = re.compile(r'Precision:\s+(\d+\.\d+)%')
    recall_pattern = re.compile(r'Recall / True Positive Rate:\s+(\d+\.\d+)%')
    fpr_pattern = re.compile(r'False Positive Rate:\s+(\d+\.\d+)%')
    f1_pattern = re.compile(r'F1 Score:\s+(\d+\.\d+)%')

    # Prepare the header for the CSV
    header = ["Filename", "Training Time (s)", "Rules", "Accuracy (%)", "Precision (%)", "Recall (%)",
              "False Positive Rate (%)", "F1 Score (%)"]

    # Open the CSV file to write the extracted metrics
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

        # Iterate over each file and extract the metrics
        for filename in filenames:
            with open(filename, 'r') as file:
                content = file.read()

                # Extract metrics using regex
                training_time = training_time_pattern.search(content)
                rules = rules_pattern.search(content)
                accuracy = accuracy_pattern.search(content)
                precision = precision_pattern.search(content)
                recall = recall_pattern.search(content)
                fpr = fpr_pattern.search(content)
                f1 = f1_pattern.search(content)

                # Prepare the row with extracted data
                row = [
                    filename,
                    float(training_time.group(1)) if training_time else None,
                    int(rules.group(1)) if rules else None,
                    float(accuracy.group(1)) if accuracy else None,
                    float(precision.group(1)) if precision else None,
                    float(recall.group(1)) if recall else None,
                    float(fpr.group(1)) if fpr else None,
                    float(f1.group(1)) if f1 else None
                ]

                # Write the row to the CSV file
                csvwriter.writerow(row)


# Example usage
filenames = ['results_data/flights_set_AQ_summary_20240606135840.txt',
             'results_data/flights_set_AQ_summary_20240606135852.txt',
             'results_data/flights_set_AQ_summary_20240606135911.txt',
             'results_data/flights_set_AQ_summary_20240606135940.txt',
             'results_data/flights_set_AQ_summary_20240606140018.txt',
             'results_data/flights_set_AQ_summary_20240606140109.txt'
             ]
output_csv = 'results_data/metrics_summary.csv'
extract_and_save_metrics(filenames, output_csv)
