import random
from typing import ClassVar

from logic.cell import Cell
from logic.field import Field
from logic.solver import Solver


class SudokuGenerator():
    field: Field[Cell]
    solver: Solver

    def __init__(self):
        self.reset()

    def reset(self):
        # Random initialization
        self.field = Field([None for j in range(81)])
        grid_step = [0 for _ in range(81)]
        grid_gen = [[x for x in range(1, 10)] for i in range(81)]
        self.solver = Solver()
        for cell in range(9):
            random.shuffle(grid_gen[cell])
        cell = 0
        backtrack = False

        # Walking cell by cell and tries values
        while 0 <= cell < 81:
            if not backtrack:
                self.field[cell].value = grid_gen[cell][grid_step[cell]]
                if self.test_correct(cell):
                    cell += 1
                    continue
            # All values tried
            if grid_step[cell] < 8:
                grid_step[cell] += 1
                backtrack = False
            # Backtrack
            else:
                grid_step[cell] = 0
                self.field[cell].value = None
                cell -= 1
                backtrack = True

    def test_correct(self, cell_id: int) -> bool:
        for cell in self.field.range_neighbours(self.field[cell_id]):
            if self.field[cell_id].value == cell.value:
                return False
        return True

    def clear_cells(self, field: Field[Cell], count, check=True, tries_limit = 100):
        tries = 0
        while count and tries < tries_limit:
            cell = random.choice(field.get_filled())
            value = cell.value
            cell.value = None
            if check:
                self.solver.field = field
                solution_count = self.solver.fast_solve(False)
                if solution_count == 1:
                    count -= 1
                else:
                    tries += 1
                    cell.value = value
            else:
                count -= 1
        return tries < tries_limit

    def gen(self):
        count = random.randrange(50, 57)
        while True:
            while True:
                field_copy = self.field.copy()
                self.clear_cells(field_copy, 20, False)
                self.solver.field = field_copy
                solution_count = self.solver.fast_solve(False)
                if solution_count == 1:
                    break
            if self.clear_cells(field_copy, count-20):
                break
        self.solver.field = field_copy
        _, difficulty = self.solver.solve()
        return field_copy.get_list(), self.field.get_list(), difficulty
