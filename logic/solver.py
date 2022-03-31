from itertools import product
from typing import Optional

from logic.cell import Cell
from logic.field import Field
from logic.step import Step


class Solver():
    __field: Field
    solution_exists: bool = True
    steps: list[Step]
    fast_crme: bool = True

    def check_candidates(self) -> bool:
        """
        Returns True if every empty cell has at least 1 candidate
        """
        return all(cell.value or len(cell.candidates) for cell in self.__field.grid)

    def __init__(self, input=None, save_marks=False):
        if input:
            self.__field = Field(input, candidates=True, marks=save_marks)
        self.steps = []

    @property
    def field(self): return self.__field

    @field.setter
    def field(self, new_field): self.__field = Field(
        new_field, candidates=True)

    def update_grid(self, cell: Cell) -> None:
        """
        Deletes cell.value from cell neighbours' candidates
        """
        for other in self.__field.range_neighbours(cell):
            if other.value:
                continue
            other.candidates.discard(cell.value)
            if self.fast_crme and len(other.candidates) == 1:
                value = other.candidates.pop()
                self.steps.append(
                    Step("Naked Single", {"id": other.index, "value": value}))
                self.__set_value(other, value)

    def __set_value(self, cell: Cell, value: int) -> None:
        cell.value = value
        cell.candidates = None
        self.update_grid(cell)

    def init_candidates(self) -> None:
        """
        CRME method.
        Scans neighbor cells to eliminate candidates
        """
        for i, block in product(range(9), [self.__field.range_row,
                                           self.__field.range_column,
                                           self.__field.range_minigrid]
                                ):
            values = set(cell.value for cell in block(i) if cell.value)
            for cell in block(i):
                if cell.value:
                    continue
                cell.candidates.difference_update(values)

    def naked_singles(self) -> None:
        """
        Naked Singles method
        Fill the cells that only have 1 candidate 
        """
        for cell in self.__field.grid:
            if cell.value:
                continue
            if len(cell.candidates) == 1:
                value = cell.candidates.pop()
                self.steps.append(
                    Step("Naked Single", {"id": cell.index, "value": value}))
                self.__set_value(cell, value)
                return True
        return False

    def hidden_singles(self) -> None:
        """
        Hidden Singles method
        Scans candidates of all cells in row/column/minigrid
        to find unique ones
        """
        for digit, i in product(range(1, 10), range(9)):
            for block in [self.__field.range_column(i),
                          self.__field.range_row(i),
                          self.__field.range_minigrid(i)
                          ]:
                group = [cell for cell in block
                         if not cell.value and digit in cell.candidates]
                if len(group) == 1:
                    cell = group[0]
                    self.steps.append(
                        Step("Hidden Single", {"id": cell.index, "value": digit}))
                    self.__set_value(cell, digit)
                    return True
        return False

    def __build_group(self, group_size: int,
                      block: Field.CellGenerator, block_index: int,
                      group: Optional[list[Cell]] = None,
                      candidates: Optional[set[int]] = None,
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

    def group_elimination(self, group_size: int):
        """
        Group Elimination method
        aka Naked Doubles/Triples/Quads
        Scans candidates of all cells in row/column/minigrid
        to find naked indpendend groups
        """
        updated = []
        for i, block in product(range(9), [self.__field.range_row,
                                           self.__field.range_column,
                                           self.__field.range_minigrid]
                                ):
            group, candidates = self.__build_group(group_size, block, i)
            if group is None or candidates is None:
                continue
            for cell in block(i):
                if (cell in group
                        or cell.value
                        or not cell.candidates.intersection(candidates)):
                    continue
                updated.append(cell)
                cell.candidates.difference_update(candidates)
            if updated:
                self.steps.append(Step(f"Naked Group", {"group_size": group_size, "ids": [
                                  cell.index for cell in updated], "values": candidates}))
                return True
        return False

    def __omission(self, main: set[Cell], secondary: set[Cell]):
        """
        This method is only called by all_omissions
        searches for omission of secondary using main
        """
        updated = []
        # All candidates from intersection (i)
        # and difference (d) of houses
        i, d = set(), set()
        for cell in main.intersection(secondary):
            if cell.value:
                continue
            i.update(cell.candidates)
        for cell in main.difference(secondary):
            if cell.value:
                continue
            d.update(cell.candidates)
        # Unique candidates in houses intersection
        # (relatively to main house)
        unique = i.difference(d)
        if not unique:
            return False
        # If unique values exist => delete them from secondary house
        for cell in secondary.difference(main):
            if cell.value:
                continue
            dif = cell.candidates.intersection(unique)
            if not dif:
                continue
            updated.append(cell)
            cell.candidates.difference_update(unique)
        if updated:
            self.steps.append(
                Step("Omission", {"ids": [cell.index for cell in updated], "values": unique}))
            return True
        return False

    def all_omissions(self):
        """
        Omissions method
        """
        for x, y, offset in product(
                range(0, 9, 3),
                range(0, 9, 3),
                range(3)):
            result = False
            column = set(self.__field.range_column(x + offset))
            row = set(self.__field.range_row(y + offset))
            grid = set(self.__field.range_minigrid(
                Field.get_minigrid_id(x, y)))
            if (self.__omission(column, grid)
                    or self.__omission(row, grid)
                    or self.__omission(grid, column)
                    or self.__omission(grid, row)):
                return True
        return False

    def __build_hidden_group(self, group_size: int,
                             digit_cells: list[Cell],
                             group: Optional[set[Cell]] = None,
                             suggestion: Optional[set[int]] = None,
                             start=1,
                             depth=0
                             ) -> tuple[set[Cell], set[int]]:
        """
        This method is only called by hidden_group_elimination
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
            if len(new_group) > group_size:
                continue
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
        for i, block in product(range(9), [self.__field.range_row,
                                           self.__field.range_column,
                                           self.__field.range_minigrid]
                                ):
            digits = []
            updated = []
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
                updated.append(cell)
                cell.candidates.intersection_update(candidates)
            if updated:
                full_cand = set(i for i in range(1, 10))
                self.steps.append(Step(f"Hidden Group",
                                  {"group_size": group_size,
                                   "ids": [cell.index for cell in updated],
                                   "values": full_cand - candidates
                                   }))
                return True
        return False

    def old_brute_force(self, first=True):
        bf = min((cell for cell in self.__field.grid if not cell.value),
                 key=lambda cell: len(cell.candidates))
        total_solutions = 0
        solver = Solver(self.__field)
        for candidate in bf.candidates:
            self.__field[bf.index] = Cell(bf.index, candidate, set())
            solver.field = self.__field
            solution_count = solver.fast_solve(first | (total_solutions != 0))
            if solution_count:
                if first:
                    self.__field = solver.__field
                    self.steps.append(Step("Brute Force", {"size": len(
                        bf.candidates), "id": bf.index, "value": candidate}))
                    self.steps += solver.steps
                    return 1
                else:
                    total_solutions += solution_count
            if total_solutions > 1:
                return total_solutions
        return total_solutions

    def brute_force(self, first=True):
        solution_count = 0
        current_cell_index = 0
        free_cells = [cell for cell in self.__field if not cell.value]
        while True:
            # Find solution
            while 0 <= current_cell_index < len(free_cells):
                if free_cells[current_cell_index].next_candidate():
                    if self.__field.check_cell(free_cells[current_cell_index]):
                        current_cell_index += 1
                else:
                    free_cells[current_cell_index].reset_candidate()
                    current_cell_index -= 1
            # If found
            if current_cell_index == len(free_cells):
                solution_count += 1
                if first:
                    self.steps.append(Step("Brute Force", {}))
                    return True
                elif solution_count == 2:
                    return False
                else:
                    current_cell_index -= 1
            else:
                return solution_count == 1

    def solve(self) -> tuple[int, int]:
        """
        Retruns (single_solution, difficulty)
        """
        difficulty = 0
        self.init_candidates()
        while Field.free_count(self.__field.grid) and self.check_candidates():
            if self.naked_singles():
                continue
            elif self.hidden_singles():
                difficulty = max(1, difficulty)
            elif (self.all_omissions()
                    or self.group_elimination(2)):
                difficulty = max(2, difficulty)
            elif (self.group_elimination(3)
                    or self.hidden_group_elimination(2)):
                difficulty = max(3, difficulty)
            elif (self.group_elimination(4)
                    or self.hidden_group_elimination(3)
                    or self.hidden_group_elimination(4)):
                difficulty = max(4, difficulty)
            else:
                single_solution = self.old_brute_force(True)
                if single_solution:
                    return 1, 5
                else:
                    return 0, -1
        if Field.free_count(self.__field.grid):
            return 0, -1
        else:
            return 1, difficulty

    def hint(self):
        self.init_candidates()
        if (self.naked_singles()
                or self.hidden_singles()
                or self.all_omissions()
                or self.group_elimination(2)
                or self.group_elimination(3)
                or self.hidden_group_elimination(2)
                or self.group_elimination(4)
                or self.hidden_group_elimination(3)
                or self.hidden_group_elimination(4)
            ):
            pass
        else:
            return None
        return self.steps.pop()

    def fast_solve(self, first=True) -> tuple[int, int]:
        """
        Retruns (single_solution, difficulty)
        """
        solution_count = 1
        self.init_candidates()
        while self.naked_singles():
            pass
        while Field.free_count(self.__field.grid) and self.check_candidates():
            if (not self.fast_crme) and self.naked_singles():
                continue
            elif self.hidden_singles():
                continue
            elif len([cell for cell in self.__field if not cell.value and len(cell.candidates) != 2]) == 0:
                return 2
            else:
                solution_count = self.old_brute_force(first)
                return solution_count
        if Field.free_count(self.__field.grid):
            return 0
        else:
            return 1
