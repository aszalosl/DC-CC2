# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 08:04:45 2017

@author: laszalos

Clustering sparse graphs."""

from typing import Dict

from graph import Graph, FixedGraph, Cluster, Node
import divide as d


def sequence(move_func, contract_func, uf, g:Graph) -> Dict[Node, Cluster]:
    """Execute the move and contract functions together.
    Repeat until there is no improvement.

    Parameters
    ----------
    move_func: function moves the nodes
    contract_func: function joins clusters
    N: number of nodes
    g: the original graph

    Returns
    -------
    clustering of nodes
    """
    while True:
        moved = move_func(uf, g)
        contracted = contract_func(g.calc_contract(uf), uf, g)
        # print(g.conflicts(uf), end=" ")
        if not moved and not contracted:
            break
    return uf


def iterated(move_func, contract_func, uf, g:Graph) -> Dict[Node, Cluster]:
    """Repeat the move and contract functions alone
    until there is no impovement.

    Parameters
    ----------
    move_func: function moves the nodes
    contract_func: function joins clusters
    N: number of nodes
    g: the original graph

    Returns
    -------
    clustering of nodes"""
    while True:
        while move_func(uf, g):
            pass
        contracted = False
        while contract_func(g.calc_contract(uf), uf, g):
            contracted = True
        if not contracted:
            break
    return uf

def iterated2(move_func, contract_func, uf, g:Graph) -> Dict[Node, Cluster]:
    """Repeat the move and contract functions alone
    until there is no impovement.

    Parameters
    ----------
    move_func: function moves the nodes
    contract_func: function joins clusters
    N: number of nodes
    g: the original graph

    Returns
    -------
    clustering of nodes"""
    while True:
        while contract_func(g.calc_contract(uf), uf, g):
            pass
        moved = False
        while move_func(uf, g):
            moved = True
        if not moved:
            break
    return uf


def recurse(fm, fc, fo, g: Graph) -> Dict[Node, Cluster]:
    """Recursive execution of the clustering.

    Parameters
    ----------
    fn: function moves the nodes
    fc: function contracts the clusters
    fo: function directs the previous functions
    lower, upper: limit of calculations
    g: the graph to clustering.

    Returns
    -------
    the clustering"""
    K = 20

    if g.size < 100:
        uf = {i:i for i in g.nodes}
        # print("uf 0: ", uf)
        uf = fo(fm, fc, uf, g)
        # print("got uf:", uf)
        return uf
    else:
        groups = d.divide(K, g)
        # print("Gs:", groups)
        uf = {}
        for i in range(K):
            new_edges = d.filter_edges(groups[i],g.edges)
            gs = FixedGraph(groups[i], new_edges)
            uf_i = recurse(fm, fc, fo, gs)
            uf.update(uf_i)
        # print(uf)
        return fo(fm, fc, uf, g)
