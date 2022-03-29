from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar

import pygame
from logic.cell import Cell
from logic.field import Field
from logic.step import Step

from game.cell import GameCell
from logic.solver import Solver
from ui.constants import *


@dataclass
class Transaction():
    mark: int = None 
    main_cell: GameCell = None 
    secondary_cells: list[GameCell] = None  #cells which lost their marks
    value: int = None 
    previous_value: int = None 
    previous_marks: int = None 


class GameField:

    auto_update_neigbours: bool = True
    auto_cerrection: bool = False

    __sf_field: ClassVar[pygame.Surface]
    __rect: pygame.Rect
    __field: Field[GameCell]
    __solution: Field[Cell]

    highlight: bool = False
    highlight_marks: bool = False
    highlight_value: int = 0

    _undo_list: list[Transaction]
    _redo_list: list[Transaction]

    selected: GameCell = None

    def __init__(self, sudoku: list, solution: list):
        self.__rect = GameField.__sf_field.get_rect(topleft=(3,147))
        self._undo_list = []
        self._redo_list = []
        cells = [None for j in range(81)]
        for index, value in enumerate(sudoku):
            x, y = index % 9, index // 9
            cells[index] = GameCell(
                (
                6 + x * 64 + x * 2 + (x // 3),  
                150 + y * 64 + y * 2 + (y // 3)),
                index,
                value=value
                )
        self.__field = Field(cells)
        self.__solution = Field(solution)

    def init():
        GameField.__sf_field = pygame.image.load("res\\field_grid.png").convert_alpha()
        GameCell.init()

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def deselect(self):
        for cell in self.__field.grid:
            cell.selected = False
            cell.neigbour = False

    def select_colide_cell(self, x: float, y: float):
        for cell in self.__field.grid:
            if cell.collidepoint(x, y):
                self.select_cell(cell.index)
                return
        
    def highlight_colide_cell(self, x: float, y: float) -> bool:
        if not self.highlight:
            return
        for cell in self.__field.grid:
            if cell.collidepoint(x, y):
                if cell.value:
                    self.highlight_value = cell.value
                    self.highlight_marks = False
                    break
                self.highlight_value = cell.mark_collidepoint(x,y)
                if self.highlight_value:
                    self.highlight_marks = True
        self.update_highlights()
                      
    def select_cell(self, index: int):
        self.deselect()
        self.selected = self.__field[index]
        self.__field[index].selected = True
        for other in self.__field.range_neighbours(self.selected):
            other.neigbour = True
    
    def check_solution(self) -> bool:
        for cell in self.__field.grid: cell.reset_highlight()
    
        if self.auto_cerrection:
            self.autocorrect_solution()
        correct = self.check_conflicts()
        correct &= not bool(self.__field.get_free())

        return correct

    def autocorrect_solution(self) -> bool:
        correct = True
        for i in range(81):
            if self.__field[i].value is None:
                #correct = False
                continue
            if self.__field[i].value != self.__solution[i].value:
                self.__field[i].incorrect = True
                correct = False
        return correct

    def check_conflicts(self) -> bool:
        correct = True

        def check_iter(cells: Iterable[GameCell]) -> bool:
            correct = True
            digs: dict[int, GameCell] = {}
            for cell in cells:
                value = cell.get_value()
                if value:
                    if value in digs:
                        digs[value].conflict = True
                        cell.conflict = True
                        correct = False
                    else:
                        digs[value] = cell
                else: 
                    correct = False
            return correct

        for i in range(9):
            correct &= check_iter(self.__field.range_column(i))
            correct &= check_iter(self.__field.range_row(i))
            correct &= check_iter(self.__field.range_minigrid(i))
            
        return correct

    def check_marks(self):
        correct = True
        for i in range(81):
            if self.__field[i].value:
                continue
            if self.__solution[i].value not in self.__field[i].marks:
                correct = False
        return correct

    def set_cell(self, value: int, index: int = None, check: bool = True) -> bool:
        correct = False
        if index is not None: 
            cell = self.__field[index]
        else:
            cell = self.selected
        if (not cell 
        or cell.fixed
        or cell.value and cell.value == value
        or value is None and not cell.value and not cell.marks
        ):
            return correct
            
        self._redo_list.clear()

        transaction = Transaction(main_cell=cell,
                                  previous_value=cell.value,
                                  value=value,
                                  secondary_cells = []
                                 )
        if cell.marks:
            transaction.previous_marks = cell.marks.copy()
        
        cell.set_value(value)

        # Update neigbour cells 
        if self.auto_update_neigbours:
            for other in self.__field.range_neighbours(cell):
                if value in other.marks:
                    other.marks.remove(value)
                    transaction.secondary_cells.append(other)

        # Check grid
        if check: 
            correct = self.check_solution()
        # Save transaction
        self._undo_list.append(transaction)
        return correct

    def flip_mark(self, value: int, index: int = None) -> bool:
        result = False
        if index is not None: 
            cell = self.__field[index]
        else:
            cell = self.selected
        if not cell or cell.value:
            return result
        
        self._redo_list.clear()
        transaction = Transaction(main_cell=cell)

        if value:
            transaction.mark = value
        else: 
            transaction.previous_marks = cell.marks.copy()
        cell.flip_mark(value)

        self._undo_list.append(transaction)
        return result

    def _del_mark(self, value: int, index: int = None) -> bool:
        result = False
        if index is not None: 
            cell = self.__field[index]
        else:
            cell = self.selected
        if (not cell 
            or cell.value
            or value not in cell.marks):
            return result
        return self.flip_mark(value=value, index=index)


    def undo(self):
        if not self._undo_list:
            return
        transaction = self._undo_list.pop()
        cell = transaction.main_cell

        if transaction.mark:
            cell.flip_mark(transaction.mark)
        else:
            cell.value = transaction.previous_value
            for other in transaction.secondary_cells:
                other.marks.append(transaction.value)
        if transaction.previous_marks is not None:
            cell.marks = transaction.previous_marks.copy()
        
        self._redo_list.append(transaction)
        if not transaction.mark: 
            self.check_solution()

    def redo(self):
        if not self._redo_list:
            return
        transaction = self._redo_list.pop()
        cell = transaction.main_cell
        
        if transaction.mark:
            cell.flip_mark(transaction.mark)
        else:
            cell.set_value(transaction.value)
            for other in transaction.secondary_cells:
                other.marks.remove(transaction.value)

        self._undo_list.append(transaction)
        self.check_solution()

    def __clear_highlights(self):
        for cell in self.__field:
            cell.marks_higlight_value = 0
            cell.highlighted = False
            cell.highlighted_neigbour = False

    def __cells_highlights(self):
        for cell in self.__field:
            if cell.value == self.highlight_value:
                cell.highlighted = True
                for other in self.__field.range_neighbours(cell):
                    other.highlighted_neigbour = True

    def __marks_highlights(self):
        for cell in self.__field:
            #cell.marks_higlight = True
            cell.marks_higlight_value = self.highlight_value

    def update_highlights(self):
        # Reset all highlights
        self.__clear_highlights()

        # Marks Highlight
        if self.highlight_value and self.highlight_marks:
            self.__marks_highlights()
            
        # Cells Highlight
        elif self.highlight_value and self.highlight:
            self.__cells_highlights()

    def auto_crme(self, reset=False):
        solver = Solver(self.__field)
        solver.init_candidates()
        self._undo_list.clear()
        for index, cell in enumerate(self.__field):
            if cell.value:
                continue
            elif cell.marks and not reset:
                cell.marks = [mark for mark in cell.marks 
                              if mark in solver.field[index].candidates]
            else:
                cell.marks = list(solver.field[index].candidates)

    def hint(self):
        if not self.autocorrect_solution():
            print("There is at least one mistake")
            return True
        if not self.check_marks():
            print("Marks initialized")
            self.auto_crme()
            return True
        solver = Solver(self.__field, save_marks=True)
        step = solver.hint()
        print(step)
        if step is None:
            print("No hints, Sorry")
            return False
        if step.method in ["Naked Single", "Hidden Single"]:
            self.set_cell(value=step.description["value"],
                          index=step.description["id"])
        elif step.method in ["Naked Group"]:
            for id in step.description["ids"]:
                for mark in step.description["values"]:
                    self._del_mark(value=mark, 
                                   index=id)
        else:
            print(f"Can't execute {step.method}")
            return False
        return True




    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLOR_FIELD_BACKGROUND, self.__rect)
        screen.blit(GameField.__sf_field, self.__rect)
        for cell in self.__field:
            cell.draw(screen)
