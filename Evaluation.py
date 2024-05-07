import csv
import Orange.data.table


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



    for test_example_aq, test_example_cn2 in zip(testing_examples_aq, testing_examples_cn2):
        if AQ.predict_target(test_example_aq) == test_example_aq.target:
            aq_correct += 1
        if CN2.predict_target(test_example_cn2) == test_example_cn2.get_class():
            cn2_correct += 1
    print("AQ: ",aq_correct, "out of", all, "correct", round(aq_correct/all*100, 2), "%")
    print("CN2: ",cn2_correct, "out of", all, "correct", round(cn2_correct/all*100, 2), "%")
    print("AQ: ",len(AQ.rules), "rules")
    print("CN2: ",len(CN2.classifier.rule_list), "rules")