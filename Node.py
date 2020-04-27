# Author: Jamshed Jahangir
# Last updated: April 26, 2020

class Node():
    # dictionary that contains all the nodes
    class_All_Nodes = {}    # node id : node object


    # a class method to add a node to our class_All_Nodes dictionary
    @classmethod
    def addNode( cls, a_node ) :
        node_id = a_node.id
        if node_id in cls.class_All_Nodes :
            raise ValueError( f'Redeclaration of Node {node_id!r}.' )
        cls.class_All_Nodes[ node_id ] = a_node

    # a class method to find a node object given its id
    @classmethod
    def findNode( cls, node_id ) :
        return cls.class_All_Nodes.get( node_id, None )

    # a class method to update the link cost between 2 existing nodes
    @classmethod
    def updateLink(cls, node_1_id, node_2_id, distance):
        node1 = cls.findNode(node_1_id)
        node2 = cls.findNode(node_2_id)

        node1.distanceTable[node_2_id] = distance
        node2.distanceTable[node_1_id] = distance
        print("-----------------------------------")
        print(f"Link between Node {node_1_id} and Node {node_2_id} updated. New link cost = {distance}.")
        print("-----------------------------------")


    # init function to setup a node object
    def __init__(self, node_id, neighbors = []):
        self.id = node_id
        self.neighbors = neighbors #list of tuples; tuple format -> (neighbor, distance to neighbor)
        self.distanceTable = {} # Key - node_id: Value - shortest distance to that node
        self.routingTable = {} # Key - destination node: Value - route to node

        # add neighbors to distanceTable
        for neighbor, cost in neighbors:
            self.distanceTable[neighbor] = cost

        Node.addNode(self)  # add newly created Node object to class_All_Nodes dictionary

    # function to initialize the distance table
    #       if a node is not already added (as a neighbor), then set the distance to that node as INFINITY
    #       if a node is itself, distance to self is 0
    def initializeDistanceTable(self):
        for node_id in Node.class_All_Nodes:
            if node_id not in self.distanceTable:
                self.distanceTable[node_id] = 16
            self.distanceTable[ self.id ] = 0


    # function to initialize routing table
    #       if destination node is a neighbor, route directly to neighbor
    #       if destination node is not a neighbor, just route to first available neighbor (Initial state)
    def initializeRoutingTable(self):
        for node_id in Node.class_All_Nodes:
            # if destination node is also neighbor node, send directly
            if self.isNeighbor(node_id):
                self.routingTable[node_id] = node_id
            elif node_id == self.id:
                self.routingTable[node_id] = self.id
            # else just send to the the first neighbor
            else:
                self.routingTable[node_id], _ = self.neighbors[0]

    # function that returns the link state table for a given Node in string format
    def displayTables(self):
        res = ""
        res += f"Node {self.id}\n"
        res += "-----------------------------------\n"
        for node_id in sorted(self.distanceTable):
            res += f"Destination Node: {node_id}     Shortest Distance: {self.distanceTable[node_id]}    Route to Node: {self.routingTable[node_id]}\n"
        res += "-----------------------------------"
        return res


    # check if a given node id is my neighbor
    def isNeighbor(self, a_node_id):
        for neighbor_id, cost in self.neighbors:
            if a_node_id == neighbor_id:
                return True
        return False

    # this is the heart of our program
    # function that implements the Bellman Ford algorithm
    #       for every node in the topology, distance to that node is obtained as follows:
    #           distance to destination node = minimum of (my current distance to that node,
    #                                               my neighbor's distance to the destination node + my cost to reach my neighbor)
    #
    def updateDistanceTable(self):
        for node_id, distance in self.distanceTable.items():
            if node_id == self.id:
                continue

            originalDistance = self.distanceTable[node_id]

            for neighbor_id, cost in self.neighbors:
                neighbor = Node.findNode(neighbor_id)
                if int( self.distanceTable[node_id] ) > int( neighbor.distanceTable[node_id] ) + int(cost):
                    self.distanceTable[node_id] = str( int( neighbor.distanceTable[node_id] ) + int(cost) )
                    self.routingTable[node_id] = neighbor_id
                    neighbor.updateDistanceTable()
