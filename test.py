import random

cells = [[None for j in range(9)] for i in range(9)]
cells_step = [[0 for j in range(9)] for i in range(9)]
cells_list = [[[x for x in range(1,10)] for j in range(9)] for i in range(9)]

def test_correct(x : int, y : int) -> bool:
    row = [cells[i][y] for i in range(9)] 
    for element in row: 
        if element and row.count(element) != 1: return False
    column = [cells[x][i] for i in range(9)] 
    for element in column: 
        if element and column.count(element) != 1: return False
    block = [cells[x - (x % 3) + j // 3][y - (y % 3) + j % 3]  for j in range(9)]
    for element in block: 
        if element and block.count(element) != 1: return False
    return True

    

for column in range(9):
    for row in range(9):
        random.shuffle(cells_list[column][row])

print(cells)
print(cells_step)
print(cells_list)

cell = 0
backtrack = False
while 0 <= cell < 81:
    x, y = cell%9, cell//9
    if not backtrack:
        cells[x][y] = cells_list[x][y][cells_step[x][y]]  
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