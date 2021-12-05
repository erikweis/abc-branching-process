import scipy.stats
import numpy as np
import requests
from datetime import datetime
import pandas as pd
import os
import sys
import argparse
from typing import Iterable
import math

import logging
import timeit

def neg_binom_pull(r0, k):
    
    
    probs = []
    
    for i in range(10):
                
        probs.append((math.gamma(i+k)/(math.factorial(i)*math.gamma(k)))*((r0)/(k+r0))**(i) * (k/(k + r0))**(k))
                
                
    probs = probs/np.sum(probs)
    
    return  np.random.choice(np.arange(0, 10), p=probs)

def binom_pull(r, infect_count):
    return np.random.binomial(infect_count, 1 - r)

def simulation_within_threshold(cumulative_cases_simulated, cumulative_cases_data,threshold=0.5):

    """Returns true if the simulation is within threshold and False if the simulation should stop."""

    error = np.abs(cumulative_cases_simulated - cumulative_cases_data) / cumulative_cases_data
    return error <= threshold


def simulate_branching_process(r0=3.5, k=0.5, r = 0.01, state='vt', cutoff_time = None,threshold=0.5):

    """ Simulate a branching process with {cutoff_time} steps,
    according to parameters R0 and K, drawn from prior beta
    distributions.

    Checks the simulation at several time steps to ensure it haw not strayed too far
    from an acceptable sample.

    Returns:
        R0,k,simulated_cumulative_cases[tuple]: The sampled parameters R0, k, and the cumulative cases.
        Returns -99 for simulated_cumulative_cases if the procedure failed one of the threshold checks.
    """
    start = timeit.timeit()

    cumulative_cases_data= pd.read_csv(f'data/{state}_first_peak.csv').values[:,1]

    if not cutoff_time:
        cutoff_time = len(cumulative_cases_data)

    trans_vec = np.zeros(cutoff_time)
    infect_vec = np.zeros(cutoff_time)

    # Check the values here for the ABC
    checkpoints = np.arange(10,cutoff_time)

    infect_vec[0] = 1
    for i in range(1, cutoff_time):

        temp = 0
        for j in range(int(infect_vec[i-1])):
            temp = temp + neg_binom_pull(r0, k)

        trans_vec[i] = temp
        infect_vec[i] = trans_vec[i] + binom_pull(r, infect_vec[i - 1])        

        if i in checkpoints:
            if not simulation_within_threshold(np.sum(trans_vec), cumulative_cases_data[i],threshold):
                return f"Failure at {i}"
        elif i<min(checkpoints) and np.sum(trans_vec)>max(cumulative_cases_data)/2:
            #double check the branching process isn't going crazy right away
            return f"Failuer at {i}"

    #calculate cumulative_cases
    cumulative_cases_simulated = [int(np.sum(trans_vec[0:i]) + 1) for i in range(1,cutoff_time)] #add 1 for initial case

    end = timeit.timeit()
    logging.info(end-start)

    return cumulative_cases_simulated        


def save_data(output,filepath):

    if isinstance(output,str):
        with open(filepath,'w') as f: 
            f.write(output)
    else:
        df = pd.DataFrame(output,columns = ['cumulative_cases_simulated'])
        df.to_csv(filepath)

def main(args):

    if not args.f:
        print("No file name called")
        sys.exit(1)

    cutoff_time = None if args.cutoff < 0 else args.cutoff
    output = simulate_branching_process(
        r0 = args.r0,
        k = args.k,
        r = args.r,
        cutoff_time = cutoff_time,
        state = args.state,
        threshold = args.error
    )

    save_data(output,args.f)


if __name__ == "__main__":

    # setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',type=str,help='filename to save the output')
    parser.add_argument('-r0',type=float,default = 3.5, help='expected secondary infections parameter for negative binomial distribution')
    parser.add_argument('-k',type= float,default = 0.5, help='dispersion parameter for negative binomial')
    parser.add_argument('-r',type=float,default = 0.01, help='carry-over infections proportion at each time step')
    parser.add_argument('--cutoff',default = -1, type=int,help='stop simualtion after N steps')
    parser.add_argument('--state',default='vt')
    parser.add_argument('--error',default=0.5,help='the maximum error for simulation when checking against real data')

    args = parser.parse_args()

    main(args)

