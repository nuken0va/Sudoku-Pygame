import random
from itertools import product, chain
from typing import ClassVar
from solver import Solver
from logic.field import Field
from logic.cell import Cell


class SudokuGenerator():

    field: Field[Cell]
    grid_step: list[int]
    grid_gen: list[list[int]]

    difficulty_levels: ClassVar[dict] = {
        1: (40, 46),
        2: (46, 50),
        3: (50, 54),
        4: (54, 57),
        5: (57, 58)
    }

    def __init__(self):
        self.field = Field([None for j in range(81)])
        self.grid_step = [0 for _ in range(81)]
        self.grid_gen = [[x for x in range(1, 10)] for i in range(81)]

    def test_correct(self, cell_id: int) -> bool:
        for cell in self.field.range_neighbours(self.field.grid[cell_id]):
            if self.field.grid[cell_id].value == cell.value:
                return False
        return True
    
    def clear_cells(self, field, count, difficulty, check = True):
        while count:
            cell = random.choice(field.grid)
            if cell.value is None:
                continue
            else:
                value = cell.value
                cell.value = None
                if check:
                    solver = Solver(field)
                    single_solution, res_difficulty = solver.solve(False)
                    if single_solution and res_difficulty <= difficulty:
                        count -= 1
                    else:
                        cell.value = value
                else:
                    count -= 1

    def gen(self, difficulty_input):
        if difficulty_input > 5:
            difficulty_input = 5
        elif difficulty_input < 1:
            difficulty_input = 1

        for cell in range(9):
            random.shuffle(self.grid_gen[cell])
        cell = 0
        backtrack = False
        while 0 <= cell < 81:
            if not backtrack:
                self.field.grid[cell].value = self.grid_gen[cell][self.grid_step[cell]]
                if self.test_correct(cell):
                    cell += 1
                    # print(cell)
                    continue
            if self.grid_step[cell] < 8:
                self.grid_step[cell] += 1
                backtrack = False
            else: 
                self.grid_step[cell]  = 0
                self.field.grid[cell].value = None
                cell -= 1
                # print(cell)
                backtrack = True

        start, stop = SudokuGenerator.difficulty_levels[difficulty_input]
        count = random.randrange(start, stop)
        while True:
            field_copy = Field(self.field)
            while True:
                self.clear_cells(field_copy, 20, False)
                solver = Solver(field_copy)
                single_solution, _ = solver.fast_solve(False)
                if single_solution:
                    break
                field_copy = Field(self.field)
            self.field = field_copy
            self.clear_cells(field_copy, count-20, difficulty_input)

            solver = Solver(field_copy)
            solution_count, difficulty = solver.solve()
            print(field_copy)
            print(solution_count)
            #if difficulty < difficulty_input: continue
            print(solver.steps)
            break
        return field_copy.get_list()

