import scipy.stats
import numpy as np
import requests
from datetime import datetime
import pandas as pd
import os
import sys

def neg_binom_pull(r0, k):
    p = r0 / (r0 + k)
    n = 1/k
    return scipy.stats.nbinom.rvs(n, p)

def binom_pull(r, infect_count):
    return np.random.binomial(infect_count, 1 - r)

def simulation_within_threshold(cumulative_cases_simulated, cumulative_cases_data):

    """Returns true if the simulation is within threshold and False if the simulation should stop."""

    error = np.abs(cumulative_cases_simulated - cumulative_cases_data) / cumulative_cases_data
    return error <= 1


def simulate_branching_process(r0, k, state, cutoff_time = None):

    """ Simulate a branching process with {cutoff_time} steps,
    according to parameters R0 and K, drawn from prior beta
    distributions.

    Checks the simulation at several time steps to ensure it haw not strayed too far
    from an acceptable sample.

    Returns:
        R0,k,simulated_cumulative_cases[tuple]: The sampled parameters R0, k, and the cumulative cases.
        Returns -99 for simulated_cumulative_cases if the procedure failed one of the threshold checks.
    """

    cumulative_cases_data= pd.read_csv(f'data/{state}_first_peak.csv').values[:,1]

    if not cutoff_time:
        cutoff_time = len(cumulative_cases_data)

    trans_vec = np.zeros(cutoff_time)
    infect_vec = np.zeros(cutoff_time)

    infect_vec[0] = 1
    for i in range(1, cutoff_time):

        temp = 0
        for j in range(int(infect_vec[i-1])):
            temp = temp + neg_binom_pull(r0, k)

        trans_vec[i] = temp
        infect_vec[i] = trans_vec[i] + binom_pull(r, infect_vec[i - 1])

        # Check the values here for the ABC
        checkpoints = [15, 30, 45, 60, 75, 90]

        if i == 45:
            print("Halfway")
        if i in checkpoints:
            if not simulation_within_threshold(np.sum(trans_vec), cumulative_cases_data[i]):
                return f"Failure at {i}"


    #calculate cumulative_cases
    cumulative_cases_simulated = [int(np.sum(trans_vec[0:i]) + 1) for i in range(1,cutoff_time)] #add 1 for initial case
    return cumulative_cases_simulated        
        

if __name__ == "__main__":

    print(len(sys.argv))

    if not 6<= len(sys.argv)<=7:
        print("USAGE %s : <output_dir> <R0> <k> <r> [cutoff_time]")
        sys.exit(1)

    output_dir = sys.argv[1]
    state = sys.argv[2]
    R0 = float(sys.argv[3])
    k = float(sys.argv[4])
    r = float(sys.argv[5])

    if len(sys.argv)>6:
        cutoff_time = int(sys.argv[6])
    else:
        cutoff_time = None
    
    output = simulate_branching_process(R0,k,state,cutoff_time)
    print(output)

    


    # url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'
    # out = requests.get(url).json()
    # data = out['data'][::-1]
    # cutoff_time = 20
    # cumulative_cases_data = [d['cases']['total'] for d in data[:cutoff_time]]


    

    # sampR0, sampK, cumulative_cases_simulated  = simulate_branching_process(cumulative_cases_data, T, 1, 4, .1, .5)

    # print("k:",sampK)
    # print("R0:", sampR0)
    # print(cumulative_cases_simulated)


