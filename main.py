import sys
import subprocess
import platform
from Node import Node

allNodeIds = []

def _main( fileName ) :

    topology = {}
    # allNodeIds = set()
    # allNodeIds = []

    with open( fileName, 'r' ) as fp :
        lines = fp.read().replace('\r', '' ).split( '\n' )
        for line in lines:
            if ( line == '' ) : #ignore blank lines
                continue

            from_, to_, cost = line.split()

            # create a dictionary to hold node and corresponding neighbor data
            if from_ not in topology:
                topology[from_] = [ (to_, cost) ]
            else:
                topology[from_].append( (to_,cost) )

            if to_ not in topology:
                topology[to_] = [ (from_, cost) ]
            else:
                topology[to_].append( (from_,cost) )


    # Initialize nodes; Add known cost of neighbors
    for node_id, neighbors in topology.items():
        # add node id's to list of all nodes
        if node_id not in allNodeIds:
            allNodeIds.append(node_id)
        newNode = Node(node_id, neighbors)

    # sort list of nodes
    allNodeIds.sort()

    # initialize distance table for all nodes
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        node.initializeDistanceTable()

    # Debug
    # for node_id, neighbors in topology.items():
    #     print(f"I am node {node_id}")
    #     print(f"My neighbors are: {neighbors}")


    # # # DEBUG: Show all nodes
    # Node.showAllNodes()

    print("( 1 ) Auto-mode")
    print("( 2 ) For step-mode")

    while True:
        modeSelect = input("Enter number to select mode.\n")

        if modeSelect == '1':
            autoMode()
            break
        elif modeSelect == '2':
            stepMode()
            break
        else:
            print("Error: Please enter a valid number. \nEnter '1' for auto-mode, or '2' for step-by-step mode.")


    # endLoop = False
    # iteration = 0
    #
    # while (not endLoop):
    #     iteration +=1
    #     print("===================================")
    #     print(f"Iteration {iteration}")
    #     print("===================================")
    #
    #     # show distances from each node
    #     for node_id in allNodeIds:
    #         node = Node.findNode(node_id)
    #         node.displayDistanceTable()
    #
    #     userInput = input("\nType \'quit\' to exit or press return key to keep iterating:   ")
    #
    #     if userInput == 'quit':
    #         break
    #     else:
    #         curr_node = str(iteration % len(allNodeIds) )
    #         if( curr_node == '0'):
    #             curr_node = str( len(allNodeIds) )
    #
    #         print (f"\nCurrent node being updated is Node - {curr_node}\n")
    #         node = Node.findNode( curr_node )
    #         node.updateDistanceTable()


def autoMode():
    print("Auto Mode")

def stepMode():
    endLoop = False
    iteration = 0

    while (not endLoop):
        iteration +=1
        print("===================================")
        print(f"Iteration {iteration}")
        print("===================================")

        # show distances from each node
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            node.displayDistanceTable()

        userInput = input("\nType \'quit\' to exit or press return key to keep iterating:   ")

        if userInput == 'quit':
            break
        else:
            curr_node = str(iteration % len(allNodeIds) )
            if( curr_node == '0'):
                curr_node = str( len(allNodeIds) )

            print (f"\nCurrent node being updated is Node - {curr_node}\n")
            node = Node.findNode( curr_node )
            node.updateDistanceTable()




# function to clear screen
def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

if __name__ == '__main__' :
  if len( sys.argv ) != 2 :
    raise ValueError( 'Please include input file name in command line arguments.' )

  _main( sys.argv[1] )
