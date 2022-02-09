import time
import collections as cls


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
        data: list of ten unique signal patterns and four digit output values.
    
    Requires:
        filename must be the name of a valid file.
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    
    return data


###############################################################################
# part 1

def find_wrong_braces(line: str, 
                        get_stack: bool=False) -> str or None or cls.deque:
    """If a line contains an incorrect closure, it returns the incorrect brace.
    Otherwise, it either returns None or the stack of the missing braces.

    Args:
        line: line to check the correctness of the braces
        get_stack (optional): in case a line has no incorrect closing braces, it
            indicates whether none should be returned or if the stack of missing 
            closing braces is returned. If true, returns None, otherwise, it
            returns the stack. Defaults to False.

    Returns:
        brace (str): incorrect brace
        braces_stack (cls.deque): stack of missing closing braces of the line
    """

    poss_braces = {'(': ')', '{': '}', '[': ']', '<': '>'}
    braces_stack = cls.deque()
    
    for brace in line:
        if brace in poss_braces:
            braces_stack.append(poss_braces[brace])
        else:
            curr_brace = braces_stack.pop()
            if brace != curr_brace:
                return brace
    
    if get_stack:
        return braces_stack


@timer
def get_incorrect_score(data: list) -> int:
    """Finds the score of the wrong parenthesis of each line of the data and 
    returns its sum.

    Args:
        data (list[str]): lines of braces

    Returns:
        score: total score of the wrong braces in the data
    """

    braces = {')': 3, ']': 57, '}': 1197, '>': 25137}

    score = 0
    for line in data:

        wrong_brace = find_wrong_braces(line)

        if wrong_brace:
            score += braces[wrong_brace]
    
    return score


def part1(test_data: list, data: list):
    """Solves the second part of the problem for day 10.

    Args:
        test_data (list[str]): small dataset provided to test the 
            algorithm.
        data (list[str]): dataset used to solve part 1 of the problem.
    """

    get_incorrect_score(test_data)
    get_incorrect_score(data)


###############################################################################
# part 2

@timer
def get_correct_score(data: list) -> int:
    """Obains the score associated with the braces left in the stack of 
    incomplete lines (that do not have a wrong parenthesis) of each line.

    Args:
        data (list[str]): lines of braces

    Returns:
        score of the median value 
    """

    braces_score = {')': 1, ']': 2, '}': 3, '>': 4}
    
    results = []
    for line in data:
        line_score = 0
        
        braces_stack = find_wrong_braces(line, True)
        if type(braces_stack) is str:
            continue
        
        while len(braces_stack) != 0:
            line_score = line_score * 5 + braces_score[braces_stack.pop()]
        
        results.append(line_score)
    
    return sorted(results)[len(results) // 2]


def part2(test_data: list, data: list):
    """Solves the second part of the problem for day 10.

    Args:
        test_data (list[str]): small dataset provided to test the 
            algorithm.
        data (list[str]): dataset used to solve part 2 of the problem.
    """

    get_correct_score(test_data)
    get_correct_score(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file('test_input.txt')
    data = read_file('input.txt')

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)