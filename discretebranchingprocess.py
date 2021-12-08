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

def neg_binom_pull(r0, k):
    
    probs = []
    for i in range(10):    
        probs.append((math.gamma(i+k)/(math.factorial(i)*math.gamma(k)))*((r0)/(k+r0))**(i) * (k/(k + r0))**(k))
                
    probs = probs/np.sum(probs)
    
    return  np.random.choice(np.arange(0, 10), p=probs)


def binom_pull(r, infect_count):
    return np.random.binomial(infect_count, 1 - r)


def non_parametric_pull(ps):
    np.random.choice(np.arange(0,10),p=ps)


def simulation_within_threshold(cumulative_cases_simulated, cumulative_cases_data,threshold=0.5):

    """Returns true if the simulation is within threshold and False if the simulation should stop."""

    error = np.abs(cumulative_cases_simulated - cumulative_cases_data) / cumulative_cases_data
    return error <= threshold


def simulate_branching_process(r0=None, k=None, r = 0, ps = None, state='vt',threshold=0):

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

    cutoff_time = len(cumulative_cases_data)

    trans_vec = np.zeros(cutoff_time)
    infect_vec = np.zeros(cutoff_time)

    # Check the values here for the ABC
    checkpoints = np.arange(10,cutoff_time)

    infect_vec[0] = 1
    for i in range(1, cutoff_time):

        temp = 0
        for j in range(int(infect_vec[i-1])):

            if ps:
                temp += non_parametric_pull(ps)
            elif (r0 is not None) and (k is not None):
                temp += neg_binom_pull(r0, k)

        trans_vec[i] = temp
        infect_vec[i] = trans_vec[i] + binom_pull(r, infect_vec[i - 1])        

        if i in checkpoints:
            if not simulation_within_threshold(np.sum(trans_vec), cumulative_cases_data[i],threshold):
                #print(f"failure at time {i}", r0,k,r)
                return f"Failure at {i}"
        elif i<min(checkpoints) and np.sum(trans_vec)>max(cumulative_cases_data)/2:
            #double check the branching process isn't going crazy right away
            return f"Failure at {i}"

    #calculate cumulative_cases
    cumulative_cases_simulated = [int(np.sum(trans_vec[0:i]) + 1) for i in range(1,cutoff_time)] #add 1 for initial case

    return cumulative_cases_simulated        


def main(args):

    if not args.f:
        print("No file name called")
        sys.exit(1)

    output = simulate_branching_process(
        r0 = args.r0,
        k = args.k,
        r = args.r,
        state = args.state,
        threshold = args.error
    )


if __name__ == "__main__":
    pass
    # # setup arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-f',type=str,help='filename to save the output')
    # parser.add_argument('-r0',type=float,default = 3.5, help='expected secondary infections parameter for negative binomial distribution')
    # parser.add_argument('-k',type= float,default = 0.5, help='dispersion parameter for negative binomial')
    # parser.add_argument('-r',type=float,default = 0.01, help='carry-over infections proportion at each time step')
    # parser.add_argument('--cutoff',default = -1, type=int,help='stop simualtion after N steps')
    # parser.add_argument('--state',default='vt')
    # parser.add_argument('--error',default=0.5,help='the maximum error for simulation when checking against real data')

    # args = parser.parse_args()

    # main(args)

