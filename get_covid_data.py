import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks,find_peaks_cwt, argrelmin,argrelmax

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def get_state_data(abbr,save=False):

    url = f'https://api.covidtracking.com/v2/states/{abbr}/daily/simple.json'
    out = requests.get(url).json()

    data = out['data'][::-1]
    print(json.dumps(data[0],indent=2))
    cases_dicts = [d['cases'] for d in data]

    df = pd.DataFrame(cases_dicts)

    if save:
        df.to_csv(f'data/{abbr}.csv')

    return df

def add_new_cases_column(df):

    df['new_cases'] = df['total'].diff()
    df['new_cases_smoothed'] = df['new_cases'].rolling(14,min_periods = 1).mean()

    return df

def get_first_wave_data(df,state,save=False):

    vals = df['new_cases_smoothed'].values
    max_val = df['new_cases_smoothed'].max(skipna=True)
    peaks,props = find_peaks(vals,distance=40,width=15)

    first_wave = df['total'].values[:peaks[0]]
    
    #exclude zero case counts
    first_nonzero_index = 0
    while not( first_wave[first_nonzero_index] > 0 and first_wave[first_nonzero_index] != float('nan')):
        first_nonzero_index += 1
    first_wave = first_wave[first_nonzero_index:]

    if save:
        outdf = pd.DataFrame(first_wave)
        outdf.to_csv(f'data/{state}_first_peak.csv')

    return first_wave


def test_peak_detection(df,state):

    vals = df['new_cases_smoothed'].values
    max_val = df['new_cases_smoothed'].max(skipna=True)
    peaks,props = find_peaks(vals,distance=40,width=15)

    plt.plot(df['new_cases'])
    plt.plot(df['new_cases_smoothed'])
    
    #vline for peaks
    for x in peaks:
        plt.axvline(x)
    
    plt.title(state)
    plt.show()


if __name__ == "__main__":

    ##### save data ######
    # for state in states:
    #     get_state_data(state.lower(),save=True)

    #### test peak detection ######
    # for state in states:
    #     df = pd.read_csv(f'data/{state.lower()}.csv')
    #     add_new_cases_column(df)
    #     test_peak_detection(df,state)

    ###### save only first wave cumulative cases #####
    for state in states:
        state=state.lower()
        df = pd.read_csv(f'data/{state}.csv')
        df = add_new_cases_column(df)
        fw = get_first_wave_data(df,state,save=True)
        print(fw[0])

