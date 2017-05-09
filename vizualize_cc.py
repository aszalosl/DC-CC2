"""visualize original problem and a solution"""
from graph import BAGraph
import sparse_contract as sc
import sparse_move as sm
import sparse_methods as m

import numpy as np
import matplotlib.pyplot as plt

N = 100
g = BAGraph(N, 0.7)
grid = np.zeros((N,N), dtype=np.int8)
grid2 = np.zeros((N,N), dtype=np.int8)
uf = m.recurse(sm.independent, sc.one, m.iterated, g)
s = [k for k in sorted(uf, key=uf.get)]
inv_s = [0]*N
for i, j in enumerate(s):
    inv_s[j-1] = i
left = 0
while left < N:
    right = left
    print(left, right)
    while right<N and uf[s[right]] == uf[s[left]]:
        print(right)
        right +=1
    grid2[left:right,left:right] = 2
    left = right

for x, y, w in g.edges:
    if w == 1:
        grid[x-1,y-1] = 3
        grid[y-1,x-1] = 3
        grid2[inv_s[x-1],inv_s[y-1]] = 3
        grid2[inv_s[y-1],inv_s[x-1]] = 3
    else:
        grid[x-1,y-1] = 1
        grid[y-1,x-1] = 1
        grid2[inv_s[x-1],inv_s[y-1]] = 1
        grid2[inv_s[y-1],inv_s[x-1]] = 1

plt.imshow(grid, plt.get_cmap('Greys'))
plt.savefig('BA100.png')
plt.imshow(grid2, plt.get_cmap('Greys'))
plt.savefig('BA100o.png')


