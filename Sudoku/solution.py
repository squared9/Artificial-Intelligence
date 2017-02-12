"""
Sudoku solver

This program solves arbitrary Sudoku puzzle utilizing the following techniques:
- only choice - automatically filling boxes that can have a single value only
- elimination - if one value is set, it removes that value from all boxes in the same unit(s)
- naked twins - if a unit has two values with the same two digits, those digits are removed in all other unit's boxes
- depth-first search - runs through different valid game boards until it finds solution, picks box with shortest number
- diagonal - enforces diagonal constraints by adding two diagonal units
"""

assignments = []
# set this flag to True to indicate you want to solve diagonal Sudoku instead of normal Sudoku
is_diagonal = True


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins_on_peers(values, box, box_peers):
    """
    Solves naked twins per one type of peers of a box
    :param values: grid values
    :param box: box
    :param box_peers: peers of a single type of a box
    :return: grid values with adjusted naked twins
    """
    value = values[box]

    twins = set()
    twins.add(box)

    # find all twins related to current box
    for box_peer in box_peers:
        if len(values[box_peer]) != 2:
            continue
        if values[box_peer] == value:
            twins.add(box_peer)

    # at least two twins
    if len(twins) < 2:
        return values

    for box_peer in box_peers:
        if box_peer in twins:
            continue
        # replace occurrence of all numbers from naked twins in this box
        for number in value:
            # assign_value(values, box_peer, values[box_peer].replace(number, ''))
            values[box_peer] = values[box_peer].replace(number, '')
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for box in boxes:
        # box must have exactly two values to be considered a twin
        if len(values[box]) != 2:
            continue
        values = naked_twins_on_peers(values, box, column_peers[box])
        values = naked_twins_on_peers(values, box, row_peers[box])
        values = naked_twins_on_peers(values, box, square_peers[box])
    return values


def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    :param A:
    :param B:
    :return:
    """
    return [s + t for s in A for t in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    row_units = [cross(r, cols) for r in rows]
    i = 0
    result = {}
    for row_unit in row_units:
        for unit in row_unit:
            value = grid[i]
            if value == ".":
                value = "123456789"
            result[unit] = value
            i += 1
    return result


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    single_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in single_boxes:
        value = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(value, '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    numbers = "123456789"
    for unit in unitlist:
        for number in numbers:
            options = [box for box in unit if number in values[box]]
            if len(options) == 1:
                values[options[0]] = number
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    values = naked_twins(values)
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)

        # Only Choice Strategy
        values = only_choice(values)

        # Naked Twins
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # previous solution was false; should not happen
    if values is False:
        return False

    # all boxes have exactly one number inside, likely solution
    if all(len(values[box]) == 1 for box in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities

    min = 10
    min_box = None
    min_value = None
    for box in values.keys():
        value = values[box]
        if len(value) > 1 and len(value) < min:
            min_box = box
            min_value = value
            min = len(value)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for number in min_value:
        sub_values = values.copy()
        sub_values[min_box] = number
        sub_values = search(sub_values)
        if sub_values != False:
            return sub_values
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
if is_diagonal:
    diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                  ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
else:
    diagonal_units = []
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
column_unit_set = dict((s, [u for u in column_units if s in u]) for s in boxes)
column_peers = dict((s, set(sum(column_unit_set[s],[]))-set([s])) for s in boxes)
row_unit_set = dict((s, [u for u in row_units if s in u]) for s in boxes)
row_peers = dict((s, set(sum(row_unit_set[s],[]))-set([s])) for s in boxes)
square_unit_set = dict((s, [u for u in square_units if s in u]) for s in boxes)
square_peers = dict((s, set(sum(square_unit_set[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

