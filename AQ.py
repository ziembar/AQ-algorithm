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
        self.not_covered_training_examples = training_examples #typeof Example
        self.complex_cut = complex_cut

    def train(self):
        while(len(self.not_covered_training_examples) > 0):
            rule = self.learn_rule()
            self.rules.append(rule)
            for example in self.not_covered_training_examples: 
                # TODO: if its working, omit examples with target != rule.target
                if self.complex_covers(rule.complex, example):
                    self.not_covered_training_examples.remove(example)
            


    def partial_star(self, star, xn, xs):
        star_cpy = star.copy()
        for complex in star:
            if self.complex_covers(complex, xn):
                star_cpy.remove(complex)
                for i in range(len(complex)):
                    if xn[i] in complex[i] and xn[i] != xs[i]:
                        complex_cpy = complex.copy()
                        complex_cpy[i].remove(xn[i])
                        star_cpy.append(complex_cpy)
                    else:
                        continue
        return star_cpy



    def learn_rule(self):
        star = []
        xs = self.not_covered_training_examples[0]
        covered_negative_examples = []
        for x in self.not_covered_training_examples:
            if x.target != xs.target:
                covered_negative_examples.append(x)

        while(len(covered_negative_examples) > 0):
            xn = covered_negative_examples[0]
            star = self.partial_star(star, xn, xs)
            star = self.generalize_star(star, xn, xs)
            covered_negative_examples_cpy = covered_negative_examples.copy()


            star = self.select_best_complex(self, self.complex_cut, star, covered_negative_examples)

            for complex in star:
                for example in covered_negative_examples:
                    if not self.complex_covers(complex, example):
                        covered_negative_examples_cpy.remove(example)
            covered_negative_examples = covered_negative_examples_cpy
            
        self.select_best_complex(self, 1, star, None)
        rule = self.Rule(*star, xs.target)
        return rule
            

    def complex_covers(self, complex, example):
        for i in range(len(complex)):
            if example[i] in complex[i]:
                continue
            else:
                return False
        return True
    
    def generalize_star(self, star):
        star_cpy = star.copy()
        for complex1 in star:
            for complex2 in star:
                for i in range(len(complex1)):
                    if(all(x in complex1[i] for x in complex2[i])):
                        star_cpy.remove(complex2)


    def select_best_complex(self, complex_cut, star, covered_negative_examples):
        for complex in star:
            for example in covered_negative_examples:
                if not self.complex_covers(complex, example):
                    complex.score += 1
        star.sort(key=lambda complex: complex.score, reverse=True)
        # TODO implement tie breaker
        star = star[:complex_cut]


           
        return star
        