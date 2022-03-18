from enum import unique
from itertools import product, chain
from typing import ClassVar
import random
from dataclasses import dataclass, field


@dataclass
class Cell:
    index: int
    value: int
    candidates: set

    def __hash__(self):
        return hash(self.index)


@dataclass
class Step:
    method: str
    description: dict

class Solver():
    grid: list[Cell]
    solution_exists: bool = True
    steps: list[Step]

    def to_id(x, y):
        """Converts x,y coordinates of cell to cell id (index)"""
        return x + y * 9

    def to_cord(index):
        """Converts cell id (index) of cell to  its x,y coordinates"""
        return index // 9, index % 9

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

    def check_candidates(self):
        """
        Returns True if every empty cell has at least 1 candidate
        """
        return all(cell.value or len(cell.candidates) for cell in self.grid)

    def __init__(self, input):
        self.grid = []
        self.steps = []
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
        elif type(input) == Solver:
            for el in input.grid:
                self.grid.append(Cell(el.index,
                                      el.value,
                                      el.candidates.copy()))

    def range_column(self, index, start=0, end=9):
        for i in range(start, end):
            yield self.grid[Solver.to_id(index, i)]

    def range_row(self, index, start=0, end=9):
        for i in range(start, end):
            yield self.grid[Solver.to_id(i, index)]

    def range_minigrid(self, index, start=0, end=9):
        x, y = (index % 3) * 3, index - (index % 3)
        for i in range(start, end):
            j, k = i % 3, i // 3
            yield self.grid[Solver.to_id(x + j, y + k)]

    def range_neighbours(self, cell: Cell):
        x, y = cell.index % 9, cell.index // 9
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

    def update_grid(self, cell):
        """
        Deletes cell.value from cell neighbours' candidates
        """
        for other in self.range_neighbours(cell):
            other.candidates.discard(cell.value)

    def __set_value(self, cell, value):
        cell.value = value
        cell.candidates = set()
        self.update_grid(cell)

    def init_candidates(self):
        """
        CRME method.
        Scans neighbor cells to eliminate candidates
        """
        for cell in self.grid:
            if cell.value:
                continue
            for other in self.range_neighbours(cell):
                cell.candidates.discard(other.value)
        return False

    def naked_singles(self):
        """
        Naked Singles method
        Fill the cells that only have 1 candidate 
        """
        for cell in self.grid:
            if cell.value:
                continue
            if len(cell.candidates) == 1:
                value = cell.candidates.pop()
                self.steps.append(Step("Naked Single", {"id": cell.index, "value": value}))
                self.__set_value(cell, value)
                return True
        return False


    def hidden_singles(self):
        """
        Hidden Singles method
        Scans candidates of all cells in row/column/minigrid
        to find unique ones
        """
        for digit, i in product(range(1, 10), range(9)):
            for block in [self.range_column(i),
                          self.range_row(i),
                          self.range_minigrid(i)
                          ]:
                group = [cell for cell in block
                         if not cell.value and digit in cell.candidates]
                if len(group) == 1:
                    cell = group[0]
                    self.steps.append(Step("Hidden Single", {"id": cell.index, "value": digit}))
                    self.__set_value(cell, digit)
                    return True
        return False

    def __build_group(self, group_size,
                      block, block_index,
                      group=None, candidates=None,
                      start=0,
                      depth=0
                      ):
        """
        This method is only called by group_elimination
        recursively builds group within block(block_index)
        with size of group_size
        """
        # Initialization
        if group is None or candidates is None:
            group, candidates = [], set()
        # Exit conditions
        if len(group) == group_size:
            return(group, candidates)
        # For the remaining cells in block
        for inc, cell in enumerate(block(index=block_index,
                                         start=start,
                                         end=9 - (group_size - len(group)) + 1
                                         )):
            if cell.value:
                continue
            if cell.candidates.issubset(candidates):
                # Candidate list doesn't need to be expanded
                group.append(cell)
                result = self.__build_group(group_size,
                                            block, block_index,
                                            group, candidates,
                                            start + 1 + inc,
                                            depth + 1
                                            )
            elif len(candidates) < group_size:
                # Candidate list can be expanded
                new_candidates = candidates.union(cell.candidates)
                if len(new_candidates) > group_size:
                    continue
                group.append(cell)
                result = self.__build_group(group_size,
                                            block, block_index,
                                            group, new_candidates,
                                            start + 1 + inc,
                                            depth + 1
                                            )
            else:
                continue
            # This code is reachable only if group.append() was called
            if result != (None, None):
                return result
            # Discard last group expansion
            group.pop()
        return None, None

    def group_elimination(self, group_size):
        """
        Group Elimination method
        aka Naked Doubles/Triples/Quads
        Scans candidates of all cells in row/column/minigrid
        to find naked indpendend groups
        """
        updated = False
        for i, block in product(range(9), [self.range_row,
                                           self.range_column,
                                           self.range_minigrid]
                                ):
            group, candidates = self.__build_group(group_size, block, i)
            if group is None or candidates is None:
                continue
            for cell in block(i):
                if (cell in group
                        or not cell.candidates.intersection(candidates)):
                    continue
                updated = True
                cell.candidates.difference_update(candidates)
            if updated:
                self.steps.append(Step(f"Naked Group({group_size})", {"ids": [cell.index for cell in block(i) if cell not in group], "values": candidates}))
                return True
        return False

    def __omission(self, main, secondary):
        """
        This method is only called by all_omissions
        searches for omission of secondary using main
        """
        found = False
        i, d = set(), set()
        for cell in main.intersection(secondary):
            i.update(cell.candidates)
        for cell in main.difference(secondary):
            d.update(cell.candidates)
        unique = i.difference(d)
        if not unique:
            return found
        for cell in secondary.difference(main):
            dif = cell.candidates.intersection(unique)
            if not dif:
                continue
            found = True
            cell.candidates.difference_update(unique)
        return found

    def all_omissions(self):
        """
        Omissions method
        """
        for x, y, offset in product(
                range(0, 9, 3),
                range(0, 9, 3),
                range(3)):
            result = False
            column = set(self.range_column(x + offset))
            row = set(self.range_row(y + offset))
            grid = set(self.range_minigrid(Solver.get_minigrid_id(x, y)))
            result |= self.__omission(column, grid)
            result |= self.__omission(row, grid)
            result |= self.__omission(grid, column)
            result |= self.__omission(grid, row)
            if result:
                self.steps.append(Step("Omission", {"grid": Solver.get_minigrid_id(x, y), "column": x + offset, "row":  y + offset}))
                return True
        return False

    def __build_hidden_group(self, group_size,
                             digit_cells,
                             group=None,
                             suggestion=None,
                             start=1,
                             depth=0
                             ):
        """
        This method is only called by group_elimination
        recursively builds group within block(block_index)
        with size of group_size
        """
        # Initialization
        if group is None or suggestion is None:
            suggestion, group = set(), set()
        # Exit conditions
        if len(group) == group_size and len(suggestion) == group_size:
            return group, suggestion
        # For the remaining digits
        for digit in range(start, 9):
            if not digit_cells[digit] or len(digit_cells[digit]) > group_size:
                continue
            new_group = group.union(digit_cells[digit])
            suggestion.add(digit + 1)
            result = self.__build_hidden_group(group_size=group_size,
                                               digit_cells=digit_cells,
                                               group=new_group,
                                               suggestion=suggestion,
                                               start=digit + 1,
                                               depth=depth + 1)
            if result != (None, None):
                return result
            suggestion.remove(digit + 1)
        return None, None

    def hidden_group_elimination(self, group_size):
        for i, block in product(range(9), [self.range_row,
                                           self.range_column,
                                           self.range_minigrid]
                                ):
            digits = []
            found, updated = False, False
            for digit in range(1, 10):
                digits.append([cell for cell in block(i)
                               if (not cell.value)
                               and digit in cell.candidates]
                              )
            group, candidates = self.__build_hidden_group(group_size, digits)
            if group is None or candidates is None:
                continue
            for cell in group:
                if not cell.candidates.difference(candidates):
                    continue
                updated = True
                cell.candidates.intersection_update(candidates)
            if updated:
                self.steps.append(Step(f"Hidden Group({group_size})", {"ids": [cell.index for cell in block(i) if cell not in group], "values": candidates}))
                return True
        return False

    def brute_force(self, first=True):
        bf = min((cell for cell in self.grid if not cell.value), key=lambda cell: len(cell.candidates))
        total_colutions = 0
        self.print_sudoku(True)
        for candidate in bf.candidates:
            print(f"Brute Force cell {bf.index}: try {candidate}")
            self.grid[bf.index] = Cell(bf.index, candidate, set())
            solver = Solver(self)
            solution_count, difficulty = solver.solve(first)
            print(f"Brute Force {solution_count = }")
            if solution_count:
                if first:
                    self.grid = solver.grid
                    self.steps.append(Step("Brute Force", {"size":len(bf.candidates), "id": bf.index, "value": candidate}))
                    self.steps += solver.steps
                    return solution_count, difficulty
                else:
                    total_colutions += solution_count
            print(f"Brute Force rolledback")
        if first:
            return 0, -1
        else:
            return total_colutions, difficulty

    def old_print_sudoku(self, dbg=False):
        missing = 0
        for row in range(9):
            for column in range(9):
                if self.grid[Solver.to_id(column, row)].value:
                    print(self.grid[Solver.to_id(column, row)].value, end=" ")
                else:
                    missing += 1
                    if dbg:
                        print(self.grid[Solver.to_id(column, row)].candidates, end=" ")
                    else:
                        print(end="  ")
            print()
        print(f"Missing {missing}")
    
    def print_sudoku(self, dbg=False):
        for row in range(9):
            for column in range(9):
                if self.grid[Solver.to_id(column, row)].value:
                    print("┌─┐", end="")
                else:
                    for i in range(1, 4):
                        if i in self.grid[Solver.to_id(column, row)].candidates:
                            print(i, end="")
                        else:
                            print(" ", end="")

            print()
            for column in range(9):
                if self.grid[Solver.to_id(column, row)].value:
                    print(f"│{self.grid[Solver.to_id(column, row)].value}│", end="")
                else:
                    for i in range(4, 7):
                        if i in self.grid[Solver.to_id(column, row)].candidates:
                            print(i, end="")
                        else:
                            print(" ", end="")

            print()
            for column in range(9):
                if self.grid[Solver.to_id(column, row)].value:
                    print("└─┘", end="")
                else:
                    for i in range(7, 10):
                        if i in self.grid[Solver.to_id(column, row)].candidates:
                            print(i, end="")
                        else:
                            print(" ", end="")
            print()
        print()

    def solve(self, first = True):
        """
        Retruns (solution_count, difficulty)
        """
        difficulty = 0
        solution_count = 0
        self.init_candidates()
        while Solver.get_free(self.grid) and self.check_candidates():
            #self.print_sudoku()
            #print(self.steps)
            if self.naked_singles():
                difficulty += 1
            elif self.hidden_singles():
                difficulty += 2
            elif (self.all_omissions()
                    or self.group_elimination(2)):
                difficulty += 3
            elif (self.group_elimination(3)
                    or self.hidden_group_elimination(2)):
                difficulty += 4
            elif (self.group_elimination(4)
                    or self.hidden_group_elimination(3)
                    or self.hidden_group_elimination(4)):
                difficulty += 5
            else:
                solution_count, bf_difficulty = self.brute_force(first)
                if solution_count:
                    return solution_count, difficulty + bf_difficulty
                else:
                    return 0, -1
        if Solver.get_free(self.grid):
            return 0, -1
        else:
            return 1, difficulty


