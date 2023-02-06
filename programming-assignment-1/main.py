import sys
import pathlib


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
        return str(self.data)


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
    print(initial_state)
