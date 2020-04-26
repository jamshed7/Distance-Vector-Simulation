import random

class Node():
    class_All_Nodes = {}


    @classmethod
    def addNode( cls, a_node ) :
        node_id = a_node.id
        if node_id in cls.class_All_Nodes :
            raise ValueError( f'Redeclaration of Node {node_id!r}.' )
        cls.class_All_Nodes[ node_id ] = a_node

    @classmethod
    def findNode( cls, node_id ) :
        return cls.class_All_Nodes.get( node_id, None )

    @classmethod
    def showAllNodes(cls):
        for item in cls.class_All_Nodes:
            print(f"Node - {item}")
            thisNode = cls.findNode(item)
            print(f"Node ID: {thisNode.id}")
            print(f"neighbors: {thisNode.displayNeighbors()}")

    @classmethod
    def breakNode(cls, broken_node_id):
        for x in Node.class_All_Nodes:
            node = cls.findNode(x)

            for node_id in self.distanceTable:
                if node.id == broken_node_id:
                    self.distanceTable[node_id] = 16
                else:
                    if node_id == broken_node_id:
                        self.distanceTable[broken_node_id] = 16


    def __init__(self, node_id, neighbors = []):
        self.id = node_id
        self.neighbors = neighbors

        self.distanceTable = {} # node_id: shortest distance
        # self.initialDistanceTable = {}
        self.routingTable = {} # destination node, route to node

        # add neighbors to distanceTable
        for neighbor, cost in neighbors:
            self.distanceTable[neighbor] = cost

        Node.addNode(self)


    def initializeDistanceTable(self):
        for node_id in Node.class_All_Nodes:
            if node_id not in self.distanceTable:
                self.distanceTable[node_id] = 16
            self.distanceTable[ self.id ] = 0


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

    def updateDistanceTable(self):

        for node_id, distance in self.distanceTable.items():
            if node_id == self.id:
                continue

            originalDistance = self.distanceTable[node_id]

            for neighbor_id, cost in self.neighbors:
                neighbor = Node.findNode(neighbor_id)
                if int(self.distanceTable[node_id]) > neighbor.getDistanceToNode(node_id) + int(cost):
                    self.distanceTable[node_id] = str( neighbor.getDistanceToNode(node_id) + int(cost) )
                    self.routingTable[node_id] = neighbor_id
                    #
                    neighbor.updateDistanceTable()


    def getDistanceToNode(self, a_node):
        return int( self.distanceTable[a_node] )



    def displayNeighbors(self):
        print(f"This is node {self.id}")
        if not self.neighbors:
            print("I do not have any neighbors.\n")
            return

        for neighbor, cost in self.neighbors:
            print(f"My neighbor {neighbor} is {cost} distance away.")
        print("\n")
