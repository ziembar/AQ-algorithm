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
            self.score = 0



    def __init__(self, training_examples, complex_cut) -> None:
        self.rules = []
        self.not_covered_training_examples = training_examples
        self.complex_cut = complex_cut

        # TODO: replace with manual input of range of valid values
        attributes = [[] for _ in range(len(training_examples[0].attributes))]
        for example in training_examples:
            for i in range(len(example.attributes)):
                if example.attributes[i] not in attributes[i]:
                    attributes[i].append(example.attributes[i])
        self.general_complex = self.Complex(attributes)


    def train(self):
        while(len(self.not_covered_training_examples) > 0):
            rule = self.learn_rule()
            self.rules.append(rule)
            for example in self.not_covered_training_examples: 
                # TODO: if its working, omit examples with target != rule.target
                if self.complex_covers(rule.complex, example):
                    self.not_covered_training_examples.remove(example)
            


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



    def learn_rule(self):
        star = [self.general_complex]
        xs = self.not_covered_training_examples[0]
        covered_negative_examples = []
        for x in self.not_covered_training_examples:
            if x.target != xs.target:
                covered_negative_examples.append(x)

        while(len(covered_negative_examples) > 0):
            xn = covered_negative_examples[0]
            star = self.partial_star(star, xn, xs)
            star = self.generalize_star(star)
            covered_negative_examples_cpy = covered_negative_examples.copy()


            star = self.select_best_complex(self.complex_cut, star, covered_negative_examples)

            for complex in star:
                for example in covered_negative_examples:
                    if not self.complex_covers(complex, example):
                        covered_negative_examples_cpy.remove(example)
            covered_negative_examples = covered_negative_examples_cpy
            
        self.select_best_complex(1, star, None)
        rule = self.Rule(*star, xs.target)
        return rule
            

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
                for i in range(len(complex1.attributes)):
                    if complex1.attributes[i] in complex2.attributes[i] and complex1.attributes[i] != complex2.attributes[i]:
                        star_cpy.remove(mapping[complex2])
        
        return star_cpy


    def select_best_complex(self, complex_cut, star, covered_negative_examples):
        # if(covered_negative_examples != None):
        #     for complex in star:
        #         for example in covered_negative_examples:
        #             if not self.complex_covers(complex, example):
        #                 complex.score += 1
        # star.sort(key=lambda complex: complex.score, reverse=True)
        # TODO implement tie breaker
        star = star[:complex_cut]
           
        return star
        

if __name__ == "__main__":
    training_examples = []
    telen = 0
    with open('datasets/beauty_mod.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) #header
        training_examples = [AQ.Example(list(map(int, row)), int(row[-1])) for row in reader]
        telen = len(training_examples)


    aq = AQ(training_examples, 1)
    aq.train()
    for rule in aq.rules:
        print( rule.complex.attributes, "---" , rule.target)

    print(len(aq.rules), "rules")
    print(telen, "training examples")

