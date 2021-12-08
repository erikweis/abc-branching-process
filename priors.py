import scipy.stats
import numpy as np
from seaborn.distributions import kdeplot
import matplotlib.pyplot as plt

def non_parametric_priors():
    probs = []
    
    mus = [1, 0.8, 0.6, 0.4, 0.2, 0.1 ,0.1, 0.1, 0.1, 0.1]
    
    for i in range(10):
        value = scipy.stats.norm.rvs(mus[i], 1)
        while (value < 0):
            value = scipy.stats.norm.rvs(mus[i], 1)
        
        probs.append(value)
        
    probs = probs/np.sum(probs)
    
    return  probs



def normal_priors():
    
    r0,k,r = -1,-1,-1
    while (r0<0 or k<0 or k>1 or r<0 or r>1):
        r0 = scipy.stats.norm.rvs(3.2,1.3)
        k = scipy.stats.norm.rvs(0.5,0.7)
        r = scipy.stats.norm.rvs(0.1,0.2)
    
    return r0,k,r


def uniform_priors():
    return [scipy.stats.uniform.rvs(1,5), scipy.stats.uniform.rvs(0.5,1.5), scipy.stats.uniform.rvs(0,0.6)]

def plot_priors(prior_func, samples=1000):

    samples = np.array([prior_func() for _ in range(samples)])

    out1 = kdeplot(samples[:,0],label='r0')
    out2 = kdeplot(samples[:,1],label='k')
    out3 = kdeplot(samples[:,2],label='r')
    plt.legend()
    plt.show()

def plot_nonparametric_priors(prior_func, samples = 1000):

    samples = np.array([prior_func() for _ in range(samples)])
     
    fig,axes = plt.subplots(5,2)

    for i, ax in enumerate(axes.flatten()):
        kdeplot(ax = [i//5], x = samples[:,i], label=("p_{%d}" %i))
        
        
    plt.show()

if __name__ == "__main__":

    plot_priors(normal_priors,samples=10000)
    plot_nonparametric_priors(non_parametric_priors, samples = 10000)