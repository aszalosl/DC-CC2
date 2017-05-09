"""Contraction for sparse graphs."""
from graph import Cluster, Node
from typing import Dict, Tuple, Set
from operator import itemgetter


def _change_one(uf: Dict[Node, Cluster], clusters: Tuple[Cluster,Cluster]) -> None:
    """Rewrite the clustering, according a given pairs.
    Modifies uf!

    Parameters
    ----------
      uf: list of clusters
          clusters of nodes
      clusters: a pair of cluster
    """
    frm, to = clusters
    for k, c in uf.items():
        if c == frm:
            uf[k] = to


def _change_all(uf: Dict[Node, Cluster], rewrite: Dict[Cluster, Cluster]) -> None:
    """Rewrite the clustering, according a given pairs.
    Modifies uf!

    Parameters
    ----------
    uf: list of clusters
        clusters of nodes
    rewrite: dict of clusters
        from-to pairs
    """
    for k, c in uf.items():
        if c in rewrite:
            uf[k] = rewrite[uf[k]]
    # print("uf/c: ", uf)


def independent(f: Dict[Tuple[Cluster, Cluster], int], uf: Dict[Node, Cluster]) -> bool:
    """Take all independent contractions, and execute them.
    Modifies uf.

    Parameters
    ----------
    f: dict of pair of clusters and ints
       forces between clusters (positive means contraction)
    uf: list of ints
       clusters

    Returns
    -------
    something modified?"""

    if f:
#        c1 = g.conflicts(uf)
        forbidden: Set[int] = set()             # is used yet
        change: Dict[Cluster, Cluster] = {}     # from-to pairs
        for k, v in f.items():
            x, y = k
            if v > 0 and x != y and x not in forbidden and y not in forbidden:
                change[y] = x
                forbidden.add(x)
                forbidden.add(y)               # mi lenne ha csak egyikre szurnenk?
        if change:
            _change_all(uf, change)
#            c2 = g.conflicts(uf)  # 4test
#            if c1 <= c2:
#                print("before: {}, after: {}".format(c1,c2))
#                raise ValueError('contract')
            return True
        return False

def one(f: Dict[Tuple[Cluster, Cluster], int], uf: Dict[Node, Cluster], g) -> bool:
    """Take the most effective contraction, and execute them.

    Parameter
    ---------
    f: dict of pair of clusters and ints
       forces between clusters (positive means contraction)
    uf: list of clusters
       clustering

    Returns
    -------
    something modified?"""

    if f:
#        c1 = g.conflicts(uf)  # 4test
        clusters, v = max(f.items(), key = itemgetter(1))
        if v <= 0:
            return False
        _change_one(uf, clusters)
#        c2 = g.conflicts(uf)  # 4test
#        if c1 <= c2:
#            print("before: {}, after: {}".format(c1,c2))
#            raise ValueError('sc.one')
        return True
    else:
        return False


def _myget(f: Dict[Tuple[Cluster, Cluster], int], x:Cluster, y:Cluster) -> int:
    """Get the value from a triangular sparse matrix.

    Parameters
    ----------
    f: triangular matrix as a dict of pairs of ints
    x,y: row and column id-s.

    Returns
    -------
    f of (x,y)"""

    if x > y:
        x, y = y, x
    v = f.get((x,y), 0)
    # print("({},{})={}".format(x,y,v))
    return v

def _myput(f: Dict[Tuple[Cluster, Cluster], int], x:Cluster, y:Cluster, v:int):
    """Put a value into a triangular matrix.

    Parameters
    ----------
    f:   triangular matrix as a dict of pairs of ints
    x,y: row and column id-s.
    v:   value"""

    if x > y:
        x, y = y, x
    f[x,y] = v
    # print(" {},{}->{}".format(x,y,v))

def _recalculate_force(f1: Dict[Tuple[Cluster, Cluster], int], \
                       clusters: Tuple[Cluster,Cluster]) \
                       -> Dict[Tuple[Cluster, Cluster], int]:
    """Recalculate forces between clusters.

    Parameters
    ----------
    f1:  forces between clusters
    frm, to: clusters are joined """
    # print("{}->{}, {}".format(frm, to, f1))
    frm, to = clusters
    f2 : Dict[Tuple[Cluster, Cluster], int] = {}
    for gs in f1:
        ga, gb = gs
        if (ga == to or ga == frm) and gb != frm and gb != to:
            _myput(f2, to, gb, _myget(f1, to, gb) + _myget(f1, frm, gb))

        if (gb == frm or gb == to) and ga != frm and ga != to:
            _myput(f2, ga, to, _myget(f1, to, ga) + _myget(f1, frm, ga))

        if ga != frm and gb != frm and ga != to and gb != to:
            f2[gs] = f1[gs]

    # f3 = g.calc_contract(uf)
    # if f3 != f2:
    #     print("Our:", f2)
    #     print("Official:", f3)
    #     raise ValueError('recalculate force')
    # print(f2)
    return f2


def iterate_min(f: Dict[Tuple[Cluster, Cluster], int], uf: Dict[Node, Cluster], g) -> bool:
    """Take the most effective contraction, and execute it. Next repeat.
    minimal recalculation for f - erronomous

    Parameters
    ---------
    f: dict of pair of clusters and ints
       forces between clusters (positive means contraction)
    uf: list of clusters
       clustering

    Returns
    -------
    something modified?"""

    if f:
#        c0 = g.conflicts(uf)
        clusters, m = max(f.items(), key = itemgetter(1))
        if m <= 0:
            return False
        while m > 0:
#            c1 = g.conflicts(uf)
            # execute the contraction
            _change_one(uf, clusters)
#            c2 = g.conflicts(uf)
#            if c1 < c2:
#                print("original: {} before: {}, after: {}, suggest: {}".format(c0, c1, c2, m))
#                print("conflicts after contract: ", g.conflicts(uf))
#                print("Our:", f1)
#                f3 = g.calc_contract(uf)
#                print("Official:", f3)
#                raise ValueError('contract')
            f = _recalculate_force(f, clusters)
            if not f:
                return True
            clusters, m = max(f.items(), key = itemgetter(1))
        return True
    else:
        return False


