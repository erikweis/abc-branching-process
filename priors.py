import scipy.stats
import numpy as np

def priors(a_R0, b_R0, a_K, b_K):

    r0,k,r = -1,-1,-1
    while (r0<0 or k<0 or r<=0 or r>1):
        r0 = scipy.stats.norm.rvs(3.2,1.3)
        k = scipy.stats.norm.rvs(0.8,0.7)
        r = scipy.stats.uniform.rvs(0,0.5)
    
    return r0,k,r
    #return [scipy.stats.uniform.rvs(a_R0, b_R0), scipy.stats.uniform.rvs(a_K, b_K), scipy.stats.uniform.rvs(0,0.6)]

if __name__ == "__main__":

    print(priors(1,2,3,4))