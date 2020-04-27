# Name: Jamshed Jahangir
# UTA ID: 1001366821
# NetID: jxj6821

import sys
import subprocess
import platform
from Node import Node

allNodeIds = [] # node ids are numbers representing a node
                # this list holds all the node ids
def _main( fileName ) :
    # open the fileName that is outlined in the command

    topology = {} # a dictionary to hold a node and corresponding neighbor data

    with open( fileName, 'r' ) as fp :
        lines = fp.read().replace('\r', '' ).split( '\n' )
        for line in lines:
            if ( line == '' ) : #ignore blank lines
                continue
            # split each line and store them as follows:
            from_, to_, cost = line.split()

            # populate the topology dictionary with network information from the file
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
        newNode = Node(node_id, neighbors) # create new node

    # sort list of node ids
    allNodeIds.sort()
    print("# DEBUG: ")
    print(topology)
    # initialize distance and routing table for all nodes
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        node.initializeDistanceTable()
        node.initializeRoutingTable()

    # print welcome prompt
    print("\nWelcome, this program will simulate the Distance-Vector Routing Protocol.\nPlease select your desired run mode.\n")
    print("( 1 ) Auto-mode")
    print("( 2 ) Step-mode")

    # start INFINITE loop; wait until valid input is received from user
    while True:
        modeSelect = input("Enter number to select mode.\n")
        # if user selects option 1 -> run autoMode
        if modeSelect == '1':
            autoMode()
            break
        # if user selects option 2 -> run stepMode
        elif modeSelect == '2':
            stepMode()
            break
        else: # invalid input received
            print("Error: Please enter a valid number. \nEnter '1' for auto-mode, or '2' for step-by-step mode.")




def autoMode():
    print("\nPerforming simulation in Auto Mode")

    loopCount = 1
    curr_state = 'default' # variable to keep track of the last state of the network
    last_state = 'default' # variable to store current state of the network

    # keep looping until stable state is reached
    while True:
        # select arbitrary node and make it update its link state table
        # curr_node = allNodeIds[0]
        curr_node = '1'
        node = Node.findNode( curr_node )
        node.updateDistanceTable()

        curr_state = ''
        # get link state tables from each node and store it in curr_state
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            curr_state += node.displayTables()
            curr_state += '\n'

        # if curr_state is different from last state then new changes have occured
        #       increase loop count and restart
        if curr_state != last_state:
            last_state = curr_state
            loopCount +=1
        else: # current state == last state i.e. no changes -> stable state reached
            break

    print("===================================")
    print(f"Stable State Reached after {loopCount} iterations.")
    print("===================================")

    stable_state = ''
    # gather table data again from all nodes and store in stable_state
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        stable_state += node.displayTables()
        stable_state += '\n'
    print(stable_state) # print all tables



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
        # get link state tables from each node and store it in curr_state
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            curr_state += node.displayTables()
            curr_state += '\n'
        # if curr_state is different from last state then new changes have occured; show current table state
        if curr_state != last_state:
            print( curr_state )
            last_state = curr_state

        else:
            print("===================================")
            print("Stable State has been reached!")
            print("===================================")
            # print("To update link information, type 'update link'\n")

        # wait for user input
        print("\nTo update link information, type 'update link'\n")
        userInput = input("\nType 'quit' to exit or press return key to keep iterating.\n")

        # user can choose to quit, continue iterating, or change a link cost
        if userInput == 'quit':
            break

        if userInput == 'update link':
            # if user decides to update a link, get new link information from user
            print("Please type in updated link information\n")
            print("Format-> [node] [node] [distance]\n")
            newLink = input()
            node_1_id, node_2_id, distance = newLink.split()
            # call the class method updateLink() to implement the changes
            Node.updateLink(node_1_id, node_2_id, distance)
            last_state = ''
            continue


        iteration +=1
        curr_node = allNodeIds[0]
        # select arbitrary node and make it update its link state table
        node = Node.findNode( curr_node )
        node.updateDistanceTable()




# function to clear screen
def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

if __name__ == '__main__' :
  if len( sys.argv ) != 2 : # Handle situation where user does not include input file name
    raise ValueError( 'Please include input file name in command line arguments.' )

  _main( sys.argv[1] )
