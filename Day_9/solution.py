from tabnanny import check
import time
import numpy as np
import functools as ft


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


def open_file(filename: str) -> list:
    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    
    return [[int(num) for num in line] for line in data]


###############################################################################
# part 1

def check_smaller(data: list, line: int, col: int, check_line: int, 
                    check_col: int, skip: set) -> bool:
    """Checks if a particular coordinate has a smaller associated value than
    another coordinate. Additionally, if it is indeed smaller, add the other
    coordinate to the set of coordinates to skip.

    Args:
        data (list[list[int]]): map of the height
        line: y value of the coordinate that is supposed to be checked if it is
            smaller than the other coordinate
        col: x value of the coordinate that is supposed to be checked if it is
            smaller than the other coordinate
        check_line: y value of the coordinate that the other coordinate is 
            supposed to be compared against
        check_col: x value of the coordinate that the other coordinate is 
            supposed to be compared against
        skip (set[tuple[int]]): coordinates to be skipped

    Returns:
        smaller: true if the coordinate (line, col) has an associated value 
            smaller than the associated value of the coordinate (check_line, 
            check_col), false otherwise
    """
    
    smaller = data[check_line][check_col] > data[line][col]
    
    if smaller:
        skip.add((check_line, check_col))
    
    return smaller


def check_min_cond(data: list, line: int, col: int, skip: set) -> bool:
    """Checks if a particular coordinate of the data follows all the conditions
    necessary for it to be considered a low point in the data: it has to be
    lower than the values in the possible 4 directions (up, down, left and 
    right). If it follows the condition in one direction, it adds the coordinate
    in that direction to the set of coordinates to skip.

    Args:
        data (list[list[int]]): map of the heights
        line: y value of the coordinate
        col: x value of the coordinate
        skip (set[tuple[int]]): coordinates that should not be considered

    Returns:
        if the coordinate checks all the necessary conditions, return True,
            otherwise, it returns False
    """

    conditions_met = 0
    
    if line < len(data) - 1:
        conditions_met += check_smaller(data, line, col, line + 1, col, skip)
    else:
        conditions_met += 1
    
    if col < len(data[0]) - 1:
        conditions_met += check_smaller(data, line, col, line, col + 1, skip)
    else:
        conditions_met += 1

    if line > 0:
        conditions_met += check_smaller(data, line, col, line - 1, col, skip)
    else:
        conditions_met += 1
    
    if col > 0:
        conditions_met += check_smaller(data, line, col, line, col - 1, skip)
    else:
        conditions_met += 1
    
    return conditions_met == 4


def find_all_lows(data: list, get_low_points=False) -> int or list:
    """Finds the number of values that are smaller than their neighbors in all
    four directions or the coordinates associated with those values.

    Args:
        data (list[list[int]]): map of heights
        get_low_points (optional): if true, returns the coordinates of the 
            low values, otherwise, it returns the number of the low values. 
            Defaults to False.

    Returns:
        n_lows: number of low values
        low_points: list of coordinates of the low values
    """

    skip = set()
    n_lows = 0
    low_points = []

    for line, nums in enumerate(data):
        for col in range(len(nums)):
            if (line, col) not in skip:
                min_flag = check_min_cond(data, line, col, skip)
                n_lows += int(data[line][col]) + 1 if min_flag else 0
                if get_low_points and min_flag:
                    low_points.append((line, col))
    
    if get_low_points:
        return low_points
    return n_lows


@timer
def time_find_lows(data: list) -> int:
    """The only purpose of this is function is to measure the time it takes for
    the find_all_lows function to run, without interfering with the usage of
    this functions ahead in the program.

    Args:
        data (list[list[int]]): map of heights

    Returns:
        number of low values
    """

    return find_all_lows(data)


def part1(test_data: list, data: list):
    """Solves the second part of the problem for day 9.

    Args:
        test_data (list[list[int]]): small dataset provided to test the 
            algorithm.
        data (list[list[int]]): dataset used to solve part 1 of the problem.
    """

    time_find_lows(test_data)
    time_find_lows(data)


###############################################################################
# part 2

def get_neighbors(line: int, col: int, max_line: int, max_col: int) -> list:
    """Finds the coordinates of the adjacent positions of the current coordinate
    in the four possible directions (up, down, right, left).

    Args:
        line: y value of the current coordinate
        col: x value of the current coordinate
        max_line: maximum value the y value of a coordinate can have
        max_col: maximum value the x value of a coordinate can have

    Returns:
        neighbors: coordinates of the adjacent positions of the current 
            coordinate (line, col)
    """

    neighbors = []
    
    if line > 0:
        neighbors.append((line - 1, col))
    
    if col > 0:
        neighbors.append((line, col - 1))
    
    if line < max_line - 1:
        neighbors.append((line + 1, col))
    
    if col < max_col - 1:
        neighbors.append((line, col + 1))

    return neighbors


def expand_basin(data: list, coor: tuple, checked_coor: set) -> int:
    """Finds the size of a basin associated with one low value.

    Args:
        data (list[list[int]]): map of heights
        coor (tuple[int]): current coordinate from which to try to expand the
            basin
        checked_coor (set[tuple[int]]): set of coordinates that has already been
            checked.

    Returns:
        size of a basin
    """
    line, col = coor
    if coor in checked_coor or data[line][col] == 9:
        return 0
    
    neighbors = get_neighbors(line, col, len(data), len(data[0]))
    checked_coor.add(coor)
    return 1 + sum([expand_basin(data, coor, checked_coor) 
                    for coor in neighbors])


@timer
def get_basins(data: list) -> int:
    """Finds the size of the basin associated with each of low points and 
    calculates the product of the size of the three biggest basins.

    Args:
        data (list[list[int]]): map of heights

    Returns:
        product of the size of the three biggest basins
    """
    low_points = find_all_lows(data, True)
    checked_coor = set()
    
    basin_sizes = [expand_basin(data, coor, checked_coor) 
                    for coor in low_points]
    basin_sizes.sort()
    
    return ft.reduce(lambda acc, x: acc * x, basin_sizes[-3:], 1)


def part2(test_data: list, data: list):
    """Solves the second part of the problem for day 9.

    Args:
        test_data (list[list[int]]): small dataset provided to test the 
            algorithm.
        data (list[list[int]]): dataset used to solve part 2 of the problem.
    """

    get_basins(test_data)
    get_basins(data)


###############################################################################

if __name__ == '__main__':
    test_data = open_file("test_input.txt")
    data = open_file("input.txt")

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)