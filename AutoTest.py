from Evaluation import nCV_AQ_CN2_summary, nCV_AQ_summary


nCV_AQ_CN2_summary("datasets/ds_salaries_clean.csv",n=1,complex_cut=1)
nCV_AQ_summary("datasets/ds_salaries_clean.csv",n=1,complex_cut=3)