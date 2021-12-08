# 

import pandas as pd

df = pd.read_csv('simulations/12-07_22-41-17/trials.csv')
print(df.head())
print(df['trial_success'].sum())