import copy

class node:
    # a node consists of a state, parent node, and g(n), h(n), and f(n) values
    def __init__(self):
        self.state = None
        self.parent = None

        self.g_n = 0
        self.h_n = 0
        self.f_n = 0
    
    def goal_test(self):
        if self.state is None:
            print("something has gone terribly wrong")
            return False

        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return (bool(self.state == goal))

# todo: more robust input handling...
def main():
    custom_puzzle = None
    queueing_function = None
    problem = node()

    raw_input = input("Welcome to Jesus' 8-puzzle solver. Type '1' to enter the default puzzle, or type '2' to create your own: ")
    puzzle_mode = int(raw_input)
    
    if (puzzle_mode == 1):
       puzzle = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
       problem.state = puzzle
    elif (puzzle_mode == 2):
        first_row = input("Enter the first row: ")
        second_row = input("Enter the second row: ")
        third_row = input("Enter the third row: ")

        first_row = first_row.split()
        second_row = second_row.split()
        third_row = third_row.split()

        for i in range(0, 3):
            first_row[i] = int(first_row[i])
            second_row[i] = int(second_row[i])
            third_row[i] = int(third_row[i])
        
        custom_puzzle = [first_row, second_row, third_row]
        problem.state = custom_puzzle
    else:
        print("Invalid input!")
        return
    
    raw_input = input("Select a queueing function. Type '1' for Uniform Cost Search. Type '2' for A* with the Misplaced Tile heuristic. Type '3' for A* with the Manhattan Distance heuristic: ")
    queueing_function_mode = int(raw_input)
    
    if (queueing_function_mode == 1):
        queueing_function = uniform_cost_search
    elif (queueing_function_mode == 2):
        queueing_function = misplaced_tile_heuristic
    elif (queueing_function_mode == 3):
        queueing_function = manhattan_distance_heuristic
    else:
        print("Invalid input!") 
        return
    
    # begin search
    solution_node, max_queue_size, iterations = general_search(problem, queueing_function)

    if (solution_node is None):
        print("search failed!")
        return
    
    print_stats(solution_node, max_queue_size, iterations)

    return

#using python list as queue, append to add to end of list, pop(0) to remove from beginning of list
#todo: get the max queue size and the number of nodes expanded 
def general_search(problem, queueing_function):
    iteration = 0
    max_node_queue_size = 0
    node_queue = []
    seen_states = []

    problem.h_n = queueing_function(problem.state)
    problem.f_n = problem.g_n + problem.h_n
    node_queue.append(problem)

    seen_states.append(problem.state)

    while(1):
        # if we run out of nodes to expand then the search has failed
        if (len(node_queue) == 0):
            return None

        # remove the node at the front of the queue with the smallest f(n)
        node = node_queue.pop(0)

        # is the node we removed our goal state? 
        if (node.goal_test()):
            return node, max_node_queue_size, iteration
        
        # expand the node we removed
        expand(node_queue, queueing_function, node, seen_states)

        # in-place sort from: https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
        node_queue.sort(key=lambda x: (x.f_n, x.g_n), reverse=False)

        # keep track of the max number of nodes in the queue (frontier nodes)
        max_node_queue_size = max(max_node_queue_size, len(node_queue))

        iteration += 1
        
    return

