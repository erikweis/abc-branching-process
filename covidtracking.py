import requests
import json
import matplotlib.pyplot as plt

url = 'https://api.covidtracking.com/v2/states/vt/daily/simple.json'

out = requests.get(url).json()

print(out['data'][0])

data = out['data'][::-1]

cumulative_cases = [d['cases']['total'] for d in data]
plt.plot(cumulative_cases)
plt.show()