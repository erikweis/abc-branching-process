from scipy.stats import nbinom, gamma
import numpy as np
from tqdm import tqdm
import requests
import json
import heapq

def single_person_infection(alpha,sigma):

    beta_ = alpha
    alpha_ = sigma

    infection_length = 21

    times = []
    while sum(times) < infection_length:
        val = gamma.rvs(alpha_,scale=1/beta_)
        times.append(val)

    relative_infection_times = [sum(times[:i+1]) for i in range(len(times))]

    return relative_infection_times


def infection(r0,k,alpha,sigma):

    n_= k
    p_= k/(r0+k)

    secondary_infection = nbinom.rvs(n_,p_,size=1)
    secondary_infection = int(secondary_infection)

    relative_times = []
    for _ in range(secondary_infection):
        relative_times += single_person_infection(alpha,sigma)

    return relative_times

def simulate_branching_process(r0,k,alpha,sigma,true_data):
    t = 0
    max_time = 90

    new_cases = [1]
    cumulative_case_data = [(0,1)]

    #times when a new person becomes infected
    activation_times = [0]

    events = []
    next_check_time = 15
    heapq.heappush(events,0)

    while len(events)>0:

        time = heapq.heappop(events)
        print(time)

        if time>next_check_time:
            data_cases = true_data[t]
            t, cum_cases = cumulative_case_data[-1]
            error = np.abs(cum_cases-data_cases)/data_cases
            if error > 0.3:
                print("errored out. stopped at time",t)
                return None

            next_check_time += 15

        relative_times = infection(r0,k,alpha,sigma)
        for dt in relative_times:
            heapq.heappush(events,time+dt)


    # for t in tqdm(np.linspace(0,max_time,100)):

    #     #check for threshold
    #     if t in [15,30,45,60,75]:
    #         data_cases = true_data[t]
    #         error = np.abs(cumulative_cases[-1]-data_cases)/data_cases
    #         if error > 0.3:
    #             print("errored out. stopped at time",t)
    #             return None

    #     for t_act in activation_times:
    #         if t_act < t:
    #             relative_times = np.array(infection(r0,k,alpha,sigma))
    #             new_activation_times = relative_times + t

    #             activation_times += list(new_activation_times)

    #     removed_times = [x for x in activation_times if x<t]
    #     activation_times = [x for x in activation_times if x>=t]

    #     if len(activation_times)==0:
    #         return cumulative_cases
    #     else:
    #         current_cumulative_cases = len(removed_times)
    #         cumulative_cases.append(cumulative_cases[-1]+current_cumulative_cases)

    return cumulative_case_data


    #print(new_cases)
    cumulative_cases = [sum(new_cases[:i]) for i in range(len(new_cases))]
    print(cumulative_cases)

if __name__ == "__main__":

    url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'
    out = requests.get(url).json()

    data = out['data'][::-1]

    cumulative_cases_data = [d['cases']['total'] for d in data[:90]]

    simulated_cases = simulate_branching_process(2,0.1,7.5,1,cumulative_cases_data)
    print(simulated_cases)
    

