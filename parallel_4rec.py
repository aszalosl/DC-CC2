#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:49:25 2017

Multiprocessing execution
@author: laci
"""
import multiprocessing as mp
import time
import math

import sparse_methods as m
import sparse_move as sm
import sparse_contract as sc
import graph
import divide as d

def start_calc(fm, fc, fo, nodes, g, out_queue):
    new_edges = d.filter_edges(nodes,g.edges)
    gs = graph.FixedGraph(nodes, new_edges)
    # print("gs.nodes", gs.nodes)
    uf = m.recurse(fm, fc, fo, gs)
    # print("start uf:", uf)
    out_queue.put(uf)


N = 5000
procs = []
cores = 4
chunksize = int(math.ceil(N) / float(cores))

g = graph.BAGraph(N, 0.6)
groups = d.divide(cores, g)

startTime = time.time()

myQueue = mp.Queue()

for i in range(cores):
    p = mp.Process(target=start_calc,
                    args=(sm.independent, sc.one, m.iterated,\
                          groups[i], g, myQueue))
    procs.append(p)
    p.start()


result = {}
for i in range(cores):
    result.update(myQueue.get())

for p in procs:
    p.join()

middleTime = time.time()

uf = m.iterated(sm.independent, sc.one, result, g)
endTime = time.time()
workTime =  endTime - startTime

#print results
print("The job took " + str(workTime) + " seconds to complete")
print("Last part" + str(endTime - middleTime) )
