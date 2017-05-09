"""testing the ideas - efficiency"""
from graph import BAGraph
import sparse_contract as sc
import sparse_move as sm
import sparse_methods as m
STEPS = 100

def compare(N, repetition):
    counter = {}
    sums = {}
    for _ in range(repetition):
        g = BAGraph(N, 0.0)
        positives = 0
        n_edges = len(g.edges)
        for j in range(1, STEPS+2):
            r = g.q_rate()
            counter[r] = counter.get(r,0)+1

            # sm.the_all
#            uf = m.sequence(sm.the_all, sc.iterate_all, N, g)
#            sums[(1, r)] = sums.get((1, r), 0) + g.conflicts(uf)
#            uf = m.sequence(sm.the_all, sc.iterate_min, N, g)
#            sums[(2, r)] = sums.get((2, r), 0) + g.conflicts(uf)
#            uf = m.sequence(sm.the_all, sc.one, N, g)
#            sums[(3, r)] = sums.get((3, r), 0) + g.conflicts(uf)
#            uf = m.sequence(sm.the_all, sc.independent, N, g)
#            sums[(4, r)] = sums.get((4, r), 0) + g.conflicts(uf)
            # sm.independent
#            uf = m.sequence(sm.independent, sc.iterate_all, N, g)
#            sums[(5, r)] = sums.get((5, r), 0) + g.conflicts(uf)
#            uf6 = {i: i for i in range(1,N+1)}
#            uf6 = m.iterated(sm.independent, sc.iterate_min, N, g)
#            sums[(6, r)] = sums.get((6, r), 0) + g.conflicts(uf)
            uf7 = m.recurse(sm.independent, sc.one, m.iterated, g)
            sums[(7, r)] = sums.get((7, r), 0) + g.conflicts(uf7)
            uf8 = {i: i for i in range(1,N+1)}
#            uf8 = m.iterated2(sm.independent, sc.one, uf8, g)
#            sums[(8, r)] = sums.get((8, r), 0) + g.conflicts(uf8)
            uf8 = m.iterated(sm.independent, sc.iterate_min, uf8, g)
            sums[(8, r)] = sums.get((8, r), 0) + g.conflicts(uf8)
            uf9 = {i: i for i in range(1,N+1)}
            uf9 = m.iterated(sm.independent, sc.one, uf9, g)
            sums[(9, r)] = sums.get((9, r), 0) + g.conflicts(uf9)

            diff = round(j*n_edges/STEPS)-positives
            g.recolor(diff)
            positives = round(j*n_edges/STEPS)
        print(".", end="")
    print("")
    ks = list(counter.keys())
    # print("ks:", ks)
    ks.sort()
    for k in ks:
        print("{0:.3f}".format(k), end="\t")
        for i in range(7,10):
            a = sums[(i,k)]/counter[k]
            print("{0:6.2f}".format(a), end="\t")
        print("")



if __name__ == "__main__":
    N = 500
    compare(N, 20)
