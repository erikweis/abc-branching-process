from scipy.stats import nbinom, gamma
import numpy as np

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

    for t in range(max_time):

        indices_to_remove = []
        for index, t_act in enumerate(activation_times):
            if t_act == t:
                relative_times = np.array(infection(r0,k,alpha,sigma))
                new_activation_times = relative_times + t
                activation_times += list(new_activation_times)

                indices_to_remove.append(index)

        for index in indices_to_remove:
            activation_times.pop(index)

        #each index represents a new case
        new_cases.append(len(indices_to_remove))

    print(new_cases)

if __name__ == "__main__":

    simulate_branching_process(5,0.5,0.1,0.1)


