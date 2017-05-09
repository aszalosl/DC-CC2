#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:59:34 2017

Divide a graph into connected subgraphs

@author: laci
"""

import math
import collections
import graph as g
from typing import List, Tuple


def _next_group(remained, chunksize, bg:g.Graph) -> List[int]:
    """Calculate a group of nodes are mostly connected.

    Parameters
    ----------
    remained: the nodes are used yet
    chunksize: the size of the group
    bg: the big graph to divide

    Returns
    -------
    a list of nodes

    """
    group = []
    stack = collections.deque()
    stack_cntr = 1
    first = remained.pop()
    remained.add(first)
    # print(remained, bg.neighbours)
    stack.append(first)
    i = 0
    while i < chunksize:
        if stack_cntr > 0:
           x = stack.popleft()
           stack_cntr -= 1
           if x in remained:
               group.append(x)
               remained.remove(x)
               i += 1
               for j in bg.neighbours[x]:
                   jj = abs(j)
                   if jj in remained:
                       stack.append(jj)
                       stack_cntr += 1

        else:
            first = remained.pop()
            remained.add(first)
            stack.append(first)
            stack_cntr = 1
    return group


def divide(K: int, bg:g.Graph) -> List[List[int]]:
    """Divide the nodes of a graph based on its edges

    Parameters
    ----------
    N: number of nodes
    K: number of groups

    Returns
    -------
    List of list of nodes"""

    N = bg.size
    # print("N:", N)
    chunksize = int(math.ceil(N) / float(K))
    remained = {i for i in bg.nodes}
    result = []
    for i in range(1,K):
        ng = _next_group(remained, chunksize, bg)
        # print("ng", ng)
        result.append(ng)
    # remaining nodes, i.e. are not used yet
    result.append(list(remained))
    # print("divide:", result)
    return result

def split_edges(lower, upper, g):
    """Select the edges of the subgraph based on indices.

    Parameters
    ----------
    lower, upper: limits of calculation
    g: the original graph

    Returns
    -------
    the edges of the subgraph"""
    sub_edges = []
    for edge in g.edges:
        x, y, v = edge
        if lower <= min(x,y) and max(x,y) < upper:
            sub_edges.append(edge)
    return sub_edges



def filter_edges(nodes:List[int], edges: List[Tuple[int,int,int]]) -> List[Tuple[int,int,int]]:
    """Filter the edges of a subgraph.

    Parameters
    ----------
    nodes: list containing the nodes
    edges: list containing the edges of the original graph

    Returns
    -------
    inverse dictionary of nodes
    filtered edges"""

    ns = {v: k for k,v in enumerate(nodes)}
    new_edges = []
    for x, y, v in edges:
        if x in ns and y in ns:
            new_edges.append((x, y,v))
    return new_edges

def test_divide(K,vbg):
    print("Original: ", len(vbg.edges))
    lgs = divide(K, vbg)
    sum = 0
    for ls in lgs:
        ns = {v: k for k,v in enumerate(ls)}
        # print(len(ls), ls)
        ne = filter_edges(ns, vbg.edges)
        sum += len(ne)
    return sum

def test_split(K,vbg):

    chunksize = int(math.ceil(vbg.size) / float(K))
    sum = 0
    for i in range(K):
        ne = split_edges(i*chunksize, (i+1)*chunksize, vbg)
        sum += len(ne)
    return sum

if __name__ == "__main__":
    N = 400
    K = 20
    vbg = g.BAGraph(N,0.7)
    oe = len(vbg.edges)
    de = test_divide(K,vbg)
    se = test_split(K,vbg)
    print("BA Original: {0}, divide: {1}({2:.1f}), split: {3}({4:.1f})".format(oe,
          de, 100*de/oe, se,  100*se/oe))

    vbg = g.ERGraph(N, 0.2, 0.7)
    oe = len(vbg.edges)
    de = test_divide(K,vbg)
    se = test_split(K,vbg)
    print("ER Original: {0}, divide: {1}({2:.1f}), split: {3}({4:.1f})".format(oe,
          de, 100*de/oe, se, 100*se/oe))
