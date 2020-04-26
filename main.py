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
        node.initializeRoutingTable()  ## new

    print("\nWelcome, this program will simulate the Distance-Vector Routing Protocol.\nPlease select your desired run mode.\n")
    print("( 1 ) Auto-mode")
    print("( 2 ) Step-mode")

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




def autoMode():
    print("\nPerforming simulation in Auto Mode")

    loopCount = 1
    curr_state = 'default'
    last_state = 'default'

    while True:
        # curr_node = str( loopCount % len(allNodeIds) )
        # if( curr_node == '0'):
        #     curr_node = str( len(allNodeIds) )
        curr_node = '1'
        node = Node.findNode( curr_node )
        node.updateDistanceTable()

        curr_state = ''
        # show distances from each node
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            curr_state += node.displayTables()
            curr_state += '\n'

        if curr_state != last_state:
            last_state = curr_state
            loopCount +=1
        else:
            break

    print("===================================")
    print(f"Stable State Reached after {loopCount} iterations.")
    print("===================================")

    stable_state = ''
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        stable_state += node.displayTables()
        stable_state += '\n'
    print(stable_state)



def stepMode():
    endLoop = False
    iteration = 0

    curr_state = 'default'
    last_state = 'default'

    while (not endLoop):
        print("===================================")
        if iteration == 0:
            print("Initial State")
        else:
            print(f"Iteration {iteration}")
        print("===================================")

        curr_state = ''
        # show distances from each node
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            curr_state += node.displayTables()
            curr_state += '\n'

        if curr_state != last_state:
            print( curr_state )
            last_state = curr_state
            userInput = input("\nType \'quit\' to exit or press return key to keep iterating:\n")
        else:
            print("===================================")
            print("Stable State has been reached!")
            print("===================================")

            userInput = input("\nType \'quit\' to exit or type 'break [node]' to simulate broken router:\n")



        if userInput == 'quit':
            break
        else:
            iteration +=1
            # curr_node = str(iteration % len(allNodeIds) )
            # if( curr_node == '0'):
            #     curr_node = str( len(allNodeIds) )
            curr_node = '1'

            # print (f"\nCurrent node being updated is Node - {curr_node}\n")
            node = Node.findNode( curr_node )
            node.updateDistanceTable()




# function to clear screen
def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

if __name__ == '__main__' :
  if len( sys.argv ) != 2 :
    raise ValueError( 'Please include input file name in command line arguments.' )

  _main( sys.argv[1] )
