from AQ import AQ
from CN2 import CN2
from Evaluation import nCV_AQ_CN2_summary, test_and_eval



# test 1
# aq = AQ('datasets/flights_test.csv', 1)
# cn2 = CN2('datasets/flights_test.csv', 1)
# aq.train()
# cn2.train()
# test_and_eval('datasets/flights_set.csv', aq, cn2)

#test 2 
# aq = AQ('datasets/beauty_set.csv', 2)
# cn2 = CN2('datasets/beauty_set.csv', 2)
# aq.train()
# cn2.train()
# test_and_eval('datasets/beauty_mod_test.csv', aq, cn2)

#test 3
nCV_AQ_CN2_summary(data='datasets/flights_set.csv', n=4, complex_cut=7)


# complex_cut -- ile kompleksow przechodzi dalej
# scoring1, scoring2, scoring3 -- jakie scoringi
# binary -- czy binarny czy nie

