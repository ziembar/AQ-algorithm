import copy
import csv

class AQ:

    class Example:
        def __init__(self, attributes, target) -> None:
            self.attributes = attributes
            self.target = target # class


    class Rule:
        def __init__(self, complex, target) -> None:
            self.complex = complex
            self.target = target

    class Complex:
        def __init__(self, attributes) -> None:
            self.attributes = attributes
            self.score1 = 0
            self.score2 = 0




    def __init__(self, training_examples, complex_cut, binary=False, target=None) -> None:
        self.rules = []
        self.not_covered_training_examples = training_examples
        self.complex_cut = complex_cut
        self.binary = binary

        if binary:
            if target != None:
                self.seed_target = target
            else:
                self.seed_target = training_examples[0].target
            for example in training_examples:
                if example.target != target:
                    self.seed_anti_target = example.target
                    break

        # TODO: replace with manual input of range of valid values??
        attributes = [[] for _ in range(len(training_examples[0].attributes))]
        for example in training_examples:
            for i in range(len(example.attributes)):
                if example.attributes[i] not in attributes[i]:
                    attributes[i].append(example.attributes[i])
        self.general_complex = self.Complex(attributes)


    def train(self):
        while(len(self.not_covered_training_examples) > 0):
            print("calculating", len(self.rules) + 1, "rule,", len(self.not_covered_training_examples), "examples left to cover")
            rule = self.learn_rule()
            if rule == None:
                break
            self.rules.append(rule)
            for example in self.not_covered_training_examples: 
                if self.complex_covers(rule.complex, example):
                    self.not_covered_training_examples.remove(example)
            

    def learn_rule(self):
        star = [self.general_complex]

        xs = None
        if self.binary:
            for example in self.not_covered_training_examples:
                if example.target == self.seed_target:
                    xs = example
                    break
            if xs == None:
                return None
        else:
            xs = self.not_covered_training_examples[0]

        all_negative_examples = []
        for x in self.not_covered_training_examples:
            if x.target != xs.target:
                all_negative_examples.append(x)

        
        flag = False
        while(not flag):
            xn_iter = iter(all_negative_examples)
            xn_correct = False
            no_more_n_seed = False

            while(not xn_correct):
                xn = next(xn_iter, None)
                if xn is None: 
                    no_more_n_seed = True
                    break
                if all(not self.complex_covers(complex, xn) for complex in star):
                    continue  # skip this xn because it's not covered by any complex in star
                elif xn_correct is not None:
                    xn_correct = True
            if no_more_n_seed:
                break

            if xn.attributes == xs.attributes:
                all_negative_examples.pop(0)
                continue #skip wrong example

            star = self.partial_star(star, xn, xs)
            star = self.generalize_star(star)

            star = self.select_best_complex(self.complex_cut, star, all_negative_examples)

            flag = True
            for complex in star:
                for example in all_negative_examples:
                    if self.complex_covers(complex, example):
                        flag = False
                        break
                if not flag:
                    break
            
        star = self.select_best_complex(1, star, all_negative_examples)
        
        rule = self.Rule(*star, xs.target)
        return rule
    
    def partial_star(self, star, xn, xs):
        star_cpy = []
        for complex in star:
            if self.complex_covers(complex, xn):
                for i in range(len(complex.attributes)):
                    if xn.attributes[i] in complex.attributes[i] and xn.attributes[i] != xs.attributes[i]:
                        complex_cpy = copy.deepcopy(complex)
                        complex_cpy.attributes[i].remove(xn.attributes[i])
                        star_cpy.append(complex_cpy)
                    else:
                        continue
            else:
                star_cpy.append(complex)
        return star_cpy

            

    def complex_covers(self, complex, example):
        for i in range(len(complex.attributes)):
            if example.attributes[i] in complex.attributes[i]:
                continue
            else:
                return False
        return True
    
    def generalize_star(self, star):
        mapping = {complex: copy.deepcopy(complex) for complex in star}
        star_cpy = list(mapping.values())
        
        for complex1 in star:
            for complex2 in star:
                if complex1 == complex2:
                    continue
                if all(all(x in attr1 for x in attr2) for attr1, attr2 in zip(complex1.attributes, complex2.attributes)):
                    if mapping[complex2] in star_cpy:
                        star_cpy.remove(mapping[complex2])
        
        return star_cpy


    def select_best_complex(self, complex_cut, star, covered_negative_examples):
        if(covered_negative_examples != None):
            for complex in star:
                for example in covered_negative_examples:
                    if not self.complex_covers(complex, example):
                        complex.score1 += 1
                complex.score2 = self.second_score(complex)
        star.sort(key=lambda complex: (complex.score1, complex.score2), reverse=True)
        star = star[:complex_cut]
        for complex in star:
            complex.score1 = 0
            complex.score2 = 0
        return star
    
    def second_score(self, complex):
        for i in range(len(complex.attributes)):
            complex.score2 += len(complex.attributes[i])

    

    def predict_target(self, example):
        for rule in self.rules:
            if self.complex_covers(rule.complex, example):
                return rule.target
        if self.binary:
            return self.seed_anti_target
        

if __name__ == "__main__":
    training_examples = []
    telen = 0
    with open('datasets/flights_test.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) #header
        training_examples = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader]
        telen = len(training_examples)

    aq = AQ(training_examples, 2)
    aq.train()

    # for rule in aq.rules:
    #     print( rule.complex.attributes, "---" , rule.target, '\n')

    # print(len(aq.rules), "rules")
    # print(telen, "training examples")



    testing_examples = []

    with open('datasets/flights_test2.csv', 'r') as file2:
        reader2 = csv.reader(file2, delimiter=';')
        next(reader2) #header
        testing_examples = [AQ.Example(list(map(str, row[:-1])), str(row[-1])) for row in reader2]

    correct = 0
    all = len(testing_examples)
    for test_example in testing_examples:
        if aq.predict_target(test_example) == test_example.target:
            correct += 1
    print(correct, "out of", all, "correct", round(correct/all*100, 2), "%")



