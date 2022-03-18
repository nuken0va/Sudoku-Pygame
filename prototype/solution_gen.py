import random
from itertools import product, chain

cells = [None for j in range(81)]
cells_step = [0 for j in range(81)]
cells_list = [[x for x in range(1,10)] for i in range(81)]


'''
def test_correct(cell: int) -> bool:
    x, y = cell % 9, cell // 9
    # Column except cell
    for i in chain(range(y), range(y + 1, 9)):
        yield self.grid[Solver.to_id(x, i)]
    # Row except cell
    for i in chain(range(x), range(x + 1, 9)):
        yield self.grid[Solver.to_id(i, y)]
    # Minigrid except row and column
    x_base, y_base = x - (x % 3), y - (y % 3)
    x, y = x % 3, y % 3
    for i, j in product(
            chain(range(x), range(x + 1, 3)),
            chain(range(y), range(y + 1, 3))
            ):
        yield self.grid[Solver.to_id(x_base + i, y_base + j)]
        
    for element in row: 
        if element and row.count(element) != 1: return False
    column = [cells[x][i] for i in range(9)] 
    for element in column: 
        if element and column.count(element) != 1: return False
    block = [cells[x - (x % 3) + j // 3][y - (y % 3) + j % 3]  for j in range(9)]
    for element in block: 
        if element and block.count(element) != 1: return False
    return True
'''

for cell in range(9):
    random.shuffle(cells_list[cell])

print(cells)
print(cells_step)
print(cells_list)

cell = 0
backtrack = False
while 0 <= cell < 81:
    if not backtrack:
        cells[cell] = cells_list[cell][cells_step[cell]  
        if test_correct(x,y):
            cell += 1
            print(cell)
            continue
    if cells_step[x][y] < 8:
        cells_step[x][y] += 1
        backtrack = False
    else: 
        cells_step[x][y] = 0
        cells[x][y] = None
        cell -= 1
        print(cell)
        backtrack = True
print(cells)