example_sudoku = [
None, None, None, None, None, 2, 5, None, None,
None, None, 8, None, None, None, None, None, None,
4, 9, None, 1, None, None, None, None, 6,

None, None, None, None, 9, None, None, 6, None,
None, 3, None, None, None, None, None, None, None,
7, 1, None, 4, None, None, None, None, 9,

None, None, 3, None, None, None, None, None, 7,
None, None, 6, 8, None, None, None, None, None,
8, 7, None, None, None, 1, None, 2, None
]

sudoku = Solver(example_sudoku)
sudoku.print_sudoku()
print(sudoku.solve())
for step in sudoku.steps:
    print(step)
sudoku.print_sudoku()


'''
def old_omission(cells):
    for x, y, index, digit in product(
            range(9,step=3),
            range(9,step=3),
            range(3),
            range(9)):
        # rows and minigrids
        c, o = set(), set()
        column = x + index
        for cell in range_column(cells,column, y, y + 3):
            c.union(cell.candidates)
        for other in chain(
                range(x, x+index),
                range(x+index+1, x+3)):
            for cell in range_column(cells,other, y, y + 3):
                o.union()
        unique = c.difference(o)
        if unique:
            for cell in chain(
                    range_column(cells,column, end = y),
                    range_column(cells,column, start = y + 3)
                    ):
                cell.candidates.difference_update(unique)
'''