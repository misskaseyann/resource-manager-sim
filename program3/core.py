import numpy as np
from program3.graph import Graph


class Core(object):
    """
    Core logic of simulation.
    """
    def __init__(self):
        """
        Initialize all class variables.
        """
        self.processes = 0
        self.resources = 0
        #  Holds tuples: (x,y,z) x = process num, y = request/release, z = resource num.
        self.steps = []
        #  Marks if resource is available or not.
        self.available = []
        #  Adjacency Matrices for hold and request edges.
        self.hold_edges = []
        self.request_edges = []
        #  Tracks where we are in the state of the system.
        self.state_num = 0
        #  Wait-for graph that we perform DFS for detecting deadlock cycles.
        self.graph = Graph()

    def read_file(self, fp):
        """
        Read in file, set number of processes, number of resources,
        and each step of the simulation state.
        :param fp: string file path to the file being parsed for data.
        """
        try:
            f = open(fp, 'r')
            file_arr = f.read().splitlines()
            #  Get number of processes.
            self.processes = int(file_arr.pop(0)[0])
            #  Get number of resources.
            self.resources = int(file_arr.pop(0)[0])
            print("\n%d processes and %d resources." % (self.processes, self.resources))
            #  Load each step.
            for line in file_arr:
                line_arr = line.split(' ')
                #  Get process num.
                p = int(line_arr[0].strip('p'))
                #  Get request/release.
                if line_arr[1] == 'requests':
                    re = 1
                else:
                    re = 0
                #  Get resource num.
                r = int(line_arr[2].strip('r'))
                #  Store as tuple in our steps.
                self.steps.append((p, re, r))
            print("%d total steps in simulation.\n" % len(self.steps))
        except IOError:
            print("Cannot find the file at", fp)

    def init_state(self):
        """
        Initialize state of system.
        """
        #  Number of available resources of each type.
        self.available = [1] * self.resources
        #  Processes owning a resource currently.
        self.connected_v = [None] * self.resources
        #  Edges representing process holding resource.
        self.hold_edges = [[0 for i in range(self.processes)] for j in range(self.resources)]
        #  Edges representing process requesting resource.
        self.request_edges = [[0 for i in range(self.processes)] for j in range(self.resources)]

    def deadlock_detection(self):
        """
        Detects if there is a cycle in the wait-for graph.
        :return: True if there is a deadlock.
        """
        recStack = set()
        visited = set()
        for node in self.graph:
            if node not in visited:
                if self.deadlock_detection_recur(node, visited, recStack):
                    print("Deadlock!")
                    return True
        print("No deadlock!")
        return False

    def deadlock_detection_recur(self, v, visited, recStack):
        """
        DFS algorithm for detecting cycles in the wait-for graph.
        :param v: current vertex.
        :param visited: set of already visited vertices.
        :param recStack: recursive stack of vertices being visited.
        :return: True if a cycle is detected.
        """
        if v in recStack:
            return True
        recStack.add(v)
        for dest in v.get_neighbors():
            if dest not in visited:
                if self.deadlock_detection_recur(dest, visited, recStack):
                    return True
        recStack.remove(v)
        visited.add(v)
        return False

    def step_forward(self):
        """
        Step forward the state.
        :return:
        """
        # TODO: Add check if there are no more states to move forward
        # TODO: Add step_backward
        print("\nStepping forward to state %d." % int(self.state_num + 1))
        #  Get process and resource involved.
        process = self.steps[self.state_num][0]
        resource = self.steps[self.state_num][2]
        #  Is this a request?
        if self.steps[self.state_num][1]:
            print("Process %d requests resource %d." % (process, resource))
            #  Is the resource not being used by a process?
            if self.available[resource] > 0:
                #  Mark in hold matrix the relationship between resource and process.
                self.hold_edges[resource][process] += 1
                #  Make resource unavailabe.
                self.available[resource] -= 1
                #  Store the process ID that holds the resource.
                self.connected_v[resource] = process
            else:
                #  Mark in request matrix the relationship between resource and process.
                self.request_edges[resource][process] += 1
                #  Add our process to the graph and make a directed edge.
                if process not in self.graph:
                    self.graph.add_vertex(process)
                if self.connected_v[resource] not in self.graph:
                    self.graph.add_vertex(self.connected_v[resource])
                if not self.graph.does_edge_exist(process, self.connected_v[resource]):
                    self.graph.add_edge(process, self.connected_v[resource])
                print("p{:d} --> p{:d}".format(process, self.connected_v[resource])) #  Protect against None type.
        else:
            print("Process %d releases resource %d." % (process, resource))
            #  Remove connection in hold matrix.
            self.hold_edges[resource][process] -= 1
            #  Does another process want this resource?
            if np.count_nonzero(self.request_edges[resource]) > 0:
                #  Get next process that wants the resource.
                new_process = self.request_edges[resource].index(1)
                #  Mark in hold matrix the relationship between resource and process.
                self.hold_edges[resource][new_process] += 1
                #  Store the process ID that holds the resource.
                self.connected_v[resource] = new_process
                #  Remove connection in request matrix.
                self.request_edges[resource][new_process] -= 1
                #  Delete edge if it exists.
                if self.graph.does_edge_exist(new_process, self.connected_v[resource]):
                    self.graph.delete_edge(new_process, self.connected_v[resource])
                print("Process %d now has resource %d." % (new_process, resource))
            else:
                print("Resource %d is now available." % resource)
                #  Mark resource as unowned by a process.
                self.available[resource] += 1
                #  Empty process that owned the resource previously.
                self.connected_v[resource] = None
        #  Advance the state.
        self.state_num += 1
