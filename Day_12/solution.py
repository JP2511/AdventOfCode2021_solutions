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


def read_file(filename: str) -> list:
    """Reads the lines from the file.

    Args:
        filename: name of the file with the data.

    Returns:
        edges of a directed graph from start to end.
    
    Requires:
        filename must be the name of a valid file.
        separator of the vertices should be a "-"
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    
    return [line.split("-") for line in data]


###############################################################################
# part 1

def construct_graph(edges: list) -> dict:
    """Constructs a graph from the edges in the form of a dictionary.

    Args:
        edges: edges of the graph

    Returns:
        graph: graph in the form of a dictionary
    """

    graph = {}
    
    for vert1, vert2 in edges:
        if vert1 not in graph:
            graph[vert1] = {vert2}
        else:
            graph[vert1].add(vert2)
        
        if vert2 not in graph:
            graph[vert2] = {vert1}
        else:
            graph[vert2].add(vert1)

    return graph


def run_through_graph(graph: dict, curr_vert: str="start", 
                        prev_vert: frozenset=frozenset(["start"])) -> int:
    """Counts the number of possible paths from the vertice "start" to the
    the vertice "end". In these paths, vertices with uncapitalized names can 
    only be passed once.

    Args:
        graph: graph of vertices and edges
        curr_vert (optional): current vertice during the traversal of the gaph. 
            Defaults to "start".
        prev_vert (optional): vertices with uncapitalized names that have 
            already been passed. Defaults to frozenset(["start"]).

    Returns:
        result: number of possible paths from start to end without repeating
            uncapitalized vertices
    """
    
    if curr_vert == "end":
        return 1
    
    result = 0
    for vert in graph[curr_vert] - prev_vert:
        curr_prev_vert = prev_vert
        
        if vert.lower() == vert and vert != "end":
            curr_prev_vert = frozenset([*prev_vert, vert])
        
        result += run_through_graph(graph, vert, curr_prev_vert)

    return result


@timer
def count_paths(data: list) -> int:
    """Constructs a graph from the data and counts the number of possible paths
    from start to end without repeating vertices with uncapitalized names.

    Args:
        data: edges of the graph

    Returns:
        number of possible paths from start to end without repeating 
            uncapitalized vertices
    """

    graph = construct_graph(data)
    return run_through_graph(graph)


def part1(test_data: list, data: list):
    """Solves the second part of the problem for day 12.

    Args:
        test_data: small dataset provided to test the algorithm.
        data: dataset used to solve part 1 of the problem.
    """

    count_paths(test_data)
    count_paths(data)


###############################################################################
# part 2

def run_through_graph_mul(graph: dict, curr_vert: str="start", rep: bool=False,
                        prev_vert: frozenset=frozenset(["start"])) -> int:
    """Counts the number of possible paths from the vertice "start" to the
    the vertice "end". In these paths, vertices with uncapitalized names can 
    only be passed once, except one, which can be repeated once.

    Args:
        graph: graph of vertices and edges
        curr_vert (optional): current vertice during the traversal of the gaph. 
            Defaults to "start".
        rep (optional): indicates if the vertice that can be repeated once, has
            already been repeated.
        prev_vert (optional): vertices with uncapitalized names that have 
            already been passed. Defaults to frozenset(["start"]).

    Returns:
        result: number of possible paths from start to end without repeating
            uncapitalized vertices except one, once.
    """
    
    if curr_vert == "end":
        return 1
    
    result = 0
    poss_opt = graph[curr_vert]-prev_vert if rep else graph[curr_vert]-{'start'}
    for vert in poss_opt:
        curr_prev_vert = prev_vert
        curr_rep = rep
        
        if vert.lower() == vert and vert != "end":
            if not rep:
                curr_rep = vert in curr_prev_vert
            curr_prev_vert = frozenset([*prev_vert, vert])
        
        result += run_through_graph_mul(graph, vert, curr_rep, curr_prev_vert)

    return result


@timer
def count_mul_paths(data: list) -> int:
    """Constructs a graph from the data and counts the number of possible paths
    from start to end without repeating vertices with uncapitalized names, 
    except one, which can be repeated once.

    Args:
        data: edges of the graph

    Returns:
        number of possible paths from start to end without repeating 
            uncapitalized vertices, except one, once.
    """

    graph = construct_graph(data)
    return run_through_graph_mul(graph)


def part2(test_data: list, data: list):
    """Solves the second part of the problem for day *INSERT DAY*.

    Args:
        test_data: small dataset provided to test the algorithm.
        data: dataset used to solve part 2 of the problem.
    """

    count_mul_paths(test_data)
    count_mul_paths(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file('test_input.txt')
    data = read_file('input.txt')

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)
