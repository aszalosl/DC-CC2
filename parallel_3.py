#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:49:25 2017

Multiprocessing execution
@author: laci
"""
import multiprocessing as mp
import time

import sparse_methods as m
import sparse_move as sm
import sparse_contract as sc
import graph


startTime = time.time()

lo = 0
up = 15000

g = graph.BAGraph(up, 0.7)
t1 = (2*lo + up)//3
t2 = (lo + 2*up)//3
g1 = graph.FixedGraph(m.filter_edges(lo, t1, g), lo, t1)
g2 = graph.FixedGraph(m.filter_edges(t1, t2, g), t1, t2)
g3 = graph.FixedGraph(m.filter_edges(t2, up, g), t2, up)


def start_calc(fm, fc, fo, l, u, g, out_queue):
    uf = m.recurse(fm, fc, fo, l, u, g)
    # print(uf)
    out_queue.put(uf)

myQueue = mp.Queue()

procs = []
p1 = mp.Process(target=start_calc, args=(sm.independent, sc.one, m.iterated,  0, t1, g1, myQueue))
p1.start()
p2 = mp.Process(target=start_calc, args=(sm.independent, sc.one, m.iterated, t1, t2, g2, myQueue))
p2.start()
p3 = mp.Process(target=start_calc, args=(sm.independent, sc.one, m.iterated, t2, up, g3, myQueue))
p3.start()

procs.append(p1)
procs.append(p2)
procs.append(p3)
uf1 = myQueue.get()
uf2 = myQueue.get()
uf3 = myQueue.get()
for p in procs:
    p.join()

# print("1 -->", uf1)
# print("2 -->", uf2)
# print("3 -->", uf3)


uf1.extend(uf2)
uf1.extend(uf3)
uf = m.iterated(sm.independent, sc.one, uf1, g)
# print("all:", uf)
endTime = time.time()
#calculate the total time it took to complete the work
workTime =  endTime - startTime
         
#print results
print("The job took " + str(workTime) + " seconds to complete")

