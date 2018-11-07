from program3.wait_for_graph.vertex import Vertex


class Graph(object):
    """
    Directed wait_for_graph for use as Wait-for wait_for_graph.
    Modified from:
    https://www.sanfoundry.com/python-program-find-directed-graph-contains-cycle-using-dfs/
    """
    def __init__(self):
        """
        Initialize vertex dict.
        """
        self.vertices = {}

    def add_vertex(self, key):
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def delete_vertex(self, key):
        self.vertices.pop(key, None)

    def get_vertex(self, key):
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, src_key, dest_key, weight=1):
        self.vertices[src_key].add_neighbor(self.vertices[dest_key], weight)

    def delete_edge(self, src_key, dest_key):
        self.vertices[src_key].delete_neighbor(self.vertices[dest_key])

    def does_edge_exist(self, src_key, dest_key):
        try:
            return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])
        except Exception:
            return False


    def __iter__(self):
        return iter(self.vertices.values())
