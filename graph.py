"""Generate random graphs."""

import random
from typing import Dict, Tuple, Set, List
Node = int
Cluster = int
Sign = int
Edge = Tuple[Node, Node, Sign]
Neighbourhood = Set[Node]

def _sign(q: float) -> Sign:
    """The edges of the graph is signed, this function returns a random sign.

    Parameter
    ---------
      q: float
         the probability that the sign became +

    -------
    Returns
      +1 (with probability q) or -1
    """

    p = random.random()
    if p < q:
        return 1
    else:
        return -1


class Graph(object):
    """This abstract class contains the methods are common at both type of
    random graphs.

    Hidden attributes
    ----------
     size: int
           number of nodes in the graph + 1
     edges: list of edges (two nodes and a sign)
           all the edges of the graph
     nodes: list of nodes
     neighbours: list of set of nodes
           the set of adjacent nodes for all the nodes,
           for the sake of faster processing
    """

    def __init__(self, size: int) -> None:
        """Store the size and initialize an empty list for edges."""
        self.__size: int = size
        self.__edges: List[Edge] = []
        self.__nodes: List[Node] = []

    @property
    def size(self) -> int:
        """A typical getter."""
        return self.__size

    @property
    def edges(self):
        """A typical getter."""
        return self.__edges

    @property
    def nodes(self):
        """A typical getter."""
        return self.__nodes

    @property
    def neighbours(self):
        """A typical getter."""
        return self.__neighbours

    def add_edge(self, edge: Edge):
        """Add a new edge to the list of edges."""
        self.__edges.append(edge)

    def _calculate_neighbours(self):
        """Generate the neigbours for all nodes based on edges."""
        self.__neighbours: Dict[Node, Neighbourhood] = {n: set() for n in self.__nodes}
        for i, j, w in self.__edges:
            # we store the id of the adjancent node and the sign of the edge
            # as we have no +0 and -0, we increment the id by 1
            if w < 0:
                self.__neighbours[i].add(-j)
                self.__neighbours[j].add(-i)
            else:
                self.__neighbours[i].add(j)
                self.__neighbours[j].add(i)

    def conflicts(self, uf: Dict[Node, Cluster]) -> int:
        """An edge have a conflict:
         a) their nodes are in the same cluster, but the sign is -
         b) their nodes are in different clusters, but the sign is +

         Parameter
         ---------
          uf: dict of cluster id'
              gives the cluster for each nodes.

         Returns
         -------
         Number of conflicts.
         """
        counter = 0
        for i, j, v in self.__edges:
            if (uf[i] == uf[j] and v == -1) or\
               (uf[i] != uf[j] and v == 1):
                counter += 1
        return counter

    def recolor(self, count: int) -> None:
        """Randomly change signs of some edges.

        Parameter
        ---------
         count: int
                number of edges change their sign.
        """
        minus = [(i, j) for i, j, v in self.__edges if v < 0]
        if len(minus) > count:
            to_change = random.sample(minus, count)
        else:
            to_change = minus
        for c, x in enumerate(self.__edges):
            i, j, v = x
            if (i, j) in to_change:
                self.__edges[c] = (i, j, 1)
        self._calculate_neighbours()

    def q_rate(self) -> float:
        """Calculate the q rate parameter of the graph.

        Returns
        -------
         ratio of positive edges."""
        positive = 0
        negative = 0
        for i, j, v in self.__edges:
            if v > 0:
                positive += 1
            if v < 0:
                negative += 1
        return positive/(positive+negative)

    def calc_contract(self, uf: Dict[Node, Cluster]) -> Dict[Tuple[Cluster,Cluster], int]:
        """Calculates the forces between clusters.

        Parameter
        ---------
         uf: dict of cluster id's"
              gives the cluster for each nodes.

        Returns
        -------
         a dict store the forces (attraction/repulsion) between clusters.
        """
        forces: Dict[Tuple[Cluster, Cluster], int] = {}
        for i, j, v in self.__edges:
            gi = uf[i]  # take the cluster of the node
            gj = uf[j]
            # +/- denotes attraction/repulsion
            # we need to sum them.
            if gi > gj:
                gi, gj = gj, gi
            if gi < gj:
                # the inner force not interesting
                forces[(gi, gj)] = forces.get((gi, gj), 0) + v
        # print("original forces:", forces)
        return forces


    def calc_attract(self, i: Node, uf: Dict[Node, Cluster]) -> Dict[Cluster, int]:
        """Calculate the forces attracts node i.

        Parameters
        ----------
         i:  int (node id - start)
             the node which is attracted
         uf: dict of cluster id's"
             gives the cluster for each nodes.
         lower, upper: clusters
             limits for attraction

        Returns
        -------
         a dict store the forces attract node i
        """
        forces: Dict[Cluster, int] = {uf[i]:0}
        # print("neighbours for {}:{}".format(i,self.__neighbours[i]))
        for j in self.__neighbours[i]:
            if j < 0:
                group_j = uf[-j]
                amount = -1
            else:
                group_j = uf[j]
                amount = 1
            forces[group_j] = forces.get(group_j, 0) + amount
        # print("forces for {}:{}".format(i,forces))
        return forces


