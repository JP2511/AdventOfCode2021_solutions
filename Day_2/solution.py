from typing import List, Tuple

import numpy as np
import time


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


###############################################################################
# part 1

@timer
def calculate_coor(data: np.ndarray) -> int:
    """Given a set of instructions with values associated, it increases or
    decreases the values of the horizontal position and the depth in accordance
    to the problem. After obtaining the final values of horizontal position and
    depth, it calculates the product of the two.

    Args:
        data: set of instructions with associated values

    Returns:
        int: result of the multiplication of the final horizontal position with
            the final value.
    """

    hor_pos = 0
    depth = 0
    for direction, val in data:
        if direction[0] == "f":
            hor_pos += int(val)
        elif direction[0] == "u":
            depth += -int(val)
        else:
            depth += int(val)
    return hor_pos * depth


def part1(test_data: np.ndarray, data: np.ndarray):
    """Solves the first part of the problem for day 2.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    calculate_coor(test_data)
    calculate_coor(data)


###############################################################################


@timer
def calculate_coor_w_aim(data: np.ndarray) -> int:
    """Given a set of instructions with values associated, it increases or
    decreases the values of the horizontal position, aim and the depth in 
    accordance to the problem. After obtaining the final values of horizontal 
    position and depth, it calculates the product of the two.

    Args:
        data: set of instructions with associated values

    Returns:
        int: result of the multiplication of the final horizontal position with
            the final value.
    """
    
    hor_pos = 0
    depth = 0
    aim = 0
    for direction, val in data:
        if direction[0] == "f":
            hor_pos += int(val)
            depth += int(val)*aim
        elif direction[0] == "u":
            aim += -int(val)
        else:
            aim += int(val)
    return hor_pos * depth


def part2(test_data: np.ndarray, data: np.ndarray):
    """Solves the second part of the problem for day 2.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 2 of the problem
    """
    calculate_coor_w_aim(test_data)
    calculate_coor_w_aim(data)



###############################################################################

if __name__ == '__main__':
    test_data = np.loadtxt("test_input.txt", dtype=str, delimiter=" ")
    data = np.loadtxt("input.txt", dtype=str, delimiter=" ")
    
    print("Part 1 " + "-"*30)
    part1(test_data, data)

    print("\nPart 2 " + "-"*30)
    part2(test_data, data)