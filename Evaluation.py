import csv
import os
import Orange.data.table
import numpy
from sklearn.model_selection import train_test_split
from tabulate import tabulate
import statistics
import os
import datetime

from AQ import AQ
from CN2 import CN2


def print_confusion_matrix(confusion_matrix, all_classes):
    headers = ["confusion matrix"] + list(all_classes)
    table = [[all_classes[i]] + row for i, row in enumerate(confusion_matrix)]
    print(tabulate(table, headers, tablefmt="latex"))


def accuracy(confusion_matrix):
    correct = 0
    all = 0
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            all += confusion_matrix[i][j]
            if i == j:
                correct += confusion_matrix[i][j]
    return [round(correct/all, 2)]*len(confusion_matrix[0]), correct/all

def precision(confusion_matrix):
    precisions = []
    for i in range(len(confusion_matrix)):
        tp = confusion_matrix[i][i]
        ftp = sum([confusion_matrix[i][j] for j in range(len(confusion_matrix))])
        if ftp == 0:
            precisions.append(0)
        else:
            precisions.append(tp/(ftp))
    return numpy.round(precisions, 2), statistics.mean(precisions)

def recall(confusion_matrix):
    recall = []
    for i in range(len(confusion_matrix)):
        tp = confusion_matrix[i][i]
        tpfn = sum([confusion_matrix[j][i] for j in range(len(confusion_matrix))])
        if tpfn == 0:
            recall.append(0)
        else:
            recall.append(tp/(tpfn))
    return numpy.round(recall, 2), statistics.mean(recall)

def f1_score(precision, recall):
    f1 = []
    for i in range(len(precision)):
        if precision[i] + recall[i] == 0:
            f1.append(0)
        else:
            f1.append(2*precision[i]*recall[i]/(precision[i]+recall[i]))
    return numpy.round(f1, 2), statistics.mean(f1)

def false_positive_rate(confusion_matrix):
    fpr = []
    for i in range(len(confusion_matrix)):
        fp = sum([confusion_matrix[j][i] for j in range(len(confusion_matrix))]) - confusion_matrix[i][i]
        tnfp = fp + sum([confusion_matrix[j][k] for j in range(len(confusion_matrix)) for k in range(len(confusion_matrix[j])) if j != i and k != i])
        if tnfp == 0:
            fpr.append(0)
        else:
            fpr.append(fp/(tnfp))
    return numpy.round(fpr, 2), statistics.mean(fpr)

def ensure_results_folder():
    if not os.path.exists('results_data'):
        os.makedirs('results_data')

def print_summary(all_classes, confusion_matrix_aq=None, aq=None, confusion_matrix_cn2=None, cn2=None, output_file=None):
    from io import StringIO
    import sys

    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result

    if confusion_matrix_aq:
        print("------------------------ AQ ------------------------")
        print(f"Training time: {round(aq.training_time, 2)} seconds")
        print(f"Scorings: {aq.scoring1} > {aq.scoring2} > {aq.scoring3}")
        print("rules: ", len(aq.rules))
        print_confusion_matrix(confusion_matrix_aq, all_classes)

        accuracy_arr, accuracy_val = accuracy(confusion_matrix_aq)
        precision_arr, precision_val = precision(confusion_matrix_aq)
        recall_arr, recall_val = recall(confusion_matrix_aq)
        fpr_arr, fpr_val = false_positive_rate(confusion_matrix_aq)
        f1_arr, f1_val = f1_score(precision_arr, recall_arr)
        print('\n')
        headers = ["Class", "Accuracy", "Precision", "Recall", "False Positive Rate", "F1 score"]

        table = [[all_classes[i], accuracy_arr[i], precision_arr[i], recall_arr[i], fpr_arr[i], f1_arr[i]] for i in range(len(all_classes))]
        print(tabulate(table, headers, tablefmt="latex"))
        print("Macro average:")
        print("Accuracy: {:.2f}%".format(accuracy_val*100))
        print("Precision: {:.2f}%".format(precision_val*100))
        print("Recall / True Positive Rate: {:.2f}%".format(recall_val*100))
        print("False Positive Rate: {:.2f}%".format(fpr_val*100))
        print("F1 Score: {:.2f}%".format(f1_val*100))
        print('\n')

    if confusion_matrix_cn2:
        print("------------------------ CN2 ------------------------")
        print(f"Training time: {round(cn2.training_time, 2)} seconds")
        print("rules: ", len(cn2.classifier.rule_list))
        print_confusion_matrix(confusion_matrix_cn2, all_classes)

        accuracy_arr, accuracy_val = accuracy(confusion_matrix_cn2)
        precision_arr, precision_val = precision(confusion_matrix_cn2)
        recall_arr, recall_val = recall(confusion_matrix_cn2)
        fpr_arr, fpr_val = false_positive_rate(confusion_matrix_cn2)
        f1_arr, f1_val = f1_score(precision_arr, recall_arr)
        print('\n')
        headers = ["Class", "Accuracy", "Precision", "Recall", "False Positive Rate", "F1 score"]
        table = [[all_classes[i], accuracy_arr[i], precision_arr[i], recall_arr[i], fpr_arr[i], f1_arr[i]] for i in range(len(all_classes))]
        print(tabulate(table, headers, tablefmt="latex"))
        print("Macro average:")
        print("Accuracy: {:.2f}%".format(accuracy_val*100))
        print("Precision: {:.2f}%".format(precision_val*100))
        print("Recall / True Positive Rate: {:.2f}%".format(recall_val*100))
        print("False Positive Rate: {:.2f}%".format(fpr_val*100))
        print("F1 Score: {:.2f}%".format(f1_val*100))

    sys.stdout = old_stdout
    result_string = result.getvalue()

    if output_file:
        with open(output_file, 'w') as f:
            f.write(result_string)
    else:
        print(result_string)


