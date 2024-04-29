import copy

class node:
    state = None
    g_n = None
    h_n = None
    f_n = None

    def __init__(self):
        self.g_n = 0
        self.h_n = 0
        self.f_n = 0
    
    def goal_test(self):
        if self.state is None:
            print("something has gone terribly wrong")
            return False

        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return (bool(self.state == goal))


def main():
    custom_puzzle = None
    queueing_function = None
    problem = node()

    raw_input = input("Welcome to Jesus' 8-puzzle solver. Type '1' to enter the default puzzle, or type '2' to create your own: ")
    puzzle_mode = int(raw_input)
    
    if (puzzle_mode == 1):
        puzzle = [[4, 1, 2], [5, 3, 0], [7, 8, 6]]
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
    
    general_search(problem, queueing_function)
    
    return

#using python list as queue, append to add to end of list, pop(0) to remove from beginning of list
#todo: get the max queue size and the number of nodes expanded 
def general_search(problem, queueing_function):
    iteration = 0

    # put 'problem' in a queue of nodes
    node_queue = []
    node_queue.append(problem)

    max_node_queue_size = 0

    seen_states = []
    seen_states.append(problem.state)

    expansions = 1

    while(1):
        print("Iteration", iteration, "of search")
        if (len(node_queue) == 0):
            print("search failed!")
            return False

        node = node_queue.pop(0)
        print("popped state with g(n) =", node.g_n, "and h(n) =", node.h_n)
        print(node.state)

        if (node.goal_test()):
            print("search success!")
            print("the solution depth is", node.g_n)
            print("the max queue size is", max_node_queue_size)
            return node
        
        #at this point i need to take node and expand it, aka find all ways 0 can move

        #todo: expand function? something like expand(node_queue, node)? would just add child notes to queue, up to queueing function to sort.
        expand(node_queue, queueing_function, node, seen_states)
        #todo: write queueing functions. 

        # in-place sort from: https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
        node_queue.sort(key=lambda x: x.f_n, reverse=False)

        print("printing node queue")
        for node in node_queue:
            print(node.state)

        if (max_node_queue_size < len(node_queue)):
            max_node_queue_size = len(node_queue)

        iteration += 1
        
    return

#node_queue is an unsorted queue
#node is the node dequeued from the node_queue, we want to expand this node

#problem: this function will do moves such that the parent state returns 
"""
Iteration 0 of search
popped state with g(n) = 0 and h(n) 0
[[4, 1, 2], [5, 3, 0], [7, 8, 6]]    
printing node queue
[[4, 1, 2], [5, 0, 3], [7, 8, 6]]    
[[4, 1, 2], [5, 3, 6], [7, 8, 0]]    
[[4, 1, 0], [5, 3, 2], [7, 8, 6]]    
Iteration 1 of search
popped state with g(n) = 1 and h(n) 6
[[4, 1, 2], [5, 0, 3], [7, 8, 6]] parent   
printing node queue
[[4, 1, 2], [5, 3, 6], [7, 8, 0]]
[[4, 1, 2], [0, 5, 3], [7, 8, 6]] child
[[4, 1, 0], [5, 3, 2], [7, 8, 6]] 
[[4, 1, 2], [5, 3, 0], [7, 8, 6]] shouldnt be here (child) (see line 124)
[[4, 0, 2], [5, 1, 3], [7, 8, 6]] child
[[4, 1, 2], [5, 8, 3], [7, 0, 6]] child
"""
#4 operators, up, down, left, right (-1 row, +1 row, -1 col, +1 col)
#returns the number of nodes expanded for a given node
def expand(node_queue, queueing_function, node, seen_states):
    blank_row = None
    blank_col = None

    test_row_col = None

    new_node = copy.deepcopy(node) 

    temp = None

    expansions = 0

    #find where the blank square '0' is
    for i in range(3):
        for j in range(3):
            if (node.state[i][j] == 0): #found the blank square
                blank_row = i
                blank_col = j
                break
    
    #can the blank square move left?
    test_row_col = blank_col - 1
    if (test_row_col >= 0 and test_row_col <= 2): #yes it can
        new_node = copy.deepcopy(node) 
        #swap the two indicies 
        new_node.state[blank_row][blank_col], new_node.state[blank_row][test_row_col] = new_node.state[blank_row][test_row_col], new_node.state[blank_row][blank_col]
        new_node.g_n += 1
        #need to get its h_n, which depends on the queueing function
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n

        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)
            expansions += 1
        else:
            print(new_node.state, "has been seen!")


    #can the blank square move right?
    test_row_col = blank_col + 1
    if (test_row_col >= 0 and test_row_col <= 2): #yes it can
        #make a new node
        new_node = copy.deepcopy(node) 
        #swap the two indicies 
        new_node.state[blank_row][blank_col], new_node.state[blank_row][test_row_col] = new_node.state[blank_row][test_row_col], new_node.state[blank_row][blank_col]
        new_node.g_n += 1
        #need to get its h_n, which depends on the queueing function
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n

        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)
            expansions += 1
        else:
            print(new_node.state, "has been seen!")

    #can the blank square move up?
    test_row_col = blank_row - 1
    if (test_row_col >= 0 and test_row_col <= 2): #yes it can
        #make a new node
        new_node = copy.deepcopy(node) 
        #swap the two indicies 
        new_node.state[blank_row][blank_col], new_node.state[test_row_col][blank_col] = new_node.state[test_row_col][blank_col], new_node.state[blank_row][blank_col]
        new_node.g_n += 1
        #need to get its h_n, which depends on the queueing function
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n

        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)
            expansions += 1
        else:
            print(new_node.state, "has been seen!")

    #can the blank square move down?
    test_row_col = blank_row + 1
    if (test_row_col >= 0 and test_row_col <= 2): #yes it can
        #make a new node
        new_node = copy.deepcopy(node) 
        #swap the two indicies 
        new_node.state[blank_row][blank_col], new_node.state[test_row_col][blank_col] = new_node.state[test_row_col][blank_col], new_node.state[blank_row][blank_col]
        new_node.g_n += 1
        #need to get its h_n, which depends on the queueing function
        new_node.h_n = queueing_function(new_node.state)
        new_node.f_n = new_node.g_n + new_node.h_n

        if (new_node.state not in seen_states):
            node_queue.append(new_node)
            seen_states.append(new_node.state)
            expansions += 1
        else:
            print(new_node.state, "has been seen!")

    return

#maybe these should just calculate the f_n value (g_n + h_n) 
#uniform_cost_search: f_n = g_n + 0
#for the other two h_n depends
def uniform_cost_search(state):
    #print("hello from uniform_cost_search!")
    return 0

def misplaced_tile_heuristic(state):
    #print("hello from misplaced_tile_heuristic!")
    correct_tile = 1
    h_n = 0

    for i in range(3):
        for j in range(3):
            if (state[i][j] != correct_tile and state[i][j] != 0):
                h_n += 1
            correct_tile += 1

    return h_n

def manhattan_distance_heuristic(state):
    #print("hello from manhattan_distance_heuristic!")
    #lookup table?
    expected_row = None
    expected_col = None

    h_n = 0

    # if tile is in correct spot, the manhattan distance will be calculated
    # however, it will add 0 to h_n. only incorrect tiles will add meaningful 
    # values to h_n
    for row in range(3):
        for col in range(3):
            if (state[row][col] != 0):
                expected_row = int((state[row][col] - 1) / 3)
                expected_col = (state[row][col] - 1) % 3

                h_n += abs(expected_col - col) + abs(expected_row - row)

    return h_n


if __name__ == "__main__":
    main()