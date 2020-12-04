# Initialize the class

class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost


def neighborInClose(neighbor, closed):
    for node in closed:
        if (neighbor.position == node.position): return True
    return False


def astar_search(map, start, end):		#sửa lại chỗ này
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)        #sửa lại chỗ này
    goal_node = Node(end, None)				#sửa lại chỗ này
    # Add the start node
    open.append(start_node)


    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open = sorted(open, key=lambda x: x.f)

        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node.position == goal_node.position:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            # path.append(start)
            # Return reversed path
            return path[::-1]
        # Unzip the current node position
        (x, y) = current_node.position
        # Get neighbors

        neighbors = [(x , y+1), (x+1, y ),
                     (x-1, y), (x, y-1),
                     (x-1, y-1), (x - 1, y +1),
                     (x+1, y - 1), (x +1, y + 1)]
        # Loop neighbors
        for next in neighbors:

            # Get value from map
            if (next[0] >= 0 and next[0] < 15 and next[1]>= 0 and next[1] < 15):
                map_value = map[next[0]][next[1]]		#sửa lại chỗ này
            else : continue
            # Check if the node is a wall
            if (map_value == 1 ):
                continue
            # Create a neighbor node
            neighbor = Node(next, current_node)
            # Check if the neighbor is in the closed list
            if (neighborInClose(neighbor, closed)):
                continue
            # Generate heuristics (Manhattan distance)
            neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                neighbor.position[1] - start_node.position[1])
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                neighbor.position[1] - goal_node.position[1])
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor.position == node.position and neighbor.f >= node.f):
            return False
    return True

