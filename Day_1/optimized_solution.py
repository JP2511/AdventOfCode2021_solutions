import numpy as np
from numba import jit
import time


###############################################################################


def timer(function: function):
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
@jit(nopython=True)
def count_increases(data: np.Array) -> int:
    """Counts the number of times one input increases to the next.

    Args:
        data: array of inputs

    Returns:
        Number of times one input increases to the next
    """

    i = 0
    result = 0
    for num in data[1:]:
        result += num > data[i]
        i += 1
    return result


def part1():
    """Solves the first part of the problem for day 1.
    """
    test_data = np.loadtxt("test_input.txt").astype("int64")
    count_increases(test_data) # compilation step on a smaller dataset

    data = np.loadtxt("input.txt").astype("int64")
    count_increases(data)


############################################################################### 

part1()