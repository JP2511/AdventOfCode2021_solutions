import time
import copy

import numpy as np
import collections as cls

from typing import Generator


###############################################################################

def timer(function):
    """Times the time in miliseconds that it takes for a function to run given
    its inputs.

    Args:
        function: function to time.
    """
    
    def inner(*args):
        start = time.time()
        print(f"The solution is: {function(*args)}")
        print(f"It took {(time.time()-start)*(10**3)} miliseconds to execute.")
        print("#"*40)
    return inner


def read_file(filename: str) -> np.ndarray:
    """Reads the lines from the file.

    Args:
        filename: name of the file with the data.

    Returns:
        grid of energy
    
    Requires:
        filename must be the name of a valid file.
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    
    return np.array([[int(i) for i in line] for line in data])


###############################################################################
# part 1

def get_start_flashes(data: np.ndarray) -> cls.deque:
    """Increments each energy level of the grid and returns a queue with the 
    coordinates of the values that are higher than 9.

    Args:
        data: grid of energy levels

    Returns:
        start_flashes: coordinates of the values that are higher than 9
    
    Ensures:
        the coordinates are given in the following format: (line, col)
    """
    
    start_flashes = cls.deque()
    y_length, x_length = data.shape
    
    for line in np.arange(y_length):
        for col in np.arange(x_length):
            data[line][col] += 1
            
            if data[line][col] > 9:
                start_flashes.append((line, col))
    
    return start_flashes


def get_neighbors(line: int, col: int, max_line: int, max_col: int)-> Generator:
    """Obtains the coordinates of the surrounding values.

    Args:
        line: y value of the current coordinate
        col: x value of the current coordinate
        max_line: maximum value the y value of a coordinate can take
        max_col: maximum value the x value of a coordinate can take

    Returns:
        coordinates of the surrounding values.
    
    Ensures:
        the coordinates are given in the following format: (line, col)
        the coordinates returned have line values between 0 and max_line - 1 and
            col values between 0 and max_col - 1
    """
    
    line_values = range(-1 if line > 0 else 0, 2 if line < max_line - 1 else 1)
    col_values = range(-1 if col > 0 else 0, 2 if col < max_col - 1 else 1)
    
    return ((line + i, col + j) for i in line_values for j in col_values 
            if not (i == 0 and j == 0))


def perform_flash(data: np.ndarray, flashes: cls.deque, prev_flashes: set, 
                    line: int, col: int):
    """Performs a flash by incrementing each neighboring value by 1. If any of
    these values become higher than 9, their coordinates are added to the 
    flashes queue.

    Args:
        data: map of energy levels
        flashes: coordinates of flashes to consinder in this step
        prev_flashes: flashes that have already been performed
        line: y value of the coordinate of the current flash
        col: x value of the coordinate of the current flash
    """

    for curr_line, curr_col in get_neighbors(line, col, *data.shape):
        if (curr_line, curr_col) in prev_flashes:
            continue
        
        data[curr_line][curr_col] += 1
        
        if data[curr_line][curr_col] > 9:
            flashes.append((curr_line, curr_col))


def count_perform_flashes(data: np.ndarray, start_flashes: cls.deque) -> int:
    """Performs and counts all flashes that occur in a single step.

    Args:
        data: grid of energy levels
        start_flashes: coordinates of the values that obtained a value higher 
            than 9 during the increment of the whole grid during a particular 
            step.

    Returns:
        n_flashes: number of flashes that occurred in a particular step
    """

    prev_flashes = set()

    while len(start_flashes) > 0:
        line, col = start_flashes.popleft()

        if (line, col) not in prev_flashes:
            prev_flashes.add((line, col))
            perform_flash(data, start_flashes, prev_flashes, line, col)

    n_flashes = len(prev_flashes)

    for line, col in prev_flashes:
        data[line][col] = 0
    
    return n_flashes


@timer
def count_flashes(data: np.ndarray, steps: int) -> int:
    """Counts the number of flashes that occur in a particular grid in a parti-
    cular amount of steps.

    Args:
        data: grid of energy levels
        steps: number of iterations for the algorithm to run

    Returns:
        n_flashes: number of flashes
    """

    n_flashes = 0
    
    for _ in np.arange(steps):
        start_flashes = get_start_flashes(data)
        n_flashes += count_perform_flashes(data, start_flashes)
    
    return n_flashes


def part1(test_data: np.ndarray, data: np.ndarray):
    """Solves the second part of the problem for day 11.

    Args:
        test_data (list[str]): small dataset provided to test the 
            algorithm.
        data (list[str]): dataset used to solve part 1 of the problem.
    """

    count_flashes(test_data, 100)
    count_flashes(data, 100)


###############################################################################
# part 2

@timer
def find_sim_flash(data: np.ndarray) -> int:
    """Determines the number of steps until the first time all values flash in
    the same step.

    Args:
        data: grid of energy levels

    Returns:
        steps: first step where all values are flashed in the same step
    """

    n_flashes = 0
    max_flashes = data.shape[0] * data.shape[1]
    steps = 0
    
    while n_flashes != max_flashes:
        steps += 1
        start_flashes = get_start_flashes(data)
        n_flashes = count_perform_flashes(data, start_flashes)
    
    return steps


def part2(test_data: np.ndarray, data: np.ndarray):
    """Solves the second part of the problem for day 11.

    Args:
        test_data (list[str]): small dataset provided to test the 
            algorithm.
        data (list[str]): dataset used to solve part 2 of the problem.
    """

    find_sim_flash(test_data)
    find_sim_flash(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file('test_input.txt')
    data = read_file('input.txt')

    print("Part 1 " + "-"*30)
    part1(copy.copy(test_data), copy.copy(data))
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)
