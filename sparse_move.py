"""Movement for sparse graphs."""
from graph import Graph, BAGraph, Node, Cluster
from typing import Dict, Tuple
from operator import itemgetter
from functools import partial
import multiprocessing as mp


def _escape(j: Node, uf: Dict[Node, Cluster]) -> None:
    """If no cluster attract node j than we move it into an empty cluster.

    Parameters
    ---------
    j: node
       actual node
    uf: list of clusters
       clustering
    start: minimal value in uf

    Returns
    -------
    new cluster Id for node j"""

    # search for an empty cluster (free cluster-id)

    occurs = set(uf.keys())
    for k, v in uf.items(): # mark the used clusters
        occurs.discard(v)
#    c1 = g.conflicts(uf)  # 4test
#    f1 = g.calc_attract(j, uf, lower, upper)  # 4test
    k = occurs.pop()
    uf[j] = k


def the_all(uf: Dict[Node, Cluster], g: Graph) -> bool:
    """Move all the nodes into the most attractive clusters.
    We use updated forces.

    Parameters
    ---------
    uf: list of clusters
       clustering
    g: the graph of the tolerance relation
    lower, upper: clusters
       limit of computations

    Returns
    -------
    something modified?"""

    # c1 = g.conflicts(uf) # 4test
    changed = False
    for i in range(g.size):
        forces = g.calc_attract(i, uf)  # recalculate forces
        new_cluster, attract = max(forces.items(), key=itemgetter(1))
        old_cluster = uf[i]
        if (attract > 0 and forces[old_cluster] < attract) or attract < 0:
            if attract < 0:
                # print(i, forces, uf, g.edges)
                _escape(i, uf, g.start)
                changed = True
            else:
                uf[i] = new_cluster
                changed = True
            # c2 = g.conflicts(uf)  # 4test
#            if c1 <= c2:
#                print("move {} into {}".format(i, cluster))
#                print("forces for {}: {}".format(i, forces))
#                print("uf:", uf)
#                print("before: {}, after: {}".format(c1,c2))
#                raise ValueError('seq move')
#            c1 = c2
    return changed

def _to_move(uf: Dict[Node, Cluster], g: BAGraph) -> Dict[Node, Tuple[Cluster, int]]:
    """Calculate "in parallel" for each node the most attractive clusters.

    Parameters
    ---------
    uf: list of clusters
       clustering
    g: the graph of the tolerance relation

    Returns
    -------
      most attractive clusters for nodes"""

    moves = {}
    # print(g.neighbours)
    for k, c in uf.items():
        forces = g.calc_attract(k, uf)   # forces contains attract of old_cluster
        new_cluster, attract = max(forces.items(), key=itemgetter(1))
        old_cluster = c
        if (attract > 0 and forces[old_cluster] < attract)  or attract < 0:
            # print("m({})={}/{} from {} ({})".format(i,cluster,a, forces, uf[i]))
            moves[k] = (new_cluster, attract)
    # print("m: ", m)
    return moves


def independent(uf: Dict[Node, Cluster], g: Graph) -> bool:
    """Move independent nodes to their most attractive clusters.

    Parameters
    ---------
    uf: list of clusters
       clustering
    g: the graph of the tolerance relation

    Returns
    -------
     something modified?"""

    moves = _to_move(uf, g)
    if moves == {}:
        return False
    # c1 = g.conflicts(uf) # 4test
    forbidden = set()
    #print("moves:", moves)
    for n, ca in moves.items():
        new_cluster, attract = ca
        old_cluster = uf[n]
        if attract < 0 and old_cluster not in forbidden:
            # go somewhere else
            #forces = g.calc_attract(i,uf)
            #print(i, forces, uf[i], moves)
            new_cluster = _escape(n, uf)
            forbidden.add(old_cluster)
            forbidden.add(new_cluster)
        else:
            # joined to a more attractive cluster
            if old_cluster not in forbidden and new_cluster not in forbidden:
                forbidden.add(old_cluster)
                forbidden.add(new_cluster)
                uf[n] = new_cluster
    # c2 = g.conflicts(uf)  # 4test
    # if c1 <= c2:
    #     print("before: {}, after: {}, moves:{}".format(c1, c2, moves))
    #     raise ValueError('sm-independent')
    return True


def _one_move(uf, g, nodes):
    moves = []
    for k in nodes:
        old_cluster = uf[k]
        forces = g.calc_attract(k, uf)   # forces contains attract of old_cluster
        new_cluster, attract = max(forces.items(), key=itemgetter(1))
        if (attract > 0 and forces[old_cluster] < attract)  or attract < 0:
            moves.append((k, new_cluster, attract))
    return moves

def independent_par(uf: Dict[Node, Cluster], g: Graph) -> bool:
    """Move independent nodes to their most attractive clusters.

    Parameters
    ---------
    uf: list of clusters
       clustering
    g: the graph of the tolerance relation

    Returns
    -------
     something modified?"""

    one_m = partial(_one_move, uf, g)
    gs = g.size//4
    parts = [g.nodes[:gs], g.nodes[gs:2*gs], g.nodes[2*gs:3*gs], g.nodes[3*gs:]]
    with mp.Pool(4) as p: # quad core
#        results = p.imap_unordered(one_m, g.nodes)
        results = p.map(one_m, parts)
    moves = [i for sl in results for i in sl] # párhuzamos verzió multiprocessing.map segítségével
    if not moves:
        return False
    c1 = g.conflicts(uf) # 4test
    # print("c1", c1, moves)
    forbidden = set()
    # print("moves:", moves)
    for n, new_cluster, attract in moves:
        old_cluster = uf[n]
        if attract < 0 and old_cluster not in forbidden:
            new_cluster = _escape(n, uf)
            forbidden.add(old_cluster)
            forbidden.add(new_cluster)
        else:
            # joined to a more attractive cluster
            if old_cluster not in forbidden and new_cluster not in forbidden:
                forbidden.add(old_cluster)
                forbidden.add(new_cluster)
                uf[n] = new_cluster
    c2 = g.conflicts(uf)  # 4test
    if c1 <= c2:
        print("before: {}, after: {}, moves:{}".format(c1, c2, moves))
        raise ValueError('sm-independent')
    return True

