import random as r
import numpy as np

def gen_fixed_degree_graph(n, dist = None):
    if dist is None:
        dist = lambda : np.random.binomial(5, .2)
    degrees = []
    for _ in range(n-1):
        degrees.append(int(dist()))
        
    sub_d_is_odd = sum(degrees) % 2
    while (True):
        d_n = int(dist())
        if (sub_d_is_odd == d_n % 2): #both odd or both even
            degrees.append(d_n)
            break;    
    
    g_d = np.zeros((n,n))
    D = sum(degrees)
    while (D > 0):
        n1, n2 = pick_nodes(degrees)
        g_d[n1,n2] += 1
        g_d[n2,n1] += 1
        degrees[n1] -= 1
        degrees[n2] -= 1
        D -= 2
    for i in range(n):
        g_d[i,i] /= 2 #Each self loop is counted twice in the above
    return g_d
        
    
def pick_nodes(degrees): #I feel there's a better way of doing this
    D = sum(degrees)
    while(True):
        index1, index2 = r.randint(1,D), r.randint(1,D)
        if (index1 != index2):
            break;
 
    found1, found2 = False, False
    t = 0
    for i, degree in enumerate(degrees):
        t = t + degree
        if t >= index1 and not found1:
            n1 = i
            found1 = True
        if t >= index2 and not found2:
            n2 = i
            found2 = True
    return n1,n2
