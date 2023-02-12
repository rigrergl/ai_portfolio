import sys
import pathlib
import copy

is_goal_found = False
nodes_enqueued = 0


class Node:
    def __init__(self, state, parent=None):
        self.state = None
        self.parent = None
        self.depth = 0

        if (not isinstance(state, State)) or (parent is not None and not isinstance(parent, Node)):
            raise ValueError("Unsupported Argument Type")

        self.state = state

        if parent:
            self.parent = parent
            self.depth = parent.depth + 1

    def get_children(self):
        children = []
        adjacent_states = self.state.get_adjacent_states()
        for state in adjacent_states:
            child = Node(state, self)
            children.append(child)
        return children


class State:
    def __init__(self, arg):
        self.data = None
        if isinstance(arg, str):
            self.from_string(arg)
        elif isinstance(arg, list):
            self.from_list(arg)
        else:
            raise ValueError("Unsupported Argument Type")

    def from_string(self, arg):
        chars = arg.split()
        self.data = [list(chars[i:i + 3]) for i in range(0, len(chars), 3)]

    def from_list(self, arg):
        self.data = arg

    def __str__(self):
        result = ""
        for line in self.data:
            for c in line:
                result += c + " "
            result = result.strip() + "\n"
        return result

    def is_goal_state(self):
        return self.data[0] == ["7", "8", "1"] and self.data[1] == ["6", "*", "2"] and self.data[2] == ["5", "4", "3"]

    def __eq__(self, other):
        if isinstance(other, State):
            return self.data == other.data
        return False

    def __hash__(self):
        return hash(tuple(map(tuple, self.data)))

    def get_adjacent_states(self):
        """Returns adjacent states in the following order:
            1. moving left item into blank
            2. Moving top item into blank
            3. Moving right item into blank
            4. Moving bottom item into blank
        """
        adjacent_states = []
        blank_r, blank_c = self.find_blank_tile()

        # moving left item into blank
        if blank_c > 0:
            new_state = State(copy.deepcopy(self.data))
            new_state.switch_positions(blank_r, blank_c, blank_r, blank_c - 1)
            adjacent_states.append(new_state)

        # moving top item into blank
        if blank_r > 0:
            new_state = State(copy.deepcopy(self.data))
            new_state.switch_positions(blank_r, blank_c, blank_r - 1, blank_c)
            adjacent_states.append(new_state)

        # moving right item into blank
        if blank_c < len(self.data[blank_r]) - 1:
            new_state = State(copy.deepcopy(self.data))
            new_state.switch_positions(blank_r, blank_c, blank_r, blank_c + 1)
            adjacent_states.append(new_state)

        # moving bottom item into blank
        if blank_r < len(self.data) - 1:
            new_state = State(copy.deepcopy(self.data))
            new_state.switch_positions(blank_r, blank_c, blank_r + 1, blank_c)
            adjacent_states.append(new_state)

        return adjacent_states

    def find_blank_tile(self):
        for r, row in enumerate(self.data):
            for c, item in enumerate(row):
                if item == "*":
                    return r, c

    def switch_positions(self, r1, c1, r2, c2):
        """Switches the positions of items (r1, c1) and (r2, c2)"""
        temp = self.data[r1][c1]
        self.data[r1][c1] = self.data[r2][c2]
        self.data[r2][c2] = temp

    def heuristic1(self):
        """
        Heuristic 1 counts the number of tiles in the wrong position
        """
        h1 = 0

        if self.data[0][2] != "1":
            h1 += 1
        if self.data[1][2] != "2":
            h1 += 1
        if self.data[2][2] != "3":
            h1 += 1
        if self.data[2][1] != "4":
            h1 += 1
        if self.data[2][0] != "5":
            h1 += 1
        if self.data[1][0] != "6":
            h1 += 1
        if self.data[0][0] != "7":
            h1 += 1
        if self.data[0][1] != "8":
            h1 += 1

        return h1


def print_path_to_parent(node):
    if not isinstance(node, Node):
        raise ValueError("Unsupported argument type")

    path_stack = []
    while node is not None:
        path_stack.append(node.state)
        node = node.parent

    while path_stack:
        next_state = path_stack.pop()
        print(next_state, "\n")


def path_has_repeated_state(node):
    if not isinstance(node, Node):
        raise ValueError("Unsupported argument type")

    state_set = set()
    while node is not None:
        if node.state in state_set:
            return True
        state_set.add(node.state)
        node = node.parent
    return False


def dfs_helper(node, max_depth=10):
    global nodes_enqueued
    global is_goal_found
    nodes_enqueued += 1

    if is_goal_found:
        return None
    elif node.depth > max_depth:
        return None
    elif node.state.is_goal_state():
        is_goal_found = True
        return node
    elif path_has_repeated_state(node):
        return None
    else:
        for child in node.get_children():
            solution = dfs_helper(child, max_depth)
            if solution:
                return solution


def dfs(i_state):
    """Runs the Depth-First Search Algorithm"""
    return dfs_helper(Node(i_state))


def ids(i_state):
    """Run the Iterative Depth-First Search Algorithm"""
    for i in range(11):
        solution = dfs_helper(Node(i_state), i)
        if solution:
            print("Solution found at depth", i)
            return solution
        else:
            print("Solution not found at depth", i)
    return None


def astar1(i_state):
    """Runs the A* algorithm with heuristic 1"""
    print(i_state)
    print(i_state.heuristic1())
    return False


def astar2(i_state):
    """Runs the A* algorithm with heuristic 2"""
    print("TODO")
    return False


if __name__ == '__main__':
    # check if arguments were entered
    if len(sys.argv) < 3:
        print("Please enter the algorithm name and relative path to input file")
        print("Here is an example: ")
        print("python main.py <algorithm_name> <input_file_path>")
        quit()

    algorithm_name = sys.argv[1]
    input_file_path = sys.argv[2]

    # Retrieve input data in text format
    with open(pathlib.Path.cwd().joinpath(input_file_path), 'r') as f:
        text_in = f.read()

    # Generate State object from input data
    initial_state = State(text_in)

    # Compute solution using the desired algorithm
    if algorithm_name == "dfs":
        solution_node = dfs(initial_state)
    elif algorithm_name == "ids":
        solution_node = ids(initial_state)
    elif algorithm_name == "astar1":
        solution_node = astar1(initial_state)
    elif algorithm_name == "astar2":
        solution_node = astar2(initial_state)
    else:
        print("Error: algorithm_name not recognized")
        quit()

    if solution_node:
        print_path_to_parent(solution_node)
        print("Number of move =", solution_node.depth)
        print("Number of states enqueued =", nodes_enqueued)
    else:
        print("Failure: solution not found with given parameters")
