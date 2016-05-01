import random as r
import numpy as np

p = .95 #probability degree = 0 (isolated node)
dist = lambda : int(r.random() > p)
n = 3

def m1():
    while(True):
        degrees = []
        for _ in range(n):
            degrees.append(int(dist()))
        if sum(degrees) % 2 == 0:
            return degrees
        
def m2():
    degrees = []
    for _ in range(n-1):
            degrees.append(int(dist()))
    while (True):
        d_n = int(dist())
        if (sum(degrees) % 2 == d_n % 2): #both are odd or both are even
            degrees.append(d_n)
            return degrees



m1_count, m2_count = 0,0            
for _ in range(10000):
    #counting whether all nodes are isolated (likely with p = .95 and n = 3)
    m1_count += (reduce(lambda x,y: x + y,m1()) == 0)
    m2_count += (reduce(lambda x,y: x + y,m2()) == 0)

print m1_count, m2_count
#Result: 99186, 90262