import scipy.stats
import numpy as np
import requests
from datetime import datetime
import pandas
import os
import json

def priors(a_R0, b_R0, a_K, b_K):
    return [scipy.stats.uniform.rvs(a_R0, b_R0), scipy.stats.uniform.rvs(a_K, b_K), scipy.stats.uniform.rvs(0,0.1)]

def binom_pull(r, infect_count):
    return np.random.binomial(infect_count, 1 - r)

def neg_binom_pull(r0, k):
    p = r0 / (r0 + k)
    n = 1/k
    return scipy.stats.nbinom.rvs(n, p)

def simulation_within_threshold(cumulative_cases_simulated, cumulative_cases_data):

    """Retursn true if the simulation is within threshold and False if the simulation should stop."""

    error = np.abs(cumulative_cases_simulated - cumulative_cases_data) / cumulative_cases_data

    return error <= 1


def simulate_branching_process(cumulative_cases_data, cutoff_time, A_R0, B_R0, A_K, B_K):

    """ Simulate a branching process with {cutoff_time} steps,
    according to parameters R0 and K, drawn from prior beta
    distributions.

    Checks the simulation at several time steps to ensure it haw not strayed too far
    from an acceptable sample.

    Returns:
        R0,k,simulated_cumulative_cases[tuple]: The sampled parameters R0, k, and the cumulative cases.
        Returns -99 for simulated_cumulative_cases if the procedure failed one of the threshold checks.
    """

    r0, k, r = priors(A_R0, B_R0, A_K, B_K)
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
            print("Count: %d" %(np.sum(trans_vec)))
            
            if not simulation_within_threshold(np.sum(trans_vec), cumulative_cases_data[i]):
                return [r0, k, None]


    #calculate cumulative_cases
    cumulative_cases_simulated = [int(np.sum(trans_vec[0:i]) + 1) for i in range(1,cutoff_time)] #add 1 for initial case
    return [r0, k, cumulative_cases_simulated]

    # print(infect_vec)
    # print(trans_vec)
    # return np.sum(trans_vec[0:T]) + 1

class Simulation:

    """Class to automatically run simulations.
    """

    def __init__(
        self,
        cumulative_cases_data,
        foldername = None,
        cutoff_time = 90,
        A_R0 = 1,
        B_R0 = 4,
        A_k = .1,
        B_k = .5,
        error = 1):

        self.A_R0 = A_R0
        self.B_R0 = B_R0
        self.A_k = A_k
        self.B_k = B_k
        self.error = error
        self.cutoff_time = cutoff_time
        self.cumulative_cases_data = cumulative_cases_data

        dirname = datetime.now().strftime("%m-%d_%H-%M-%S") if foldername is None else foldername
        self.dirpath = os.path.join('simulations',dirname)
        os.mkdir(self.dirpath)
        
        #save hyperparams
        hyperparams = {'A_R0':A_R0,'B_R0':B_R0,'A_k':A_k,'B_k':B_k}
        json_fpath = os.path.join(self.dirpath,'hyperparams.json')
        with open(json_fpath,'w') as f:
            json.dump(hyperparams,f)
        
        #create data file
        self.csv_fpath = os.path.join(self.dirpath,'trials.csv')
        with open(self.csv_fpath,'w') as f:
            f.write('R0|k|cases\n')

    def run(self,iterations=1000):
        
        self.num_rejected_samples = 0

        for i in range(iterations):
            sampR0, sampK, simulated_cases  = simulate_branching_process(
                self.cumulative_cases_data,
                self.cutoff_time,
                self.A_R0,
                self.B_R0,
                self.A_k,
                self.B_k
            )

            with open(self.csv_fpath,'a') as f:
                f.write(f"{sampR0}|{sampK}|{simulated_cases}\n")
                if not simulated_cases:
                    self.num_rejected_samples += 1

        print("number of rejected samples",self.num_rejected_samples)
        
        

if __name__ == "__main__":
    url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'
    out = requests.get(url).json()

    data = out['data'][::-1]

    cutoff_time = 20
    cumulative_cases_data = [d['cases']['total'] for d in data[:cutoff_time]]

    s = Simulation(cumulative_cases_data,cutoff_time=cutoff_time)
    s.run(iterations=100)

    

    # sampR0, sampK, cumulative_cases_simulated  = simulate_branching_process(cumulative_cases_data, T, 1, 4, .1, .5)

    # print("k:",sampK)
    # print("R0:", sampR0)
    # print(cumulative_cases_simulated)


