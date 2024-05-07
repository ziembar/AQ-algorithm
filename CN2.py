import Orange

class CN2():

    def __init__(self, training_data, complex_cut=1):
        self.training_data = Orange.data.Table(training_data)
        self.learner = Orange.classification.CN2Learner()
        self.learner.rule_finder.search_strategy.constrain_continuous = True
        self.learner.rule_finder.search_strategy.beam_width = complex_cut
        self.classifier = None
    

    def train(self):
        self.classifier = self.learner(self.training_data)
        return self.classifier

    def predict_target(self, test_record):
        if self.classifier is None:
            raise Exception("Classifier not trained yet")
        c_values = self.training_data.domain.class_var.values
        return c_values[int(self.classifier(test_record))]