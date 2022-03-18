from collections.abc import Iterable
from itertools import product

from typing import ClassVar
import pygame

from cell import Cell
from point import Point


class Field:

    __sf_field: ClassVar[pygame.Surface]
    __rect: pygame.Rect

    selected: Cell = None

    def __init__(self):
        self.__rect = Field.__sf_field.get_rect(topleft=(0,0))
        self.cells = [[None for j in range(9)] for i in range(9)]
        for id in range(81):
            x, y = id // 9, id % 9
            self.cells[x][y] = Cell(
                (
                6 + x * 64 + x * 2 + (x // 3),  
                150 + y * 64 + y * 2 + (y // 3)),
                Point(x, y))

    def init():
        Field.__sf_field = pygame.image.load("dig\\sudoku.png").convert()
        Cell.init()

    def deselect(self):
        if self.selected:
            self.selected.deselect()
            self.selected = None

    def select_colide_cell(self, x: float, y: float):
        self.deselect()
        for row in self.cells:
            for cell in row:
                if cell.collidepoint(x, y):
                    self.selected = cell
                    cell.select()
    
    def select_cell(self, x: int, y: int):
        self.deselect()
        self.selected = self.cells[x][y]
        self.cells[x][y].select()
    
    def __check_iter(cells: Iterable) -> bool:
        correct = True
        digs = {}
        for cell in cells:
            value = cell.get_value()
            if value:
                if value in digs:
                    digs[value].mark()
                    cell.mark()
                    correct = False
                else:
                    digs[value] = cell
            else: 
                correct = False
        return correct

    def check_solution(self) -> bool:
        for i,j in product(range(9), repeat=2): self.cells[i][j].unmark()
        correct = True
        for i in range(9):
            correct &= Field.__check_iter([self.cells[i][j] for j in range(9)])
            correct &= Field.__check_iter([self.cells[j][i] for j in range(9)])
            correct &= Field.__check_iter(
                [self.cells[i - (i % 3) + j // 3][(i % 3) * 3 + j % 3] for j in range(9)])
        return correct

    def set_cell(self, value: int, pos: Point = None, check: bool = True) -> bool:
        result = False
        if pos: 
            cell = self.cells[pos.x][pos.y]
        else:
            cell = self.selected
        if cell:
            cell.set_value(value)
            if check: 
                result = self.check_solution()
        return result

    def set_mark(self, value: int, pos: Point = None) -> bool:
        result = False
        if pos: 
            cell = self.cells[pos.x][pos.y]
        else:
            cell = self.selected
        if cell:
            cell.set_mark(value)
        return result

    def draw(self, screen: pygame.Surface):
        screen.blit(Field.__sf_field, self.__rect)
        for row in self.cells:
            for cell in row: 
                cell.draw(screen)
