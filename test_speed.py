"""testing the ideas - speed"""
from timer import Timer
from graph import BAGraph, Node
import sparse_contract as sc
import sparse_move as sm
import sparse_methods as m
STEPS = 12

def stats(ps):
    """Averages of conflicts at different q rates

    Parameter
    ---------
    ps: list of pairs of rates and conflicts

    Returns
    -------
    statistics """
    s = {}
    c = {}
    for p in ps:
        i,t = p
        c[i] = c.get(i,0) + 1
        s[i] = s.get(i,0) + t
    r = {}
    for i in c:
        r[i] = s[i]/c[i]
    return r

def sum_stat(ps):
    sum = 0
    for t in ps:
        sum += t[1]
    return sum


def q_run_BA(N, repetition, fm, fc, fo):
    """Speed test of several run of clustering of given size random BA.

    Parameters
    ----------
    N: size of the graph
    repetition: number of tests
    move_func: function moves nodes
    contract_func: function joins clusters

    Returns
    -------
    list of pairs of q_rates and conflicts
    """
    run = []
    for _ in range(repetition):
        g = BAGraph(N, 0.0)
        # print(g.nodes, g.edges)
        positives = 0
        n_edges = len(g.edges)
        for j in range(1, STEPS+2):
            uf = {i: i for i in range(1,N+1)}
            uf = fo(fm, fc, uf, g)
            run.append((g.q_rate(),g.conflicts(uf)))
            diff = round(j*n_edges/STEPS)-positives
            g.recolor(diff)
            positives = round(j*n_edges/STEPS)
            print(".", end="")
    return run

def q_rec_BA(N, repetition, fm, fc, fo):
    """Speed test of several run of clustering of given size random BA.

    Parameters
    ----------
    N: size of the graph
    repetition: number of tests
    move_func: function moves nodes
    contract_func: function joins clusters

    Returns
    -------
    list of pairs of q_rates and conflicts
    """
    run = []
    for _ in range(repetition):
        g = BAGraph(N, 0.0)
        #print(g.edges)
        positives = 0
        n_edges = len(g.edges)
        for j in range(1, STEPS+2):
            uf = m.recurse(fm, fc, fo, g)
            run.append((g.q_rate(),g.conflicts(uf)))
            diff = round(j*n_edges/STEPS)-positives
            g.recolor(diff)
            positives = round(j*n_edges/STEPS)
            print(".", end="")
    return run

if __name__ == "__main__":
    N = 20000
#    with Timer() as t:
#        s = q_run_BA(N, 5, sm.independent, sc.one, m.sequence)
#    print("independent+one+seq: time %s sec, %d conflicts" % (t.secs, sum_stat(s)))
    # print(stats(s))
    with Timer() as t:
        s = q_run_BA(N, 2, sm.independent, sc.one, m.iterated)
    print("independent+one+iter: time %s sec, %d conflicts" % (t.secs, sum_stat(s)))
    # print(stats(s))
    with Timer() as t:
        s = q_rec_BA(N, 2, sm.independent, sc.one, m.iterated)
    print("independent+one+iter (rec): time %s sec, %d conflicts" % (t.secs, sum_stat(s)))
    # print(stats(s))
    with Timer() as t:
        s = q_run_BA(N, 2, sm.independent_par, sc.one, m.iterated)
    print("independent_par+one+seq: time %s sec, %d conflicts" % (t.secs, sum_stat(s)))
#    q_run_BA(N, 5, sm.independent_par, sc.one, m.iterated)