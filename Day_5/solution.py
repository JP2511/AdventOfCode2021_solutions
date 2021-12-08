import time
import re
from typing import Iterable


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


def read_file(filename: str) -> list:
    """Opens a file and reads the data.

    Args:
        filename: name of the file to read.

    Returns:
        : list of lines created by two points in 2D.

    Requires:
        filename must be the name of a valid file.
        the lines of the file should have the following format `x1,y1 -> x2,y2`.
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read()
    
    return re.findall(r"([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)", data)


###############################################################################
# Part 1

def filter_data(data: list) -> list:
    """Removes lines which are not horizontal or vertical and reorganizes the
    values order.

    Args:
        data: x1, y1, x2, y2 values per line.

    Returns:
        : x1, x2, y1, y2 values of the horizontal or vertical lines. The order
            of xs or the order of the ys might be switched if x2 > x1 or if 
            y2 > y1, respectively.
    
    Requires:
        data should be a list of 4 integer tuples.
    """

    def choose_ver_hor(values: tuple) -> bool:
        x1, y1, x2, y2 = values
        return  (x1 == x2 and y1 != y2) or (x1 != x2 and y1 == y2)

    def rearrange(values: tuple) -> tuple:
        x1, y1, x2, y2 = list(map(int, values))
        if x2 < x1:
            return (x2, x1, y1, y2)
        if y2 < y1:
            return (x1, x2, y2, y1)
        return (x1, x2, y1, y2)
    
    return list(map(rearrange, filter(choose_ver_hor, data)))


def count_line(graph: dict, pos: tuple, overlaps: set):
    """Adds a point to the graph of points where each point has been passed at 
    least once by a line or if the point is already on the graph, increases the
    number of overlaps until it reaches 2 and adds it to the set of overlapped
    points.

    Args:
        graph: points in the graph through which at least a line passes and the 
            number of times and line has passed through each point
        pos: x and y coordinates of a point.
        overlaps: points that have been overlapped at least twice.
    """

    if pos not in graph:
        graph[pos] = 1
    else:
        if graph[pos] == 1:
            overlaps.add(pos)
            graph[pos] += 1


def graph_data(filtered_data: list) -> int:
    """Counts the number of points that have been passed by at least two lines.

    Args:
        filtered_data (list): list of x1, x2, y1, y2 values of horizontal and
            vertical lines.

    Returns:
        : number of points that have been passed by at least two lines.
    """

    graph = {}
    overlaps = set()
    for line in filtered_data:
        x1, x2, y1, y2 = line

        if x1 != x2:
            for x in range(x1, x2 + 1):
                count_line(graph, (x, y1), overlaps)
        else:
            for y in range(y1, y2 + 1):
                count_line(graph, (x1, y), overlaps)
    
    return len(overlaps)


@timer
def count_overlaps(raw_data: list) -> int:
    """Counts the number of points that have been passed by at least two 
    vertical or horizontal lines.

    Args:
        raw_data: x1, y1, x2, y2 values of all lines.

    Returns:
        : number of points that have been passed by at least two lines.
    """

    return graph_data(filter_data(raw_data))


def part1(test_data, data):
    """Solves the first part of the problem for day 5.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    count_overlaps(test_data)
    count_overlaps(data)


###############################################################################

def filter_data_w_diag(data: list) -> list:
    """Reorganizes the values' order.

    Args:
        data: x1, y1, x2, y2 values per line.

    Returns:
        : x1, x2, y1, y2 values of the lines. The order of xs or the order of 
            the ys might be switched if x2 > x1 and x2 == x1 or if y2 > y1 and
            x1 == x2, respectively.
    """

    def rearrange(values: tuple) -> tuple:
        x1, y1, x2, y2 = list(map(int, values))
        
        if x2 < x1 and y2 == y1:
            return (x2, x1, y1, y2)
        
        elif y2 < y1 and x2 == x1:
            return (x1, x2, y2, y1)
        
        return (x1, x2, y1, y2)
    
    return list(map(rearrange, data))


def create_range(z1: int, z2: int) -> Iterable:
    """Creates a generator of integer values from z1 to z2 or from z2 to z1,
    depending on z1 < z2 or z1 > z2, respectively.

    Args:
        z1: integer value.
        z2: integer value.

    Returns:
        : generator of integer values from z1 to z2 or from z2 to z1, 
            depending on z1 < z2 or z1 > z2, respectively.
    """

    if z1 < z2:
        return range(z1, z2 + 1)
    else:
        return range(z1, z2 - 1, -1)


def graph_data_w_diag(filtered_data: list) -> int:
    """Counts the number of points that have been passed by at least two lines.

    Args:
        filtered_data (list): list of x1, x2, y1, y2 values of all lines.

    Returns:
        : number of points that have been passed by at least two lines.
    """

    graph = {}
    overlaps = set()
    for line in filtered_data:
        x1, x2, y1, y2 = line

        if x1 != x2 and y1 != y2:
            for i, j in zip(create_range(x1, x2), create_range(y1, y2)):
                count_line(graph, (i,j), overlaps)
        elif x1 != x2:
            for x in range(x1, x2 + 1):
                count_line(graph, (x, y1), overlaps)
        else:
            for y in range(y1, y2 + 1):
                count_line(graph, (x1, y), overlaps)
    return len(overlaps)


@timer
def count_overlaps_w_diag(raw_data: list) -> int:
    """Counts the number of points that have been passed by at least two lines.

    Args:
        raw_data: x1, y1, x2, y2 values of all lines.

    Returns:
        : number of points that have been passed by at least two lines.
    """

    return graph_data_w_diag(filter_data_w_diag(raw_data))


def part2(test_data, data):
    """Solves the second part of the problem for day 5.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 2 of the problem
    """

    count_overlaps_w_diag(test_data)
    count_overlaps_w_diag(data)



###############################################################################

if __name__ == '__main__':
    test_data = read_file("test_input.txt")
    data = read_file("input.txt")

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)