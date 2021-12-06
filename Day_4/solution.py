import functools as ft
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


def read_file(filename: str) -> str:
    """Opens a file and reads the numbers called during the bingo and the bingo
    cards (or tiles, as they shall be referred from here on).

    Args:
        filename: name of the file to read its input.

    Returns:
        : Numbers called during the bingo.
        : Tiles (bingo cards). 
    
    Requires:
        filename must the name of a valid file.
        numbers called during the bingo should be separated from the first tile
            by an empty line.
        tiles should be separated from each other with an empty line.
    """

    with open(filename) as datafile:
        data = datafile.read().split("\n\n")
    
    numbers, *tiles = data
    
    return (list(map(int, numbers.split(","))), 
            [list(map(int, tile.split())) for tile in tiles])


###############################################################################
# Part 1

def prepare_data(tiles: list) -> list:
    """Converts the numbers on each tile card into a dictionary where the keys
    are the numbers and the values are the positions (coordinates) of where we
    can find those numbers in the specific tile. Additionally, per tile, it also
    creates a list of the number of values unmarked in each line and a list of
    the number of values unmarked in each column.

    Args:
        tiles: bingo cards used during the calling of the numbers.

    Returns:
        prep_tiles: list of tuples where each tuple contains information 
            relative to one tile. The tuple contains a dictionary, with the 
            numbers in the keys and their position on the tile as their value,
            it contains a list with the number of unmarked numbers in the 
            columns of the tile and it contains a list of the number of unmarked
            numbers in the lines of the tiles.
    """

    prep_tiles = []
    for tile in tiles:
        cols = [0 for _ in range(5)]
        lines = [0 for _ in range(5)]

        corr_tiles = {}
        for index, value in enumerate(tile):
            cols[index % 5] += 1
            lines[index // 5] += 1

            if value not in corr_tiles:
                corr_tiles[value] = []
            corr_tiles[value].append((index % 5, index // 5))
        
        prep_tiles.append((corr_tiles, cols, lines))
    
    return prep_tiles


def find_num(num: int, tile: tuple) -> tuple:
    """Marks a number in the tile.

        It removes the number from the dictionary of numbers and their positions
    in the tiles and it decreases the number of unmarked numbers in the lists of
    the numbers of unmarked numbers per line and per column.

    Args:
        num: number to be marked (removed from the dictionary).
        tile: information regarding the bingo card: dictionary of unmarked 
            numbers and their positions in the tile, list of the number of 
            unmarked numbers per column and list of the number of unmarked 
            numbers per line.

    Returns:
        empty_col_or_line (bool): indicates if the tile has any fully marked 
            column or line. If the flag is true, then the tile has has a fully
            marked column or line.
        tile_values (dict[int: tuple]): unmarked numbers in the tile associated
            with their positions.
        cols (list[int]): number of unmarked numbers in the tile per column.
        lines (list[int]): number of unmarked numbers in the tile per line.

    Requires:
        the tiles should be 5x5, i.e., the tiles should have 5 lines (or rows)
            and should have 5 columns.
    """

    tile_values, cols, lines = tile
    empty_col_or_line = False

    if num in tile_values:
        t_col, t_line = tile_values[num].pop()
        cols[t_col] -= 1
        lines[t_line] -= 1

        if len(tile_values[num]) == 0:
            del tile_values[num]

        if cols[t_col] < 1 or lines[t_line] < 1:
            empty_col_or_line = True

    return (empty_col_or_line, tile_values, cols, lines)


def run_bingo(numbers: list, tiles: list) -> int:
    """Runs the bingo game until some tile has won the game.

        For every number that is called, it marks that number in each tile if
    they have it and then it verifies if any tile has won the game. A game is
    won when a line or column of numbers is fully marked. When this happens, it
    returns the product of the sum of the unmarked numbers of the winning tile
    and the number that made that tile win the game.

    Args:
        numbers: numbers to be called during the bingo game.
        tiles: information relative to each tile.

    Raises:
        ValueError: since the game has to finish after all the numbers have been
            called, it doesn't make sense for the game to not terminate. 
            Therefore, it raises and exception indicating that something did not
            go well.

    Returns:
        : product of the sum of the unmarked numbers of the winning tile and the
        number that made that tile win the game.
    """

    for num in numbers:
        result = list(map(ft.partial(find_num, num), tiles))
        
        tiles = []
        for sol, tile, cols, lines in result:
            if sol:
                return sum(tile.keys())*num
            tiles.append((tile, cols, lines))

    raise ValueError("run_bingo failed")


@timer
def find_fst_winner(data: tuple) -> int:
    """Finds the result of the bingo game, according to the tiles and the 
    numbers in the data.

    Args:
        data: numbers to be called during the bingo game and the information
            regarding the tiles.

    Returns:
        : result of the game.
    """

    numbers, tiles = data
    return run_bingo(numbers, prepare_data(tiles))


def part1(test_data, data):
    """Solves the first part of the problem for day 4.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 1 of the problem
    """

    find_fst_winner(test_data)
    find_fst_winner(data)


###############################################################################
# Part 2

def run_bingo_until_last(numbers: list, tiles: list) -> int:
    """Runs the bingo game until the last tile has won the game.

        For every number that is called, it marks that number in each tile if
    they have it and then it verifies if any tile has won the game. When the 
    last tile wins the game, it returns the product of the sum of the unmarked 
    numbers of that tile and the number that made that tile win the game.

    Args:
        numbers: numbers to be called during the bingo game.
        tiles: information relative to each tile.

    Raises:
        ValueError: since the game has to finish after all the numbers have been
            called, it doesn't make sense for the game to not terminate. 
            Therefore, it raises and exception indicating that something did not
            go well.

    Returns:
        : product of the sum of the unmarked numbers of the last winning tile 
            and the number that made that tile win the game.
    """

    for num in numbers:
        result = list(map(ft.partial(find_num, num), tiles))
        
        tiles = []
        for sol, tile, cols, lines in result:
            if not sol:
                tiles.append((tile, cols, lines))
        
        if len(tiles) == 0:
            return sum(result[0][1].keys())*num

    raise ValueError("run_bingo_until_last failed")


@timer
def find_last_winner(data: tuple) -> int:
    """Finds the result of the last winner of the bingo game, according to the 
    tiles and the numbers in the data.

    Args:
        data: numbers to be called during the bingo game and the information
            regarding the tiles.

    Returns:
        : result of the last winner of the game.
    """

    numbers, tiles = data
    return run_bingo_until_last(numbers, prepare_data(tiles))


def part2(test_data, data):
    """Solves the second part of the problem for day 4.

    Args:
        test_data: small dataset provided to test the algorithm
        data: dataset used to solve part 2 of the problem
    """

    find_last_winner(test_data)
    find_last_winner(data)


###############################################################################

if __name__ == '__main__':
    test_data = read_file("test_input.txt")
    data = read_file("input.txt")

    print("Part 1 " + "-"*30)
    part1(test_data, data)
    print("\nPart 2 " + "-"*30)
    part2(test_data, data)