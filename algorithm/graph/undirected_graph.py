from algorithm.sort.heap import PriorityQueue


class UnconnectedError(Exception):
    pass


class Vertex(object):
    def __init__(self, key):
        self._key = key
        self._edges = list()

    def get_adjacencies_and_weights(self):
        pass


class Edge(object):
    def __init__(self, vertex1, vertex2, weight):
        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self.weight = weight

    def is_one_endpoint(self, vertex):
        return vertex is self._vertex1 or vertex is self._vertex2

    def get_endpoints(self):
        return (self._vertex1, self._vertex2)


class UndirectedGraph(object):
    def __init__(self):
        self._vertexes = {}
        self._edges = list()

    def add_vertex(self, key):
        pass

    def add_edge(self, key1, key2, weight=None):
        pass

    def get_edge(self, key1, key2):
        pass

    def _init_kruskal(self):
        # each vertex as a set
        self._sets = set()
        self._mst_edges = list()
        for each in self._vertexes.values():
            self._sets.add(set(each))

    def _find_set(self, vertex):
        for each in self._sets:
            if vertex in each:
                return each
            else:
                raise KeyError('Failed to find the set that contains: %s' % vertex)

    def _union_the_sets_of_edge_connected(self, edge):
        endpoints = edge.get_endpoints()
        set0 = self._find_set(endpoints[0])
        set1 = self._find_set(endpoints[1])
        if set0 is not set1:
            self._sets.remove(set0)
            self._sets.remove(set1)
            self._sets.add(set0.union(set1))
            self._mst_edges.append(edge)

    def mst_kruskal(self):
        # all edges in none-increasing order
        self._init_kruskal()
        for edge in sorted(self._edges, key=lambda x: x.weight):
            self._union_the_sets_of_edge_connected(edge)
            if len(self._sets) == 1:
                break
        else:
            raise UnconnectedError('Failed to calculate MST')

        return self._mst_edges

    def _init_prim(self):
        for vertex in self._vertexes.values():
            vertex.distance = float('inf')
            vertex.pre = None

    def mst_prim(self, start_key=None):
        self._init_prim()
        if start_key is None:
            strart_vertex = self._vertexes.values()[0]
        else:
            strart_vertex = self._vertexes[start_key]
        strart_vertex.distance = 0
        pq = PriorityQueue(((each.distance, each) for each in self._vertexes.values()), key=lambda x: x.distance)
        while not pq.empty():
            cur_vertex = pq.pop()
            for vertex, weight in cur_vertex.get_adjacencies_and_weights():
              if (vertex.distance, vertex) in pq and weight < vertex.getDistance():
                  vertex.distance = weight
                  vertex.pre = cur_vertex
                  pq.decrease_key(vertex, weight)


if __name__ == '__main__':
    pass
