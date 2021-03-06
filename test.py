# 

# import pandas as pd

# df = pd.read_csv('simulations/12-07_22-41-17/trials.csv')
# print(df.head())
# print(df['trial_success'].sum())

from scipy.stats import truncnorm
import numpy as np
import matplotlib.pyplot as plt

# x = np.linspace(-1,10,100)

# mean, std = 3, 1
# min_val, max_val = 0,10
# a,b = (min_val - mean)/std , (max_val - mean)/std
# tn = truncnorm(a,b,scale=std,loc=mean).pdf(x)

# plt.plot(x,tn)
# plt.show()

alpha = 2.5
x_m = 1000

x = np.linspace(1000,200000,100)
y = alpha*(x_m**alpha)/np.power(x,alpha+1)
print(np.sum(y))

print(np.mean(x*y))
print(alpha*x_m/(alpha-1))