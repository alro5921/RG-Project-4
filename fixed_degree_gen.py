import random as r
import numpy as np
from functools import reduce
from enum import Enum
from collections import defaultdict

from scipy.stats import poisson
from scipy.special import binom
import matplotlib.pyplot as plt
import click


class Dist(Enum):
    binomial = 1
    geometric = 2


def gen_fixed_degree_graph(dist, n):
    if dist == Dist.binomial:
        dist = lambda: np.random.binomial(5, .5, size=n)
    elif dist == Dist.geometric:
        dist = lambda: np.random.geometric(.4, size=n)

    degrees = None
    while degrees is None or np.sum(degrees) % 2 != 0:
        degrees = dist()

    g_d = np.zeros((n, n))
    half_edges = reduce(lambda x, y: x + y, [[i] * degrees[i] for i in range(n)])
    r.shuffle(half_edges)
    while len(half_edges) > 0:
        u = half_edges.pop()
        v = half_edges.pop()
        if u == v:
            g_d[u, v] += 1
        else:
            g_d[u, v] += 1
            g_d[v, u] += 1
    return g_d


def count_loops(g):
    n = len(g)
    loops = 0
    for i in range(n):
        loops += g[i, i]
    return loops


def count_parallel_edges(g):
    n = len(g)
    parallel = 0
    for i in range(n):
        for j in range(i, n):
            parallel += int(binom(g[i, j], 2))
    return parallel


@click.command()
@click.argument('dist_name')
@click.argument('edge')
def main(dist_name, edge):
    edges = defaultdict(int)
    if dist_name == 'binomial':
        dist = Dist.binomial
        lam = 1
    elif dist_name == 'geometric':
        dist = Dist.geometric
        lam = 1.5
    else:
        raise ValueError("Wrong dist argument")

    if edge == 'loop':
        count = count_loops
    elif edge == 'parallel':
        count = count_parallel_edges
        lam **= 2
    else:
        raise ValueError('Wrong edge argument')

    for _ in range(1000):
        g = gen_fixed_degree_graph(dist, 250)
        edges[count(g)] += 1

    x = np.array(list(edges.keys()))
    y = np.array(list(edges.values()))
    y = y / np.sum(y)
    p_y = poisson.pmf(x, lam)
    plt.style.use('ggplot')
    experimental = plt.scatter(x, y)
    theoretical = plt.scatter(x, p_y, c='r', marker='+')
    plt.legend((experimental, theoretical), ('Experimental', 'Theoretical'))
    plt.title(edge + ' ' + dist_name)
    plt.xlabel('N')
    plt.ylabel('Probability')
    plt.show()

if __name__ == '__main__':
    main()
