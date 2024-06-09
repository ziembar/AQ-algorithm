from AQ import AQ
from CN2 import CN2
from Evaluation import nCV_AQ_CN2_summary, nCV_AQ_summary, test_and_eval



# example test 1
aq = AQ('datasets/flights_test.csv', 1)
cn2 = CN2('datasets/flights_test.csv', 1)
aq.train()
cn2.train()
test_and_eval('datasets/flights_set.csv', aq, cn2)

# example test 2 
aq = AQ('datasets/beauty_set.csv', 2)
# cn2 = CN2('datasets/beauty_set.csv', 2)
aq.train()
# cn2.train()
test_and_eval('datasets/beauty_mod_test.csv', aq)

# example test 3
nCV_AQ_CN2_summary(data='datasets/flights_set.csv', n=1, complex_cut=1)


# example test 4
aq = AQ('datasets/test_data.csv', 1, scoring1='fast')
aq.train()
for rule in aq.rules:
    print(rule.complex.attributes, ' -> ', rule.target)


# example test 5
test_and_eval('datasets/test_data.csv', aq)

# example test 6
nCV_AQ_CN2_summary("datasets/test_data.csv",n=3,complex_cut=2)
