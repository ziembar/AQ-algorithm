from AQ import AQ
from CN2 import CN2
from Evaluation import test_and_eval



# test 1
# aq = AQ('datasets/flights_test2.csv', 2)
# cn2 = CN2('datasets/flights_test2.csv', 2)
# aq.train()
# cn2.train()
# test_and_eval(aq, cn2, 'datasets/flights_test2.csv')

#test 2 
aq = AQ('datasets/beautyyyy.csv', 3)
cn2 = CN2('datasets/beautyyyy.csv', 3)
aq.train()
cn2.train()
test_and_eval(aq, cn2, 'datasets/beauty_mod_test.csv')