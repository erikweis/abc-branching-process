import scipy.stats
import numpy as np
import requests


def priors(a_R0, b_R0, a_K, b_K):
    return [scipy.stats.uniform.rvs(a_R0, b_R0), scipy.stats.uniform.rvs(a_K, b_K), scipy.stats.uniform.rvs(0,0.1)]

def binom_pull(r, infect_count):
    return np.random.binomial(infect_count, 1 - r)


def neg_binom_pull(r0, k):
    p = r0 / (r0 + k)
    n = 1/k
    return scipy.stats.nbinom.rvs(n, p)


def abc_check(cumu_count, cumul_case_data):
    error = (cumu_count - cumul_case_data) / cumul_case_data

    if error > 1:
        return False
    else:
        return True



def simulate_branching_process(cumul_case, time, A_R0, B_R0, A_K, B_K):
    r0, k, r = priors(A_R0, B_R0, A_K, B_K)
    trans_vec = np.zeros(time)
    infect_vec = np.zeros(time)

    infect_vec[0] = 1
    for i in range(1, T):
        temp = 0
        for j in range(int(infect_vec[i-1])):
            temp = temp + neg_binom_pull(r0, k)

        trans_vec[i] = temp
        infect_vec[i] = trans_vec[i] + binom_pull(r, infect_vec[i - 1])

        #Check the values here for the ABC



        # Check the values here for the ABC
        checkpoints = [15, 30, 45, 60, 75, 90]

        if i == 45:
            print("Halfway")
        if i in checkpoints:
            print("Count: %d" %(np.sum(trans_vec)))
            check = abc_check(np.sum(trans_vec), cumul_case[i])
            if check:
                if i == 90:
                    return [r0, k, np.sum(trans_vec[0:T]) + 1]

            else:
                return [r0, k, -99]


    # print(infect_vec)
    # print(trans_vec)
    # return np.sum(trans_vec[0:T]) + 1


if __name__ == "__main__":
    url = 'https://api.covidtracking.com/v2/states/ny/daily/simple.json'
    out = requests.get(url).json()

    data = out['data'][::-1]

    T = 90
    cumulative_cases_data = [d['cases']['total'] for d in data[:T]]
    sampR0, sampK, simulated_cases  = simulate_branching_process(cumulative_cases_data, T, 1, 4, .1, .5)

    print("k:",sampK)
    print("R0:", sampR0)
    print(simulated_cases)

    # import matplotlib.pyplot as plt
    # plt.hist(t1)
    # plt.show()

