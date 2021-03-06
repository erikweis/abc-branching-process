import scipy.stats
import numpy as np
from seaborn.distributions import kdeplot
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

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

def get_truncnorm(min_val, max_val, mean, std):

    a,b = (min_val - mean)/std , (max_val - mean)/std
    return truncnorm(a,b,scale=std,loc=mean).rvs()


def normal_priors(state='vt'):

    if state=='wi':
        r0 = get_truncnorm(2, 8, 4.5, 1.5)
        k = get_truncnorm(0, 0.5, 0.1, 0.2)
        r = get_truncnorm(0, 1, 0.8, 0.1)
        res = np.random.randint(0,40)
    else:
    
        r0 = get_truncnorm(1, 7, 3.2, 1.3)
        k = get_truncnorm(0, 0.5, 0.13, 0.5)
        r = get_truncnorm(0, 1, 0.7, 0.1)
        res = np.random.randint(0,40)
    
    return r0, k, r, res


def uniform_priors():
    return [scipy.stats.uniform.rvs(1,5), scipy.stats.uniform.rvs(0.5,1.5), scipy.stats.uniform.rvs(0,0.6)]

def plot_priors(prior_func, samples=1000,state='vt'):

    samples = np.array([prior_func(state) for _ in range(samples)])

    fig, ax = plt.subplots(1,3,figsize=(9,3))

    plt.sca(ax[0])
    out1 = kdeplot(samples[:,0],label='r0')
    plt.title('r0')
    plt.sca(ax[1])
    plt.title('k')
    out2 = kdeplot(samples[:,1],label='k')
    plt.sca(ax[2])
    plt.title('recovery')
    out3 = kdeplot(samples[:,2],label='r')
    plt.tight_layout()
    plt.show()

def plot_nonparametric_priors(prior_func, samples = 1000):

    samples = np.array([prior_func() for _ in range(samples)])
     
    fig,axes = plt.subplots(5,2)

    for i, ax in enumerate(axes.flatten()):
        kdeplot(ax = [i//5], x = samples[:,i], label=("p_{%d}" %i))
        
        
    plt.show()

if __name__ == "__main__":

    plot_priors(normal_priors,samples=1000,state='wi')
    #plot_nonparametric_priors(non_parametric_priors, samples = 10000)