import functools as ft
import multiprocessing as mp
import time


##############################################################################

def read_file(filename: str) -> list:
    """Opens a file and reads it into a list.

    Args:
        filename: name of the file to read its input.

    Returns:
        data: list of lines of the files as strings.
    
    Requires:
        filename must the name of a valid file.
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    return data


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

def sum_till_half(data: list, index: int) -> tuple:
    """Determines the most common value in the column.

    Args:
        data: data in which to find the most common value in one of its columns.
        index: index of the column of the data to determine its most common 
            value.

    Returns:
        index: index of the column the result applies to.
        : most common value in column.
    
    Requires:
        the only possible values for elements of the column of the data are 0
            and 1.
    """
    
    result = 0
    half_length = len(data) // 2
    for row in data:
        result += int(row[index])
        if result > half_length:
            return (index, "1")
    
    return (index, "0")


def find_gamma(data: list) -> str:
    """Finds the most common element in each column of the data (using 
    multiprocessing) and generates a binary number where at each position there
    is the most common number of each column of the same index.

    Args:
        data: data from which the columns are used to generate the binary 
            number.

    Returns:
        : binary number of the most common number per column of the data.
    
    Requires:
        each element of the data must contain only 1s and 0s.
    """

    with mp.Pool(2) as p:
        sums = p.map(ft.partial(sum_till_half,data), 
                        range(len(data[0])))
    
    list_result = [0 for i in range(len(sums))]
    for index, value in sums:
        list_result[index] = value
    
    return "".join(list_result)


def invert_bin_2_int(bin_num: str) -> int:
    """Inverts the bits of a binary number and converts the resulting binary
    number into an int.
    """

    result = ""
    for i in bin_num:
        result += "1" if i == "0" else "0"
    return int(result, 2)


@timer
def determ_gamma_epsilon(data: list) -> int:
    """It calculates the product of the gamma and epsilon values obtained from 
    the data given.

    Args:
        data: data from which the gamma and epsilon values are to be obtained.

    Returns:
        : product of the gamma and epsilon values.
    """
    gamma = find_gamma(data)
    return invert_bin_2_int(gamma) * int(gamma, 2)


def part1(test_data: list, data: list):
    """Solves the first part of the problem for day 3.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    determ_gamma_epsilon(test_data)
    determ_gamma_epsilon(data)


##############################################################################
# create a Prefix Tree (or Trie) class

class TrieNode():
    """Node of the Prefix Tree (or Trie) data structure.
    """

    def __init__(self, next_nodes: dict):
        self.next = next_nodes
    

    def is_empty(self) -> bool:
        """Determines if the current node, has any child nodes. If it hasn't it
        returns true, and false, otherwise.
        """
        return len(self.next) == 0



def add_trie_node(node: TrieNode, key: str):
    """Adds a node to a another trie node or to a trie.

    Args:
        node: trie node or trie to which add a node.
        key: value of the node and each child node it must have before 
            adding it to the trie or trie node.
    """

    value, *rest = key

    if len(rest) > 0:
        if value in node.next:
            node.next[value][0] += 1
        else:
            node.next[value] = [1, TrieNode({})]
        add_trie_node(node.next[value][1], rest)
    
    elif value in node.next:
        node.next[value][0] += 1
    else:
        node.next[value] = [1, TrieNode({})]


def generate_trie(trie_nodes: list) -> TrieNode:
    """Generates a prefix tree (or trie).

    Args:
        trie_nodes: keys to add to the prefix tree being generated

    Returns:
        root: root node of the prefix tree.
    """

    root = TrieNode({})
    for key in trie_nodes:
        add_trie_node(root, key)
    return root



##############################################################################
# part 2

def get_trie_values(trie_node: TrieNode) -> list:
    """Generates a list of the possible values the a key can have starting from
    the current node. 
        THIS FUNCTION IS ONLY USED FOR DEBUGGING.

    Args:
        trie_node: starting point from which to determine the possible keys.

    Returns:
        result: list of keys that are in the trie that takes the trie_node as 
        the root node.
    """

    if trie_node.is_empty():
        return [""]
    result = []

    for i in trie_node.next:
        for j in get_trie_values(trie_node.next[i][1]):
            result.append(i+j)
    return result


def find_common(trie_root: TrieNode, most) -> str:
    """Finds either the most common value or the least common value at each 
    child node with the most (or least, respectively) common value and returns 
    the key formed by concatenating these values. If a node as only one value, 
    that value is concatenated into the key. If a node doesn't have any values, 
    that returns an empty string or finalizes the key.

    Args:
        trie_root: node from which to obtain the most (or least) common value at
            each one of its child nodes to form the key.
        most: flag that indicates if the most common value is wanted or if the
            least common value is wanted. If it is set to true, it will obtain
            keys based on the most common value.

    Returns:
        : key obtained by recursively obtaining the most (or least) common value
        at each child node with the most (or least, respectively) common value. 
    """

    next_values = trie_root.next
    
    if len(next_values) == 0:
        return ""
    elif len(next_values) == 1:
        value = list(next_values.keys())[0]
        return value + find_common(trie_root.next[value][1], most)
    else:
        fst, fst_node = next_values["0"]
        snd, snd_node = next_values["1"]
        
        if most:
            if fst <= snd:
                return "1" + find_common(snd_node, most)
            return "0" + find_common(fst_node, most)
        if fst <= snd:
            return "0" + find_common(fst_node, most)
        return "1" + find_common(snd_node, most)


@timer
def obtain_ox_diox_gen(data: list) -> int:
    """Obtains the oxygen generator and the CO2 scrubber rating.

    Args:
        data: data from which to obtain the oxygen generator and the CO2 
            scrubber rating.

    Returns:
        : product of the oxygen generator and the CO2 scrubber rating. 
    """

    root = generate_trie(data)
    ox_gen = int(find_common(root, True), 2)
    diox_gen = int(find_common(root, False), 2)

    return ox_gen * diox_gen


def part2(test_data: list, data: list):
    """Solves the second part of the problem for day 3.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 2 of the problem
    """

    obtain_ox_diox_gen(test_data)
    obtain_ox_diox_gen(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file("test_input.txt")
    data = read_file("input.txt")
    
    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)