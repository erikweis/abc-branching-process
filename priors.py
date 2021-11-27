import scipy.stats
import numpy as np

def priors(a_R0, b_R0, a_K, b_K):
    return [scipy.stats.uniform.rvs(a_R0, b_R0), scipy.stats.uniform.rvs(a_K, b_K), scipy.stats.uniform.rvs(0,0.1)]

