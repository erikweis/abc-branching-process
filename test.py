# 

# import pandas as pd

# df = pd.read_csv('simulations/12-07_22-41-17/trials.csv')
# print(df.head())
# print(df['trial_success'].sum())

from scipy.stats import truncnorm
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1,10,100)

mean, std = 3, 1
min_val, max_val = 0,10
a,b = (min_val - mean)/std , (max_val - mean)/std
tn = truncnorm(a,b,scale=std,loc=mean).pdf(x)

plt.plot(x,tn)
plt.show()
