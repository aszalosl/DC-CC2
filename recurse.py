#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:49:25 2017

Recursive execution
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
uf = m.recurse(sm.independent, sc.one, m.iterated, lo, up, g)
# print("all:", uf)
endTime = time.time()
#calculate the total time it took to complete the work
workTime =  endTime - startTime
         
#print results
print("The job took " + str(workTime) + " seconds to complete")

