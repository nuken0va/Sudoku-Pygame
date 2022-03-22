from itertools import chain, product
from typing import Callable, ClassVar, Iterator
from logic_cell import Cell


class Field():
    grid: list[Cell]
    CellGenerator: ClassVar = Callable[..., Iterator[Cell]]
    
    def __init__(self, input = None):
        self.grid = []
        if type(input) == list:
            for ind, el in enumerate(input):
                if el is None:
                    sug = {i for i in range(1, 10)}
                elif type(el) is set:
                    sug = el
                    el = None
                else:
                    sug = set()
                self.grid.append(Cell(ind, el, sug))
        elif type(input) == Field:
            for el in input.grid:
                self.grid.append(Cell(el.index,
                                      el.value,
                                      el.candidates.copy()))

    def get_minigrid_id(x, y):
        """
        Сalculates minigrid id by x,y coordinates of cell
        Minigrids ids:
        [0][1][2]
        [3][4][5]
        [6][7][8]
        """
        return y - (y % 3) + (x // 3)

    def get_free(block):
        """
        Returns ammount of cells without a value
        """
        return len([cell for cell in block if not cell.value])

    def range_column(self, index, start=0, end=9) -> Iterator[Cell]:
        for i in range(start, end):
            yield self[Cell.to_id(index, i)]

    def range_row(self, index, start=0, end=9):
        for i in range(start, end):
            yield self[Cell.to_id(i, index)]

    def range_minigrid(self, index, start=0, end=9):
        x, y = (index % 3) * 3, index - (index % 3)
        for i in range(start, end):
            j, k = i % 3, i // 3
            yield self[Cell.to_id(x + j, y + k)]

    def range_neighbours(self, cell: Cell):
        x, y = cell.index % 9, cell.index // 9
        # Column except cell
        for i in chain(range(y), range(y + 1, 9)):
            yield self[Cell.to_id(x, i)]
        # Row except cell
        for i in chain(range(x), range(x + 1, 9)):
            yield self[Cell.to_id(i, y)]
        # Minigrid except row and column
        x_base, y_base = x - (x % 3), y - (y % 3)
        x, y = x % 3, y % 3
        for i, j in product(
                chain(range(x), range(x + 1, 3)),
                chain(range(y), range(y + 1, 3))
                ):
            yield self[Cell.to_id(x_base + i, y_base + j)]

    def check_cell(self, cell: Cell):
        for other in self.range_neighbours(cell):
            if other.value == cell.value:
                return False
        return True

    def __str__(self):
        result = ""
        for row, substr in product(range(9), range(3)):
            for column in range(9):
                valstr = ["┌───┐",
                          f"│ {self[Cell.to_id(column, row)].value} │",
                          "└───┘"]
                if self[Cell.to_id(column, row)].value:
                    result += valstr[substr]
                else:
                    result += " "
                    for i in range(substr * 3 + 1, substr * 3 + 4):
                        if i in self[Cell.to_id(column, row)].candidates:
                            result += str(i)
                        else:
                            result += " "
                    result += " "
            result += "\n"
        return result
    
    def __getitem__(self, key): return self.grid[key]

    def __setitem__(self, key, value: Cell): self.grid[key] = value

    #def copy(self):
        #return Field(self.copy, self.value, self.candidates.copy())