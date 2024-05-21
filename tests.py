from AQ import AQ
from CN2 import CN2
from Evaluation import nCV_AQ_CN2_summary, test_and_eval



# test 1
# aq = AQ('datasets/flights_test.csv', 1)
# cn2 = CN2('datasets/flights_test.csv', 1)
# aq.train()
# cn2.train()
# test_and_eval('datasets/flights_test2.csv', aq, cn2)

#test 2 
aq = AQ('datasets/beautyyyy.csv', 2)
cn2 = CN2('datasets/beautyyyy.csv', 2)
aq.train()
cn2.train()
test_and_eval('datasets/beauty_mod_test.csv', aq, cn2)

#test 3
# nCV_AQ_CN2_summary(data='datasets/flights_test.csv', n=1, complex_cut=1)