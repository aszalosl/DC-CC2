#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:49:25 2017

Sequential execution
@author: laci
"""
import time

import sparse_methods as m
import sparse_move as sm
import sparse_contract as sc
import graph


startTime = time.time()

lo = 0
up = 15000

g = graph.BAGraph(up, 0.7)
uf1 = [i for i in range(lo,up)]
uf = m.iterated(sm.independent, sc.one, uf1, g)
# print("all:", uf)
endTime = time.time()
#calculate the total time it took to complete the work
workTime =  endTime - startTime
         
#print results
print("The job took " + str(workTime) + " seconds to complete")

