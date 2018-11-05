import numpy as np
import copy
from program3.graph import Graph


class Core(object):
    def __init__(self):
        """
        Initialize all class variables.
        """
        self.processes = 0
        self.resources = 0
        #  Holds tuples: (x,y,z) x = process num, y = request/release, z = resource num.
        self.steps = []
        # Algorithm data structures.
        self.available = []
        self.nodes = []
        self.hold_edges = []
        self.request_edges = []
        self.state_num = 0

        self.graph = Graph()
        self.vertices = 0


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
            print("%d total steps in simulation." % len(self.steps))
        except IOError:
            print("Cannot find the file at", fp)

    def init_state(self):
        """
        Initialize state.
        """
        #  Number of available resources of each type.
        self.available = [1] * self.resources
        self.connected_v = [None] * self.resources
        #  Total nodes in the graph.
        for i in range(self.processes):
            self.nodes.append('p' + str(i))
        for i in range(self.resources):
            self.nodes.append('r' + str(i))
        #  Edges representing process holding resource.
        self.hold_edges = [[0 for i in range(self.processes)] for j in range(self.resources)]
        #  Edges representing process requesting resource.
        self.request_edges = [[0 for i in range(self.processes)] for j in range(self.resources)]

        self.vertices = self.processes

    def deadlock_detection(self):
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

    # def deadlock_detection(self):
    #     """
    #     Detects if there is deadlock in the current state.
    #     This is sing-instance resource deadlock detection only.
    #     Referenced from: http://www.embeddedlinux.org.cn/rtconforembsys/5107final/LiB0100.html
    #     :return: True if deadlocked.
    #     """
    #     print("\n------Checking State %d for Deadlock-------\n" % self.state_num)
    #     #  Copy our own node list to be able to manipulate.
    #     n = self.nodes.copy()
    #     #  Empty list for graph traversal.
    #     l = []
    #     #  Hold edges.
    #     h = copy.deepcopy(self.hold_edges)
    #     print(h)
    #     #  Request edges.
    #     r = copy.deepcopy(self.request_edges)
    #     print(r)
    #
    #     #  Add node to list.
    #     l.append(n.pop(0))
    #     #  For each node in N
    #     while len(n) >= 0 and len(l) > 0:
    #         print(l)
    #         print(n)
    #         #  Check if node is in list twice.
    #         element = l[-1]
    #         print(element)
    #         if l.count(element) > 1:
    #             print("Deadlock!")
    #             return True
    #         #  Pick arc and follow it to next node.
    #         if element[0] == 'p' and np.count_nonzero(h[int(element[1])]) > 0:
    #             l.append(n.pop(n.index('r' + str(h[int(element[1])].index(1))))) # TODO clean up variables
    #             print(element + " <-- " + l[len(l) - 1])
    #             #  Mark arc as visited.
    #             h[int(element[1])][h[int(element[1])].index(1)] = 0
    #         elif element[0] == 'r' and np.count_nonzero(r[int(element[1])]) > 0:
    #             print(r)
    #             l.append(n.pop(n.index('p' + str(r[int(element[1])].index(1))))) # TODO clean up variables
    #             print(element + " --> " + l[len(l) - 1])
    #             #  Mark arc as visited.
    #             r[int(element[1])][r[int(element[1])].index(1)] = 0
    #         else:
    #             # all arcs traversed.
    #             print("Else statement")
    #             print(l)
    #             l.pop(len(l) - 1)
    #             if not len(l) and len(n) > 0:
    #                 l.append(n.pop(0))
    #     print("No deadlock!")
    #     return False

    def step_forward(self):
        """
        Step forward the state.
        :return:
        """
        print("\nStepping forward to state %d." % int(self.state_num + 1))
        process = self.steps[self.state_num][0]
        resource = self.steps[self.state_num][2]
        if self.steps[self.state_num][1]:
            print("Process %d requests resource %d." % (process, resource))
            if self.available[resource] > 0:
                self.hold_edges[resource][process] += 1
                self.available[resource] -= 1
                self.connected_v[resource] = process
            else:
                self.request_edges[resource][process] += 1
                print("here")
                if process not in self.graph:
                    self.graph.add_vertex(process)
                if self.connected_v[resource] not in self.graph:
                    self.graph.add_vertex(self.connected_v[resource])
                if not self.graph.does_edge_exist(process, self.connected_v[resource]):
                    self.graph.add_edge(process, self.connected_v[resource])
                print("p%d --> p%d" % (process, self.connected_v[resource]))
                #self.graph[process].append(self.connected_v[resource])
        else:
            print("Process %d releases resource %d." % (process, resource))
            self.hold_edges[resource][process] -= 1
            # Does another process want this resource?
            if np.count_nonzero(self.request_edges[resource]) > 0:
                new_process = self.request_edges[resource].index(1)

                self.hold_edges[resource][new_process] += 1
                self.connected_v[resource] = new_process

                self.request_edges[resource][new_process] -= 1

                if self.graph.does_edge_exist(new_process, self.connected_v[resource]):
                    self.graph.delete_edge(new_process, self.connected_v[resource])
                #elf.graph[new_process].remove(self.connected_v[resource])

                print("Process %d now has resource %d." % (new_process, resource))
            else:
                print("Resource %d is now available." % resource)
                self.available[resource] += 1
                self.connected_v[resource] = None

        # MIGHT NEED TO MOVE THIS!!!!!!!
        self.state_num += 1
