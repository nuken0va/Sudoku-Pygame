from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar

import pygame
from logic.cell import Cell
from logic.field import Field

from game.cell import GameCell


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

    __sf_field: ClassVar[pygame.Surface]
    __rect: pygame.Rect
    __field: Field[GameCell]
    __solution: Field[Cell]
    autocerrection: bool = False
    undo_list: list[Transaction]
    redo_list: list[Transaction]

    selected: GameCell = None

    def __init__(self, sudoku: list, solution: list):
        self.__rect = GameField.__sf_field.get_rect(topleft=(3,147))
        self.undo_list = []
        self.redo_list = []
        cells = [None for j in range(81)]
        for index, value in enumerate(sudoku):
            x, y = index // 9, index % 9
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
        GameField.__sf_field = pygame.image.load("res\\field.png").convert()
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
    
    def select_cell(self, index: int):
        self.deselect()
        self.selected = self.__field[index]
        self.__field[index].selected = True
        for other in self.__field.range_neighbours(self.selected):
            other.neigbour = True
    
    def check_solution(self) -> bool:
        for cell in self.__field.grid: cell.reset_highlight()
    
        if self.autocerrection:
            correct = self.autocorrect_solution()
        correct = self.check_conflicts()

        return correct

    def autocorrect_solution(self) -> bool:
        correct = True
        for i in range(81):
            if self.__field[i].value is None:
                correct = False
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

    def set_cell(self, value: int, index: int = None, check: bool = True) -> bool:
        correct = False
        if index: 
            cell = self.__field[index]
        else:
            cell = self.selected
        if (not cell 
        or cell.fixed
        or cell.value and cell.value == value
        or value is None and not cell.value and not cell.marks
        ):
            return correct
            
        self.redo_list.clear()

        transaction = Transaction(main_cell=cell,
                                  previous_value=cell.value,
                                  value=value,
                                  secondary_cells = []
                                 )
        if cell.marks:
            transaction.previous_marks = cell.marks.copy()
        
        transaction.previous_marks = cell.set_value(value)

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
        self.undo_list.append(transaction)
        return correct

    def set_mark(self, value: int, index: int = None) -> bool:
        result = False
        if index: 
            cell = self.__field[index]
        else:
            cell = self.selected
        if not cell or cell.value:
            return result
        
        self.redo_list.clear()
        transaction = Transaction(main_cell=cell)

        if value:
            transaction.mark = value
        else: 
            transaction.previous_marks = cell.marks.copy()
        cell.set_mark(value)

        self.undo_list.append(transaction)
        return result

    def undo(self):
        if not self.undo_list:
            return
        transaction = self.undo_list.pop()
        cell = transaction.main_cell

        if transaction.mark:
            cell.set_mark(transaction.mark)
        else:
            cell.value = transaction.previous_value
            for other in transaction.secondary_cells:
                other.marks.append(transaction.value)
        if transaction.previous_marks is not None:
            cell.marks = transaction.previous_marks.copy()
        
        self.redo_list.append(transaction)
        if not transaction.mark: 
            self.check_solution()

    def redo(self):
        if not self.redo_list:
            return
        transaction = self.redo_list.pop()
        cell = transaction.main_cell
        
        if transaction.mark:
            cell.set_mark(transaction.mark)
        else:
            cell.set_value(transaction.value)
            for other in transaction.secondary_cells:
                other.marks.remove(transaction.value)


        self.undo_list.append(transaction)
        self.check_solution()

    def draw(self, screen: pygame.Surface):
        screen.blit(GameField.__sf_field, self.__rect)
        for cell in self.__field:
            cell.draw(screen)
