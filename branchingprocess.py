from scipy.stats import nbinom, gamma
import numpy as np
from tqdm import tqdm

def single_person_infection(alpha,sigma):

    beta_ = alpha
    alpha_ = sigma

    infection_length = 21

    times = []
    while sum(times) < infection_length:
        val = gamma.rvs(alpha,scale=1/beta_)
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

    

def simulate_branching_process(r0,k,alpha,sigma):
    t = 0
    max_time = 90

    new_cases = [1]

    activation_times = [0]

    L = []

    count = 0
    for t in tqdm(np.linspace(0,max_time,100)):

        for t_act in activation_times:
            if t_act < t:
                relative_times = np.array(infection(r0,k,alpha,sigma))
                new_activation_times = relative_times + t

                activation_times += list(new_activation_times)

        removed_times = [x for x in activation_times if x<t]
        activation_times = [x for x in activation_times if x>=t]

        if len(activation_times)==0:
            break
        else:
            new_cases.append(len(removed_times))

        if count>10:
            break
        else:
            count+=1

    #print(new_cases)
    cum_cases = [sum(new_cases[:i]) for i in range(len(new_cases))]
    print(cum_cases)

if __name__ == "__main__":

    simulate_branching_process(2,0.1,0.5,0.1)


