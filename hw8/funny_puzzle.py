import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for i in range(len(to_state)):
        if from_state[i] == 0:
            continue
        x_dist = abs(i % 3 - (from_state[i]-1) % 3)
        y_dist = abs((i//3) - (from_state[i]-1)//3)
        distance += y_dist + x_dist
    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, f"h={get_manhattan_distance(succ_state)}")


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = list(list())
    #get x and y values for the 0s.
    #x_vals = tuple()
    #y_vals = tuple()
    for i in range(len(state)):
        adj_vals = list()
        if state[i] == 0:
            x_val = i % 3
            y_val = i // 3
            #horizontal
            #ifs are to not switch 0 values.
            if x_val == 1:
                if state[i-1] != 0:
                    succ_states.append(switch_values(state, i-1, i))
                if state[i+1] != 0:
                    succ_states.append(switch_values(state, i+1, i))
            elif x_val == 2:
                if state[i-1] != 0:
                    succ_states.append(switch_values(state, i-1, i))
            elif x_val == 0:
                if state[i+1] != 0:
                    succ_states.append(switch_values(state, i+1, i))
            #vertical
            if y_val == 1:
                if state[i+3] != 0:
                    succ_states.append(switch_values(state, i+3, i))
                if state[i-3] != 0:
                    succ_states.append(switch_values(state, i-3, i))
            elif y_val == 0:
                if state[i+3] != 0:
                    succ_states.append(switch_values(state, i+3, i))
            elif y_val == 2:
                if state[i-3] != 0:
                    succ_states.append(switch_values(state, i-3, i))
    return sorted(succ_states)

def switch_values(state, indexNewVal, indexOldVal):
    #switches a with b
    if state[indexNewVal] == 0:
        return
    new_state = state[:]
    temp = new_state[indexOldVal]
    new_state[indexOldVal] = new_state[indexNewVal]
    new_state[indexNewVal] = temp
    return new_state

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along h values, number of moves,
        and max queue number in the format specified in the pdf.
    """
    pq = []
    visited = set()
    state_tuple = tuple(state)
    heapq.heappush(pq, (get_manhattan_distance(state), state_tuple, (0, get_manhattan_distance(state), -1)))
    max_queue_length = 0
    path = []

    while pq:
        max_queue_length = max(max_queue_length, len(pq))
        cost, state, (num_moves, h, parent_index) = heapq.heappop(pq)
        visited.add(state)

        if state == tuple(goal_state):
            path.append((list(state), (num_moves, h, parent_index)))
            break

        successors = get_succ(list(state))
        for succ in successors:
            succ_tuple = tuple(succ)
            if succ_tuple not in visited:
                moves_inc = num_moves + 1
                h_inc = get_manhattan_distance(succ, goal_state)
                cost_inc = moves_inc + h_inc
                heapq.heappush(pq, (cost_inc, succ_tuple, (moves_inc, h_inc, len(path))))

        path.append((list(state), (num_moves, h, parent_index)))

    solution_path = []
    index = len(path) - 1
    while index != -1:
        state, (num_moves, h, parent_index) = path[index]
        solution_path.append((state, h, num_moves))
        index = parent_index

    solution_path.reverse()
    for state, h, num_moves in solution_path:
        print(state, f"h={h} moves: {num_moves}")

    print("Max queue length:", max_queue_length)




if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()
    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([5, 2, 3, 0, 6, 4, 7, 1, 0])
    print()
