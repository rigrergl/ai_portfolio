import sys
import pathlib
import copy


class Node:
    def __init__(self, state, parent):
        self.state = None
        self.parent = None
        self.depth = 0

        if (not isinstance(state, State)) or (parent is not None and not isinstance(parent, Node)):
            raise ValueError("Unsupported Argument Type")

        self.state = state

        if parent:
            self.parent = parent
            self.depth = parent.depth + 1


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
        self.data = []
        lines = arg.splitlines()
        for line in lines:
            self.data.append(line.split())

    def from_list(self, arg):
        self.data = arg

    def __str__(self):
        result = ""
        for line in self.data:
            for c in line:
                result += c + " "
            result = result.strip() + "\n"
        return result

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


def dfs(i_state):
    """Runs the Depth-First Search Algorithm"""
    print("Initial state:")
    print(i_state)

    print("Adjacent States:")
    adjacent_states = i_state.get_adjacent_states()
    for state in adjacent_states:
        print(state)


def ids(i_state):
    """Run the Iterative Depth-First Search Algorithm"""
    print("TODO")


def astar1(i_state):
    """Runs the A* algorithm with heuristic 1"""
    print("TODO")


def astar2(i_state):
    """Runs the A* algorithm with heuristic 2"""
    print("TODO")


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
        dfs(initial_state)
    elif algorithm_name == "ids":
        ids(initial_state)
    elif algorithm_name == "astar1":
        astar1(initial_state)
    elif algorithm_name == "astar2":
        astar2(initial_state)
    else:
        print("Error: algorithm_name not recognized")
        quit()
