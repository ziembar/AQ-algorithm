import csv
import Orange.data.table
from tabulate import tabulate
import statistics


def print_confusion_matrix(confusion_matrix, all_classes):
    headers = ["confusion matrix"] + list(all_classes)
    table = [[all_classes[i]] + row for i, row in enumerate(confusion_matrix)]
    print(tabulate(table, headers, tablefmt="grid"))


def accuracy(confusion_matrix):
    correct = 0
    all = 0
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            all += confusion_matrix[i][j]
            if i == j:
                correct += confusion_matrix[i][j]
    return correct/all

def precision(confusion_matrix, all_classes):
    precisions = []
    for i in range(len(confusion_matrix)):
        tp = confusion_matrix[i][i]
        ftp = sum([confusion_matrix[i][j] for j in range(len(confusion_matrix))])
        if ftp == 0:
            precisions.append(0)
        else:
            precisions.append(tp/(ftp))
    print("precision by class:")
    print(tabulate([precisions], list(all_classes), tablefmt="grid"))
    return statistics.mean(precisions)

def recall(confusion_matrix, all_classes):
    recall = []
    for i in range(len(confusion_matrix)):
        tp = confusion_matrix[i][i]
        tpfn = sum([confusion_matrix[j][i] for j in range(len(confusion_matrix))])
        if tpfn == 0:
            recall.append(0)
        else:
            recall.append(tp/(tpfn))
    print("recall by class:")
    print(tabulate([recall], list(all_classes), tablefmt="grid"))
    return statistics.mean(recall)

def test_and_eval(test_data, AQ = None, CN2 = None): 
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
        if AQ:
            confusion_matrix_aq[all_classes.index(test_example_aq.target)][all_classes.index(AQ.predict_target(test_example_aq))] += 1
        if CN2:
            confusion_matrix_cn2[all_classes.index(test_example_cn2.get_class())][all_classes.index(CN2.predict_target(test_example_cn2))] += 1


    if AQ:
        print("------------------------ AQ ------------------------")
        print("rules: ", len(AQ.rules))
        print('\n')
        print_confusion_matrix(confusion_matrix_aq, all_classes)
        print('\n')
        print("accuracy: ",round(accuracy(confusion_matrix_aq)*100, 2), "%")
        print('\n')
        precision_aq = precision(confusion_matrix_aq, all_classes)
        print("precision overall: ", round(precision_aq*100, 2), "%")
        print('\n')
        recall_aq = recall(confusion_matrix_aq, all_classes)
        print("recall overall: ", round(recall_aq*100, 2), "%")
        print('\n')
        print("F1 score: ", round((2*precision_aq*recall_aq/(recall_aq+precision_aq))*100, 2), "%")

    
    if CN2:
        print('\n')
        print("------------------------ CN2 ------------------------")
        print("rules: ", len(CN2.classifier.rule_list))
        print('\n')
        print_confusion_matrix(confusion_matrix_cn2, all_classes)
        print('\n')
        print("accuracy: ", round(accuracy(confusion_matrix_cn2)*100, 2), "%")
        precision_cn2 = precision(confusion_matrix_aq, all_classes)
        print("precision overall: ", round(precision_cn2*100, 2), "%")
        print('\n')
        recall_cn2 = recall(confusion_matrix_aq, all_classes)
        print("recall overall: ", round(recall_cn2*100, 2), "%")
        print('\n')
        print("F1 score: ", round((2*precision_cn2*recall_cn2/(recall_cn2+precision_cn2))*100, 2), "%")


    #OX - predicted, OY - actual


