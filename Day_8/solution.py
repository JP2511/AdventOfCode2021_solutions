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
        data: list of ten unique signal patterns and four digit output values.
    
    Requires:
        filename must be the name of a valid file.
    """

    with open(filename, 'r', encoding='utf8') as datafile:
        data = datafile.read().splitlines()
    return data


###############################################################################
# part 1

def count_uniq(line: str) -> int:
    """Counts the words that correspond to numbers that are represented using a
    unique number of letters per line in the four digit output values.

    Args:
        line: single set of ten unique signal patterns and four digit output 
            values

    Returns:
        counter: number of numbers that are represented with a unique number of
            letters in the four digit output values.
    """

    uniq_dig = {2, 3, 4, 7}
    
    counter = 0
    for i in line.split("|")[1].split():
        if len(i) in uniq_dig:
            counter += 1
    
    return counter


@timer
def total_uniq(data: list) -> int:
    """Counts the number of numbers that are represented using a unique number 
    of letters in the four digit output values for the whole dataset.

    Args:
        data: list of ten unique signal patterns and four digit output values.

    Returns:
        total number of numbers that are represented using a unique number of 
            letters in the four digit output values.
    """

    return sum([count_uniq(line) for line in data])


def part1(test_data: list, data: list):
    """Solves the first part of the problem for day 8.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    total_uniq(test_data)
    total_uniq(data)


###############################################################################

def parse(raw_uniq_sig: str) -> dict:
    """Converts the ten unique signal pattern of each line into a dictionary of
    the length of each word associaded with a list of words that have that 
    length. The words stored as a set and not as string.

    Args:
        raw_uniq_sig: ten unique signal pattern.

    Returns:
        uniq_sig_pattern: dictionary where the keys correspond to the possible
            lengths of the unique signal patterns and the values are the list of
            words with that length, with the words stored as sets.
    """
    
    uniq_sig_pattern = {}
    for digit in raw_uniq_sig.split():
        length = len(digit)
        
        if length not in uniq_sig_pattern:
            uniq_sig_pattern[length] = [set(digit)]
        else:
            uniq_sig_pattern[length] += [set(digit)]
    
    return uniq_sig_pattern


def decoder(uniq_sig_pattern: dict) -> dict:
    """Generates a mapper of encoded values to decoded values of the ten unique
    signal pattern.

    Args:
        uniq_sig_pattern: dictionary where the keys correspond to the possible
            lengths of the unique signal patterns and the values are the list of
            words with that length, with the words stored as sets.

    Returns:
        dictionary where the encoded letters are mapped to a standard set of
            letters.
    """

    encoder = {'a': uniq_sig_pattern[3][0] - uniq_sig_pattern[2][0]}
    
    dg = uniq_sig_pattern[5][0].intersection(*uniq_sig_pattern[5][1:])
    dg -= encoder['a']
    
    encoder['d'] = dg & uniq_sig_pattern[4][0]
    encoder['g'] = dg - encoder['d']
    encoder['b'] = uniq_sig_pattern[4][0] - uniq_sig_pattern[2][0] - encoder['d']
    
    encoder['e'] = uniq_sig_pattern[7][0] - encoder['a'] - encoder['b']
    encoder['e'] -= encoder['d'] | encoder['g'] | uniq_sig_pattern[2][0]
    
    encoder['f'] = uniq_sig_pattern[2][0].intersection(*uniq_sig_pattern[6])
    encoder['c'] = uniq_sig_pattern[2][0] - encoder['f']
    
    return {list(encoder[decoded])[0]: decoded for decoded in encoder}


def decode(line: str) -> int:
    """Decodes the four digit ouput value based on the corresponding ten unique
    signal pattern.

    Args:
        line: four digit ouput value and corresponding ten unique signal
            pattern.

    Returns:
        decoded four digit ouput value.
    
    Requires:
        line should have the ten unique signal pattern separated from the four
            digit ouput value with the '|' character.
    """

    uniq_dig = {2: 1, 3: 7, 4: 4, 7: 8}
    cust_letter_encoder = {'a': 1, 'b': 10, 'c': 100, 'd': 1000, 'e': 10000, 
                        'f': 100000, 'g': 1000000}
    decoded_digits = {1110111: 0, 1011101: 2, 1101101: 3, 1101011: 5, 1111011: 6, 
                        1101111: 9}

    letter_decoder = decoder(parse(line.split("|")[0]))

    number = ""
    for word in line.split("|")[1].split():
        if len(word) in uniq_dig:
            number += str(uniq_dig[len(word)])
        else:
            encoding = sum([cust_letter_encoder[letter_decoder[letter]]
                            for letter in word])
            number += str(decoded_digits[encoding])
    
    return int(number)


@timer
def sum_decoded_output(data: list) -> int:
    """Decodes the four digit output values based on the corresponding ten 
    unique signal pattern and sums the results of the full dataset.

    Args:
        data: list of four digit output values and their associated ten unique
            signal pattern.

    Returns:
        sum of the decoded four digit output values.
    """

    return sum([decode(line) for line in data])


def part2(test_data: list, data: list):
    """Solves the second part of the problem for day 8.

    Args:
        test_data: small dataset provided to test the algorithm.
        data: dataset used to solve part 2 of the problem.
    """

    sum_decoded_output(test_data)
    sum_decoded_output(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file("test_input.txt")
    data = read_file("input.txt")
    
    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)