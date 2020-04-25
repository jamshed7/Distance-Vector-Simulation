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



    def __init__(self, node_id, neighbors = []):
        self.id = node_id
        self.neighbors = neighbors

        self.distanceTable = {} # node_id: shortest distance

        # add neighbors to distanceTable
        for neighbor, cost in neighbors:
            self.distanceTable[neighbor] = cost

        Node.addNode(self)

    def updateDistanceTable(self):

        for neighbor_id, cost in self.neighbors:
            # get neighbor object
            neighbor = Node.findNode(neighbor_id)

            for node, distance in self.distanceTable.items():
                originalDistance = self.distanceTable[node]
                self.distanceTable[node] = str( min( int( self.distanceTable[node] ), neighbor.getDistanceToNode(node) + int(cost) ) )

                # if self.distanceTable[node] != originalDistance:
                #     neighbor.updateDistanceTable()


    def getDistanceToNode(self, a_node):
        return int( self.distanceTable[a_node] ) # convert to int




    def initializeDistanceTable(self):
        for node_id in Node.class_All_Nodes:
            if node_id not in self.distanceTable:
                self.distanceTable[node_id] = 16
            self.distanceTable[ self.id ] = 0


    def displayDistanceTable(self):
        print(f"Distance Vector Table for Node: {self.id}")
        print("===================================")

        for node_id in sorted(self.distanceTable):
            print(f"From Node: {self.id} To Node: {node_id} Shortest Distance: {self.distanceTable[node_id]}")

        print("\n")



    def displayNeighbors(self):
        print(f"This is node {self.id}")
        if not self.neighbors:
            print("I do not have any neighbors.\n")
            return

        for neighbor, cost in self.neighbors:
            print(f"My neighbor {neighbor} is {cost} distance away.")
        print("\n")
