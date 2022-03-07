from ast import Pass
import pstats
from re import L
import pygame
from itertools import product
from cell import Cell
from point import Point
from collections.abc import Iterable

class Field:
    def __init__(self, sf_cell : pygame.Surface, sf_sel_cell : pygame.Surface, sf_err_cell : pygame.Surface):
        self.cells = [[None for j in range(9)] for i in range(9)]
        self.selected = None
        for x_pos, y_pos, x_off, y_off in product(range(0,3), repeat =4 ):
            self.cells[x_pos + x_off * 3][y_pos + y_off * 3] = Cell(sf_cell, sf_sel_cell, sf_err_cell,
                (x_pos * 32 + x_off * (32 * 3 + 4), y_pos * 32 + y_off * (32 * 3 + 4)),
                Point(x_pos + x_off * 3, y_pos + y_off * 3))

    def select_colide_cell(self, x : float, y : float):
        if self.selected:
            self.selected.deselect()
            self.selected = None
        for row in self.cells:
            for cell in row: 
                if cell.collidepoint(x, y):
                    self.selected = cell
                    cell.select()
    
    def select_cell(self, x : int, y : int):
        if self.selected:
            self.selected.deselect()
        self.selected = self.cells[x][y]
        self.cells[x][y].select()
    
    def check_iter(cells : Iterable) -> bool:
        correct = True
        digs = {}
        for cell in cells:
            if cell.value: 
                if cell.value in digs:
                    digs[cell.value].mark()
                    cell.mark()
                    correct = False
                else:
                    digs[cell.value] = cell
            else: correct = False
        return correct

    def check_solution(self) -> bool:
        for i,j in product(range(9), repeat=2): self.cells[i][j].unmark()
        correct = True
        for i in range(9):
            correct &= Field.check_iter([self.cells[i][j] for j in range(9)])
            correct &= Field.check_iter([self.cells[j][i] for j in range(9)])
            correct &= Field.check_iter([self.cells[i - (i % 3) + j // 3][(i % 3) * 3 + j % 3]  for j in range(9)])
        return correct

    def set_cell(self, value, sf_dig : pygame.Surface):
        if self.selected:
            self.selected.set(value, sf_dig)
            result = self.check_solution()
        print(result)
    
    def safe_set_cell(self, x : int, y : int, value, sf_dig : pygame.Surface):
        self.cells[x][y].set(value, sf_dig)

    def draw(self, screen : pygame.Surface):
        for row in self.cells:
            for cell in row: 
                cell.draw(screen)