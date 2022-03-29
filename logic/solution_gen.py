import random
from typing import ClassVar

from logic.cell import Cell
from logic.field import Field
from logic.solver import Solver


class SudokuGenerator():

    field: Field[Cell]
    solver: Solver
    difficulty_levels: ClassVar[dict] = {
        1: (40, 46),
        2: (46, 50),
        3: (50, 54),
        4: (54, 57),
        5: (57, 58)
    }

    def __init__(self):
        self.field = Field([None for j in range(81)])
        grid_step = [0 for _ in range(81)]
        grid_gen = [[x for x in range(1, 10)] for i in range(81)]        
        self.solver = Solver()

        for cell in range(9):
            random.shuffle(grid_gen[cell])
        cell = 0
        backtrack = False
        while 0 <= cell < 81:
            if not backtrack:
                self.field[cell].value = grid_gen[cell][grid_step[cell]]
                if self.test_correct(cell):
                    cell += 1
                    continue
            if grid_step[cell] < 8:
                grid_step[cell] += 1
                backtrack = False
            else: 
                grid_step[cell]  = 0
                self.field[cell].value = None
                cell -= 1
                backtrack = True

    def test_correct(self, cell_id: int) -> bool:
        for cell in self.field.range_neighbours(self.field[cell_id]):
            if self.field[cell_id].value == cell.value:
                return False
        return True
    
    def clear_cells(self, field, count, check = True):
        while count:
            cell = random.choice(field.grid)
            if cell.value is None:
                continue
            else:
                value = cell.value
                cell.value = None
                if check:
                    self.solver.field = field
                    single_solution, _ = self.solver.fast_solve(False)
                    if single_solution:
                        count -= 1
                    else:
                        cell.value = value
                else:
                    count -= 1

    def gen(self):
        start, stop = SudokuGenerator.difficulty_levels[3]
        count = random.randrange(start, stop)
        while True:
            field_copy = self.field.copy()
            self.clear_cells(field_copy, 20, False)
            self.solver.field = field_copy
            single_solution, _ = self.solver.fast_solve(False)
            if single_solution:
                break
        self.clear_cells(field_copy, count-20)
        return field_copy.get_list(), self.field.get_list()

