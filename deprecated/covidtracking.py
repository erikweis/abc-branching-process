import requests
import json
import matplotlib.pyplot as plt

url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'

out = requests.get(url).json()

print(json.dumps(out['data'][100],indent=2))

data = out['data'][::-1]

cumulative_cases = [d['cases']['total'] for d in data]
new_cases = [cumulative_cases[i+1]-cumulative_cases[i] for i in range(len(cumulative_cases)-1)]
plt.plot(new_cases)
plt.show()