import sys

if __name__ == '__main__':
    # check if arguments were entered
    if len(sys.argv) < 3:
        print("Please enter the algorithm name and relative path to input file")
        print("Here is an example: ")
        print("python main.py <algorithm_name> <input_file_path>")
        quit()

    algorithm_name = sys.argv[1]
    input_file_path = sys.argv[2]

    print(algorithm_name)
    print(input_file_path)
