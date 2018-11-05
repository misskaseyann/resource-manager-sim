class Vertex(object):
    """
    Vertex object with key and value pairs.
    Modified from:
    https://www.sanfoundry.com/python-program-find-directed-graph-contains-cycle-using-dfs/
    """
    def __init__(self, key):
        self.key = key
        self.points_to = {}

    def get_key(self):
        return self.key

    def add_neighbor(self, dest, weight):
        self.points_to[dest] = weight

    def delete_neighbor(self, dest):
        del self.points_to[dest]

    def get_neighbors(self):
        return self.points_to.keys()

    def get_weight(self, dest):
        return self.points_to[dest]

    def does_it_point_to(self, dest):
        return dest in self.points_to
