import numpy as np
import numba as nb
import functools as ft
import time
import math


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

@nb.njit()
def calculated_var(h_est: int, x: int) -> int: 
    """Finds the distance between the midpoint and some other point.

    Args:
        h_est: Midpoint.
        x: Point to measure the distance to the midpoint.

    Returns:
        distance to the midpoint.
    """
    return np.abs(h_est - x)


@timer
@nb.njit()
def calc_least_consumption(data: np.ndarray) -> int:
    """Finds the point closest to most points in the data and calculates the
    cumulative distance of all the points to the mid point. The value of the
    distance between two points is just the absolute value of the difference
    between those two points.

    Args:
        data: points to measure the distance against.

    Returns:
        cumulative distance of the midpoint to the points of the data.
    """

    sorted_data = np.sort(data)

    half = len(sorted_data) // 2
    var_w_half = lambda x: calculated_var(half, x)

    if len(sorted_data) % 2 == 0:
        h_est = int(round((sorted_data[half] + sorted_data[half-1])/2))
        var_w_h_est = lambda x: calculated_var(h_est, x)

        return np.sum(var_w_h_est(sorted_data))
    
    return np.sum(var_w_half(sorted_data))


def part1(test_data, data):
    """Solves the first part of the problem for day 7.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    calc_least_consumption(test_data)
    calc_least_consumption(data)


###############################################################################
# Part 2

@ft.lru_cache()
def cache_arange(generations: int) -> int:
    """Calculates the distance between two points. Given that the distance is
    given by the sum of values of the succession with the following rule: 
    a_n = n. So, the distance of two points, of which that absolute difference 
    is 4 is a_4 + a_3 + a_2 + a_1= 4 + 3 + 2 + 1  = 10.

    Args:
        generations: absolute difference between the two points.

    Returns:
        distance between two points.
    """

    return np.sum(np.arange(1, generations+1))


def h_move(x1: int, x_bar: int) -> int:
    """Calculates the cost/distance of a point to a possible midpoint.

    Args:
        x1: point to measure the distance to the midpoint.
        x_bar: midpoint

    Returns:
        distance of the point to the midpoint.
    """

    generations = np.abs(x1 - x_bar)
    if generations == 0:
        return 0

    return cache_arange(generations)


@timer
def find_cost_midpoint(data):
    """Find the midpoint value in the data, where the distance is measured 
    cumulatively, and calculates the distance from midpoint to all the other 
    points.

    Args:
        data: data from which to find the midpoint and to calculate the distance
            from it.

    Returns:
        sum of the distance from all the points to the midpoint.
    """
    
    mean = np.sum(data)/len(data)
    
    low_mean = math.floor(mean)
    low_move_calc = lambda x: h_move(x, low_mean)
    up_mean = math.ceil(mean)
    up_move_calc = lambda x: h_move(x, up_mean)
    
    return min(sum(map(low_move_calc, data)), sum(map(up_move_calc, data)))


def part2(test_data, data):
    """Solves the second part of the problem for day 7.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 2 of the problem
    """

    find_cost_midpoint(test_data)
    find_cost_midpoint(data)


###############################################################################

if __name__ == '__main__':
    test_data = np.loadtxt("test_input.txt", delimiter=",", dtype='int64')
    data = np.loadtxt("input.txt", delimiter=",", dtype='int64')

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)