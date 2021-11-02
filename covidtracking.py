import requests
import json
import matplotlib.pyplot as plt

url = 'https://api.covidtracking.com/v2/states/vt/daily/simple.json'

out = requests.get(url).json()

print(json.dumps(out['data'][100],indent=2))

data = out['data'][::-1]

cumulative_cases = [d['cases']['total'] for d in data]
plt.plot(cumulative_cases)
plt.show()