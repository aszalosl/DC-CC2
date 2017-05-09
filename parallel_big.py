#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:49:25 2017

Multiprocessing execution
just some run for big graphs
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


def iter_calc(nodes):
    new_edges = d.filter_edges(nodes,g.edges)
    gs = graph.FixedGraph(nodes, new_edges)
    uf = {i: i for i in nodes}
    # print("gs.nodes", gs.nodes)
    uf = m.iterated(sm.independent, sc.iterate_min, uf, gs)
    # print("start uf:", uf)
    return uf

def rec_calc(nodes):
    new_edges = d.filter_edges(nodes,g.edges)
    gs = graph.FixedGraph(nodes, new_edges)
    uf = {i: i for i in nodes}
    # print("gs.nodes", gs.nodes)
    uf = m.recurse(sm.independent, sc.iterate_min, m.iterated, gs)
    # print("start uf:", uf)
    return uf

def test(N):
    global g
    cores = 20
    g = graph.BAGraph(N, 0.6)
    groups = d.divide(cores, g)
    startTime = time.time()
    ###############################xx
    with mp.Pool(4) as p2:
        result2 = p2.map(rec_calc, groups)
    # print(result2)
    r2 = {}
    for i in result2:
        r2.update(i)
    middleTime2 = time.time()

    uf2 = m.iterated(sm.independent, sc.iterate_min, r2, g)
    endTime2 = time.time()
    ##################
    uf = {i:i for i in g.nodes}
    uf3 = m.iterated(sm.independent, sc.iterate_min, uf, g)
    endTime3 = time.time()
    #print results
    return "{0:8.3f}\t{1:8.3f}\t{2:6d}\t{3:8.3f}\t{4:6d}\n".format(\
      endTime2 - startTime, endTime2 - middleTime2, g.conflicts(uf2),\
      endTime3 - endTime2, g.conflicts(uf3))
for _ in range(10):
    print(test(30000))