# four operators, up, down, left, right (-1 row, +1 row, -1 col, +1 col)
# todo: clean this up somehow...
def expand(node_queue, queueing_function, node, seen_states):
    blank_row = None
    blank_col = None

    test_row_col = None

    new_node = None

    #find the indices of the blank square '0'
    for i in range(3):
        for j in range(3):
            if (node.state[i][j] == 0):
                blank_row = i
                blank_col = j
                break

    
    
    # can the blank square move to the left?
    test_row_col = blank_col - 1
    if (test_row_col >= 0 and test_row_col <= 2): 
        # create a new node to apply this operator to
        new_node = copy.deepcopy(node) 
        # swap the the blank puzzle piece with the puzzle piece to the left of it (moves the blank square left)
        new_node.state[blank_row][blank_col], new_node.state[blank_row][test_row_col] = new_node.state[blank_row][test_row_col], new_node.state[blank_row][blank_col]

        # get g(n), h(n), and f(n) values for the new node
        new_node.g_n += 1
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n
        new_node.parent = node

        # ensure the new node has not been seen before
        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)

    # can the blank square move to the right?
    test_row_col = blank_col + 1
    if (test_row_col >= 0 and test_row_col <= 2): 
        # create a new node to apply this operator to
        new_node = copy.deepcopy(node) 
        # swap the the blank puzzle piece with the puzzle piece to the right of it (moves the blank square right)
        new_node.state[blank_row][blank_col], new_node.state[blank_row][test_row_col] = new_node.state[blank_row][test_row_col], new_node.state[blank_row][blank_col]

        # get g(n), h(n), and f(n) values for the new node
        new_node.g_n += 1
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n
        new_node.parent = node

        # ensure the new node has not been seen before
        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)

    # can the blank square move up?
    test_row_col = blank_row - 1
    if (test_row_col >= 0 and test_row_col <= 2): 
        # create a new node to apply this operator to
        new_node = copy.deepcopy(node) 
        # swap the the blank puzzle piece with the puzzle piece on top of it (moves the blank square up)
        new_node.state[blank_row][blank_col], new_node.state[test_row_col][blank_col] = new_node.state[test_row_col][blank_col], new_node.state[blank_row][blank_col]

        # get g(n), h(n), and f(n) values for the new node
        new_node.g_n += 1
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n
        new_node.parent = node

        # ensure the new node has not been seen before
        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)

    # can the blank square move down?
    test_row_col = blank_row + 1
    if (test_row_col >= 0 and test_row_col <= 2):
         # create a new node to apply this operator to
        new_node = copy.deepcopy(node) 
        # swap the the blank puzzle piece with the puzzle piece on below it (moves the blank square down)
        new_node.state[blank_row][blank_col], new_node.state[test_row_col][blank_col] = new_node.state[test_row_col][blank_col], new_node.state[blank_row][blank_col]

        # get g(n), h(n), and f(n) values for the new node
        new_node.g_n += 1
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n
        new_node.parent = node

        # ensure the new node has not been seen before
        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)

    return

# returns the h(n) value for a particular node's state
# uniform cost search has a h(n) of zero
def uniform_cost_search(state):
    return 0

# returns the h(n) value for a particular node's state
# using the misplaced tile heuristic
def misplaced_tile_heuristic(state):

    expected_tile = 1

    h_n = 0

    for i in range(3):
        for j in range(3):
            if (state[i][j] != expected_tile and state[i][j] != 0):
                h_n += 1
            expected_tile += 1

    return h_n

# returns the h(n) value for a particular node's state
# using the manhattan distance heuristic
def manhattan_distance_heuristic(state):

    expected_row = None
    expected_col = None

    h_n = 0

    # if tile is in correct spot, the manhattan distance will still be calculated
    # however, it will add 0 to h_n. only incorrect tiles will add meaningful 
    # values to h_n
    for row in range(3):
        for col in range(3):
            if (state[row][col] != 0):
                expected_row = int((state[row][col] - 1) / 3)
                expected_col = (state[row][col] - 1) % 3

                h_n += abs(expected_col - col) + abs(expected_row - row)

    return h_n

def print_stats(node, queue_size, iterations):
    print("search successful!")
    print()
    print("The depth of the solution is:", node.g_n)
    print("The maximum queue size was:", queue_size)
    print("The number of nodes expanded was:", iterations)
    print()

    curr_node = node
    path = []

    while curr_node is not None:
        path.append(curr_node)
        curr_node = curr_node.parent
    
    path.reverse()

    print("The path to the solution is:")
    for node in path:
        print(node.state)


if __name__ == "__main__":
    main()