class FixedGraph(Graph):
    """Graph given with its edges."""
    def __init__(self, nodes, edges):
        """Build by its edges."""
        super().__init__(len(nodes))
        self._Graph__edges = edges
        self._Graph__nodes = nodes
        self._calculate_neighbours()

class ERGraph(Graph):
    """Erdős-Rényi random graph.
    see: https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model"""

    def __init__(self, N:int, p:float, q:float) -> None:
        """Generate it!

        Parameters
        ----------
         N: int
            number of nodes
         p: float
            probability to have an edge between two given nodes
         q: float
            rate of positive edges

        Returns
        -------
         the graph
        """
        super().__init__(N)
        for i in range(1,N):
            for j in range(i+1, N+1):
                if random.random() < p:
                    self.add_edge((i, j, _sign(q)))
        self._Graph__nodes = [i for i in range(1,N+1)]
        self._calculate_neighbours()

class BAGraph(Graph):
    """Barabási-Albert random graph.
    see: https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model
    """

    def __init__(self, N:int, q:float, m0:int =3, m:int =2) -> None:
        """Generate it!

        Parameters
        ----------
         N: int
            number of nodes
         q: float
            rate of positive edges
         m0: int
            size of the core (complete subgraph)
         m: int
            number of connections of a newcomer

        Returns
        -------
         the graph
        """
        super().__init__(N)
        total_degree = 0
        degree_list: List[int] = [0]

        shuffling = list(range(1,N+1))
        random.shuffle(shuffling)
        shuffling = [0] + shuffling
        for i in range(1,m0+1):                 # core -- a complete graph
            for j in range(i+1,m0+1):
                si = shuffling[i]
                sj = shuffling[j]
                self.add_edge((si, sj, _sign(q)))
            degree_list.append(m0-1)
        total_degree = m0*(m0-1)

        for current_node in range(m0+1, N+1):
            nodes_to_connected: List[int] = []
            # print("dl b:", degree_list)
            while len(nodes_to_connected) < m:
                # connect by preference
                rand = random.randint(1, total_degree)
                # print("r", rand)
                sum = 0
                for i in range(1,len(degree_list)):
                    sum += degree_list[i]
                    if rand <= sum:
                        node_to_connect = i
                        break
                if node_to_connect in nodes_to_connected:
                    continue
                else:
                    nodes_to_connected.append(node_to_connect)
                    self.add_edge((shuffling[current_node], shuffling[i], \
                        _sign(q)))
                    degree_list[node_to_connect] += 1

            degree_list.append(m)
            total_degree += m * 2
            # print("dl a:", degree_list)
        self._Graph__nodes = [i for i in range(1,N+1)]
        self._calculate_neighbours()
        # print(self.edges)

if __name__ == "__main__":
    a = BAGraph(12, 0.1)
    print("BA12 edges: ", a.edges)
    print("BA12 q: ", a.q_rate())
    print("BA12 neighbours: ", a.neighbours)
    # a.recolor(8)
    # print(a.get_edges(), a.q_rate())
    r = ERGraph(12, 0.2, 0.1)
    print("ER12 edges: ", r.edges)
    print("ER12 q: ", r.q_rate())
    print("ER12 neighbours: ", r.neighbours)
