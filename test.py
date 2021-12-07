from urllib.request import urlopen
import json
import numpy as np

import plotly.express as px
from meta_submitter_all_python import STATES


s = STATES
#s.remove('DC')
fig = px.choropleth(locations=s, locationmode="USA-states", color=np.random.randint(0,100,size=len(s)), color_continuous_scale='Viridis', scope="usa")
fig.show()