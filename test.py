# from urllib.request import urlopen
# import json
import numpy as np

# import plotly.express as px
# from meta_submitter_all_python import STATES


# s = STATES
# #s.remove('DC')
# fig = px.choropleth(locations=s, locationmode="USA-states", color=np.random.randint(0,100,size=len(s)), color_continuous_scale='Viridis', scope="usa")
# fig.show()

import matplotlib.pyplot as plt
from scipy.stats import binom

#x = np.linspace(0,1,100)
#y = scipy.stats.binom.pmf(60,100,0.2)
#plt.plot(x,y)
n=100
p=0.7

k = np.arange(1, 99)
print(binom.pmf(k, n, p))
plt.plot(k, binom.pmf(k, n, p), 'bo', ms=8, label='binom pmf')
plt.vlines(k, 0, binom.pmf(k, n, p), colors='b', lw=5, alpha=0.5)
plt.xlabel('k')
plt.ylabel('P(k)')
plt.annotate('p=0.3',(90,0.7))
plt.show()
