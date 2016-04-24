import random as r
import numpy as np
import scipy
import fixed_degree_gen as fd

def sim21(trials, g_size, dist = None):
    if dist is None:
        dist = lambda : np.random.binomial(5, .5) 
    x_1_trials = {}
    for _ in range(trials):
        g = fd.gen_fixed_degree_graph(g_size, dist)
        loop_count = 0
        for i in range(g_size):
            loop_count += g[i,i]
        if not loop_count in x_1_trials:
            x_1_trials[loop_count] = 1
        else:
            x_1_trials[loop_count] += 1
    return x_1_trials

 
print sim21(1000, 1000)
#P(0) = P(1) = e^-1 ~ .367
#Result: {0.0: 368, 1.0: 366, 2.0: 176, 3.0: 60, 4.0: 25, 5.0: 4, 6.0: 1}   


def sim22(trials, g_size, dist = None):
    if dist is None:
        dist = lambda : np.random.binomial(5, .5) 
    x_2_trials = {}
    j = 0
    for _ in range(trials):
        g = fd.gen_fixed_degree_graph(g_size, dist)
        parallel_count = 0
        for i in range(g_size):
            for k in range(1+i,g_size):
                parallel_count += scipy.special.binom(g[i,k],2)
        if not parallel_count in x_2_trials:
            x_2_trials[parallel_count] = 1
        else:
            x_2_trials[parallel_count] += 1
        j += 1
    return x_2_trials



print sim22(1000, 1000)
#P(0) = P(1) =  e^-1 ~ .367
#Result: {0.0: 360, 1.0: 364, 2.0: 203, 3.0: 51, 4.0: 19, 5.0: 2, 6.0: 1}

def is_simple(g):
    g_size = g.shape[0]
    for i in range(g_size):
        for k in range(1+i,g_size):
            if (g[i,k] > 1):
                return False
        if (g[i,i] > 0):
            return False
    return True

def sim23(trials, g_size, dist = None):
    if dist is None:
        dist = lambda : np.random.binomial(5, .5) 
    x_3_trials = 0
    for _ in range(trials):
        g = fd.gen_fixed_degree_graph(g_size, dist)
        x_3_trials += is_simple(g)
    return x_3_trials


print sim23(1000, 1000)
#P(Simple) = e^-2 ~ .135
#Result: 143
