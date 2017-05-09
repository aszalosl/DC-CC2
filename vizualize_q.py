"""Vizualize the costs according to q"""
from graph import BAGraph
import sparse_contract as sc
import sparse_move as sm
import sparse_methods as m

import matplotlib.pyplot as plt

N = 300
r = []
c = []
for i in range(10):
    for j in range(101):
        g = BAGraph(N, j/100.0)
        uf = m.recurse(sm.independent, sc.iterate_min, m.iterated, g)
        r.append(g.q_rate())
        c.append(g.conflicts(uf))
plt.scatter(r,c,marker=".")
plt.xlabel('rate q')
plt.ylabel('no of conflicts')
#plt.show()
plt.savefig('CC300.png')
