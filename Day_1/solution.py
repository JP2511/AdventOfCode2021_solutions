import numpy as np
from numba import jit
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
@jit(nopython=True)
def count_increases(data: np.ndarray) -> int:
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


def part1(test_data: np.ndarray, data: np.ndarray):
    """Solves the first part of the problem for day 1.

    Args:
        test_data: small dataset to compile the function
        data: dataset used to solve part 1 of the problem
    """

    count_increases(test_data) # compilation step on a smaller dataset
    count_increases(data)


###############################################################################
# part 2

@timer
@jit(nopython=True)
def count_3_increases(data: np.ndarray) -> int:
    """Counts the number of times the sum of three inputs increased from the
    sum of the previous three inputs. There is an overlap of 2 inputs between 
    the previous 3 inputs and the current three inputs. 

    Args:
        data: array of inputs

    Returns:
        Number of times one input increases to the next
    """

    last_value = data[0]+data[1]+data[2]
    result = 0
    i = 0
    for num in data[3:]:
        current = last_value + num - data[i]
        result += current > last_value
        last_value = current
        i += 1
    
    return result


def part2(test_data: np.ndarray, data: np.ndarray):
    """Solves the second part of the problem for day 1.

    Args:
        test_data: small dataset to compile the function
        data: dataset used to solve part 1 of the problem
    """

    count_3_increases(test_data) # compilation step on a smaller dataset
    count_3_increases(data)


############################################################################### 

if __name__ == '__main__':
    test_data = np.loadtxt("test_input.txt", dtype="int")
    data = np.loadtxt("input.txt", dtype="int")
    
    print("Part 1 " + "-"*40)
    part1(test_data, data)

    print("\nPart 2 " + "-"*40)
    part2(test_data, data)