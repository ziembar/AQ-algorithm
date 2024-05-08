import csv
import Orange.data.table
from tabulate import tabulate


def print_confusion_matrix(confusion_matrix, all_classes):
    print("confusion matrix:")
    headers = [""] + list(all_classes)
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

def test_and_eval(AQ, CN2, test_data): 
    testing_examples_aq = []
    with open(test_data, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader) #header
        next(reader) #fields type
        next(reader) #metadata

        testing_examples_aq = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader]
    testing_examples_cn2 = Orange.data.Table(test_data)

    all = len(testing_examples_aq)
    
    aq_correct = 0
    cn2_correct = 0

    all_classes = testing_examples_cn2.domain.class_var.values

    confusion_matrix_aq = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]
    confusion_matrix_cn2 = [[0 for _ in range(len(all_classes))] for _ in range(len(all_classes))]


    for test_example_aq, test_example_cn2 in zip(testing_examples_aq, testing_examples_cn2):

        confusion_matrix_aq[all_classes.index(test_example_aq.target)][all_classes.index(AQ.predict_target(test_example_aq))] += 1
        confusion_matrix_cn2[all_classes.index(test_example_cn2.get_class())][all_classes.index(CN2.predict_target(test_example_cn2))] += 1



    print("------------ AQ ------------")
    print("rules: ", len(AQ.rules))
    print("accuracy: ",accuracy(confusion_matrix_aq), "%")

    print_confusion_matrix(confusion_matrix_aq, all_classes)
    
    print("------------ CN2 ------------")
    print("rules: ", len(CN2.classifier.rule_list))
    print("accuracy: ", accuracy(confusion_matrix_cn2), "%")

    print_confusion_matrix(confusion_matrix_cn2, all_classes)

    #OX - predicted, OY - actual


