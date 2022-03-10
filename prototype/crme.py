from itertools import product
import random
from dataclasses import dataclass, field

@dataclass
class Cell:
    index : int
    value : int
    suggestions : list = field(default_factory=list)

def get_sudoku(grid):
    sudoku = []
    for ind, el in enumerate(grid):
        sudoku.append(Cell(ind, el,[1,2,3,4,5,6,7,8,9]))
    return sudoku

def get_id(x,y):
    return x + y * 9

def range_column(cells, x, start = 0, end = 9):
    for i in range(start, end):
        yield cells[get_id(x, i)]

def range_row(cells, y, start = 0, end = 9):
    for i in range(start, end):
        yield cells[get_id(i, y)]

def range_minigrid(cells, x = None, y = None, index = None, start = 0, end = 9):
    if index is not None:
        x, y = (index % 3) * 3, index - (index % 3)
    else:
        x, y = x - (x % 3), y - (y % 3)
    for i in range(start, end):
        j, k = i % 3, i // 3
        yield cells[get_id(x + j, y + k)]


def old_crme(cells):
    for cell in range(81):
        sug = [True for i in range(9)]
        x, y = cell // 9, cell % 9
        if cells[get_id(x,y)].value:
            continue
        for i in range(9):
            for value in [cells[get_id(x,i)].value, 
                          cells[get_id(i,y)].value, 
                          cells[get_id(x - (x % 3) + (i // 3),y - (y % 3) + (i % 3))].value]:
                if value and sug[value - 1]: sug[value - 1] = False
        if sug.count(True) == 1:
            value = sug.index(True) + 1
            cells[get_id(x,y)].value = value
            return True
        else: 
            cells[get_id(x,y)].suggestions = sug
        cells[get_id(x,y)].suggestions = sug
    return False

def crme(cells):
    for cell in range(81):
        sug = [True for i in range(9)]
        x, y = cell // 9, cell % 9
        if cells[get_id(x,y)].value:
            continue
        for other in range_column(cells, x):
            if other.value and sug[other.value - 1]: sug[other.value - 1] = False
        for other in range_row(cells, y):
            if other.value and sug[other.value - 1]: sug[other.value - 1] = False
        for other in range_minigrid(cells, x, y):
            if other.value and sug[other.value - 1]: sug[other.value - 1] = False
        if sug.count(True) == 1:
            value = sug.index(True) + 1
            cells[get_id(x,y)].value = value
            print(f"crme {x}, {y}, value {value}")
            return True
        else: 
            cells[get_id(x,y)].suggestions = sug
        #cells[get_id(x,y)].suggestions = sug
    return False

def lr(cells):
    for digit, i in product(range(9), repeat=2):
        group = [cell for cell in range_column(cells, i) 
                if not cell.value and cell.suggestions[digit]]
        if len(group) == 1: 
            group[0].value = digit + 1
            print(f"lr_column_{i}, value {digit + 1}")
            return True
        group = [cell for cell in range_row(cells, i)
                if not cell.value and cell.suggestions[digit]]
        if len(group) == 1: 
            group[0].value = digit + 1
            print(f"lr_row_{i}, value {digit + 1}")
            return True
        group = [cell for cell in range_minigrid(cells, index=i)
                if not cell.value and cell.suggestions[digit]]
        if len(group) == 1: 
            group[0].value = digit + 1
            print(f"lr_minigrid_{i}, value {digit + 1}")
            return True
    return False

def build_group(cells,
                g_size,
                group,
                suggestions,
                block,
                block_index,
                start,
                depth = 0):
    if len(group) == g_size:
        return(group, suggestions)
    for ind, cell in enumerate(block(
        cells,
        index = block_index, 
        start = start,
        end = 9 - (g_size - len(group)) + 1
        )):
        print("\t"*depth+f"Cell-{cell.index}", end="\t")
        if len(cell.suggestions) <= g_size and all(elem in suggestions for elem in cell.suggestions):
            group.append(cell)
            print(f"Sutable: Suggestions group grows {group = }")
            result = build_group(cells, g_size, group, suggestions, block, block_index, start + 1 + ind, depth + 1)
        elif len(suggestions) < g_size:
            new_sug = list(set(suggestions + cell.suggestions))
            if len(new_sug) <= g_size:
                group.append(cell)
                print(f"Sutable: Suggestions group grows {new_sug = }, {group = }")
                result = build_group(cells, g_size, group, new_sug, block, block_index, start + 1 + ind, depth + 1)
            else: 
                print("Not sutable: Suggestions group is too big")
                continue
        else: 
            print("Not sutable")
            continue
        # This part is only achivable if group.append() was called
        if result != (None, None): return result
        group.pop()
        print("\t"*depth+f"Rollback: {group},{suggestions}")
    return None, None

sudoku = get_sudoku([None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None,])

sudoku[get_id(5,3)].suggestions = [1,2,4]
sudoku[get_id(5,4)].suggestions = [1,4,5]
sudoku[get_id(4,5)].suggestions = [1,2]
sudoku[get_id(5,5)].suggestions = [1,2,3]
sudoku[get_id(3,5)].suggestions = [1,2,3]

print(build_group(cells = sudoku,
            g_size = 4,
            group = [],
            suggestions = [],
            block = range_minigrid,
            block_index = 4,
            start = 0
            ))
'''
for i in range(50):
    random.choice(example_sudoku).value = None
'''



"""
for _ in range(40):
    print()
    for i in range(9):
        for j in range(9):
            if example_sudoku[get_id(i,j)].value:
                print(example_sudoku[get_id(i,j)].value, end=" ")
            else: print(end="  ")
        print()
    if crme(sudoku):
        continue
    if lr(sudoku):
        continue
    break

    """

missing = 0
for i in range(9):
    for j in range(9):
        if sudoku[get_id(i,j)].value:
            print(sudoku[get_id(i,j)].value, end=" ")
        else: 
            missing += 1
            print(end="  ")
            #print(sudoku[get_id(i,j)].suggestions,end=" ")
    print()
print(f"Missing {missing}")



'''
[None, 8, None, None, None, None, 1, None, 9,
    6, 4, None, None, None, 1, None, 3, 7,
    None, 7, None, 8, 3, None, None, None, None,
    7, None, 1, None, None, 3, None, 4, None,
    None, None, 5, None, None, None, None, 8, 3,
    4, None, None, 6, None, 5, None, None, None,
    9, None, None, None, 6, 2, None, None, 8,
    None, 1, None, None, None, 9, None, None, None,
    None, 2, 4, 7, None, 8, 5, None, None]
    '''