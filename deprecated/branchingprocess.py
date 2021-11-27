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


def poisson(alpha,sigma):

    beta_ = alpha
    alpha_ = sigma
    return gamma.rvs(alpha_,scale=1/beta_)

def simulate_branching_process(r0,k,alpha,sigma,true_data):
    t = 0
    max_time = 90

    cumulative_case_data = [(0,1)]

    next_check_time = 90

    #store infected node id, recovery time
    infected = [0]
    nodeidx2recoverytime = {0:21}

    #initial_infection
    t1 = poisson(alpha,sigma)

    total_num_nodes=1
    events = [('infection',0,t1),('recovery',0,21)]

    while len(events)>0:

        #edit data
        old_cumulative_cases = cumulative_case_data[-1][1]

        #get event
        event_type,node,time = heapq.heappop(events)

        #threshold check
        if time>next_check_time:
            print(cumulative_case_data)
            data_cases = true_data[t]
            print(data_cases)
            t, cum_cases = cumulative_case_data[-1]
            error = np.abs(cum_cases-data_cases)/data_cases
            if error > 0.9:
                print("errored out. stopped at time",t)
                return None

            next_check_time += 15
        elif time>max_time:
            return cumulative_case_data

        if event_type == 'infection':

            #new infection
            new_node_id = total_num_nodes
            total_num_nodes += 1
            recovery_time = time+21

            infected.append(new_node_id)
            nodeidx2recoverytime[new_node_id] = recovery_time
            
            heapq.heappush(events,('recovery',new_node_id,recovery_time))

            #node infects someone else, if it happens before they recover
            infection_time = time + poisson(alpha,sigma)
            if infection_time < nodeidx2recoverytime[node]:
                heapq.heappush(events,('infection',node,infection_time))            

            cumulative_case_data.append((time,old_cumulative_cases+1))


        elif event_type == 'recovery':

            infected.remove(node)


    return cumulative_case_data

if __name__ == "__main__":

    url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'
    out = requests.get(url).json()

    data = out['data'][::-1]

    cumulative_cases_data = [d['cases']['total'] for d in data[:90]]

    simulated_cases = simulate_branching_process(1,0.1,10,10,cumulative_cases_data)
    print(simulated_cases)

    # alpha = 4
    # sigma = 4

    # beta_ = alpha
    # alpha_ = sigma
    # t1 = gamma.rvs(alpha_,scale=1/beta_,size= 1000)

    # import matplotlib.pyplot as plt
    # plt.hist(t1)
    # plt.show()
    