def test_and_eval(test_data, aq=None, cn2=None):
    ensure_results_folder()
    dataset_name = os.path.splitext(os.path.basename(test_data))[0]
    output_file = os.path.join('results_data', f"{dataset_name}_evaluation_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    testing_examples_aq = []
    with open(test_data, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader) #header
        next(reader) #fields type
        next(reader) #metadata

        testing_examples_aq = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader]
    testing_examples_cn2 = Orange.data.Table(test_data)

    all_classes = testing_examples_cn2.domain.class_var.values

    confusion_matrix_aq = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]
    confusion_matrix_cn2 = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]

    for test_example_aq, test_example_cn2 in zip(testing_examples_aq, testing_examples_cn2):
        if aq:
            confusion_matrix_aq[all_classes.index(test_example_aq.target)][all_classes.index(aq.predict_target(test_example_aq))] += 1
        if cn2:
            confusion_matrix_cn2[all_classes.index(test_example_cn2.get_class())][all_classes.index(cn2.predict_target(test_example_cn2))] += 1

    if aq and cn2:
        print_summary(all_classes, confusion_matrix_aq, aq, confusion_matrix_cn2, cn2)
        return

    if aq:
        print_summary(all_classes, confusion_matrix_aq, aq)
        return

    if cn2:
        print_summary(all_classes, confusion_matrix_cn2 = confusion_matrix_cn2, cn2 = cn2)
        return
    print_summary(all_classes, confusion_matrix_aq, aq, confusion_matrix_cn2, cn2, output_file=output_file)

    #OX - predicted, OY - actual




def nCV_AQ_CN2_summary(data, n, complex_cut=1):
    ensure_results_folder
    dataset_name = os.path.splitext(os.path.basename(data))[0]
    output_file = os.path.join('results_data', f"{dataset_name}_summary_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")



    with open(data, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        fields_type = next(reader)
        metadata = next(reader)
        examples_data = list(reader)

    all_classes = Orange.data.Table(data).domain.class_var.values
    

    confusion_matrix_aq = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]
    confusion_matrix_cn2 = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]

    for i in range(n):
        print(f"{i+1}/{n} cross validation...")

        train_data, val_data = train_test_split(examples_data, test_size=0.2, random_state=i)

        with open('temp/train_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(fields_type)
            writer.writerow(metadata)
            writer.writerows(train_data)

        with open('temp/val_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(fields_type)
            writer.writerow(metadata)
            writer.writerows(val_data)

        aq = AQ('temp/train_data.csv', complex_cut)
        cn2 = CN2('temp/train_data.csv', complex_cut)

        aq.train()
        cn2.train()


        testing_examples_aq = []
        with open('temp/val_data.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader) #header
            next(reader) #fields type
            next(reader) #metadata

            testing_examples_aq = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader]
        testing_examples_cn2 = Orange.data.Table('temp/val_data.csv')

        for test_example_aq, test_example_cn2 in zip(testing_examples_aq, testing_examples_cn2):
            confusion_matrix_aq[all_classes.index(test_example_aq.target)][all_classes.index(aq.predict_target(test_example_aq))] += 1
            confusion_matrix_cn2[all_classes.index(test_example_cn2.get_class())][all_classes.index(cn2.predict_target(test_example_cn2))] += 1

        os.remove(f'temp/train_data.csv')
        os.remove(f'temp/val_data.csv')

    print_summary(all_classes, confusion_matrix_aq, aq, confusion_matrix_cn2, cn2, output_file=output_file)
    #OX - predicted, OY - actual

def nCV_AQ_summary(data, n, complex_cut=1):
    ensure_results_folder()
    dataset_name = os.path.splitext(os.path.basename(data))[0]
    output_file = os.path.join('results_data', f"{dataset_name}_AQ_summary_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    with open(data, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        fields_type = next(reader)
        metadata = next(reader)
        examples_data = list(reader)

    all_classes = Orange.data.Table(data).domain.class_var.values

    confusion_matrix_aq = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]

    for i in range(n):
        print(f"{i+1}/{n} cross validation...")

        train_data, val_data = train_test_split(examples_data, test_size=0.2, random_state=i)

        with open('temp/train_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(fields_type)
            writer.writerow(metadata)
            writer.writerows(train_data)

        with open('temp/val_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(fields_type)
            writer.writerow(metadata)
            writer.writerows(val_data)

        aq = AQ('temp/train_data.csv', complex_cut)

        aq.train()

        testing_examples_aq = []
        with open('temp/val_data.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader) #header
            next(reader) #fields type
            next(reader) #metadata

            testing_examples_aq = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader]

        for test_example_aq in testing_examples_aq:
            confusion_matrix_aq[all_classes.index(test_example_aq.target)][all_classes.index(aq.predict_target(test_example_aq))] += 1

        os.remove(f'temp/train_data.csv')
        os.remove(f'temp/val_data.csv')

    print_summary(all_classes, confusion_matrix_aq, aq, output_file=output_file)
