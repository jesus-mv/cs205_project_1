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
        puzzle = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
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

#using python list as queue, append to add, pop to remove
def general_search(problem, queueing_function):
    # put 'problem' in a queue of nodes
    node_queue = []
    node_queue.append(problem)

    #test "function pointer"
    queueing_function()

    while(1):
        if (len(node_queue) == 0):
            return False
        
        node = node_queue.pop()

        if (node.goal_test()):
            return node
        
        #at this point i need to take node and expand it, aka find all ways 0 can move

        #todo: expand function? something like expand(node_queue, node)? would just add child notes to queue, up to queueing function to sort.
        expand(node_queue, queueing_function, node)
        #todo: write queueing functions. 
        
        

    return

#node_queue is an unsorted queue
#node is the node dequeued from the node_queue, we want to expand this node

#4 operators, up, down, left, right (-1 row, +1 row, -1 col, +1 col)
def expand(node_queue, queueing_function, node):
    blank_row = None
    blank_col = None

    test_row_col = None

    new_node = None

    temp = None

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
        #make a new node
        new_node = copy.deepcopy(node) 
        #swap the two indicies 
        new_node.state[blank_row][blank_col], new_node.state[blank_row][test_row_col] = new_node.state[blank_row][test_row_col], new_node.state[blank_row][blank_col]
        new_node.g_n += 1
        #need to get its h_n, which depends on the queueing function
        new_node.h_n = queueing_function(new_node.state)
        node_queue.append(new_node)

    

        
            

    return

#maybe these should just calculate the f_n value (g_n + h_n) 
#uniform_cost_search: f_n = g_n + 0
#for the other two h_n depends
def uniform_cost_search(state):
    print("hello from uniform_cost_search!")
    return 0

def misplaced_tile_heuristic(state):
    print("hello from misplaced_tile_heuristic!")
    correct_tile = 1
    h_n = 0

    for i in range(3):
        for j in range(3):
            if (state[i][j] != correct_tile and state[i][j] != 0):
                h_n += 1
            correct_tile += 1

    return h_n

def manhattan_distance_heuristic(state):
    print("hello from manhattan_distance_heuristic!")
    #lookup table?
    return


if __name__ == "__main__":
    main()