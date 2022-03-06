from ast import Pass
import pygame
from typing import Union

class Cell:
    rect : pygame.Rect

    sf_cell : pygame.Surface
    sf_sel_mask : pygame.Surface
    sf_err_mask : pygame.Surface

    sf_dig : pygame.Surface
    id : tuple[int, int]

    selected : bool
    marked : bool

    def __init__(self, sf_cell : pygame.Surface, 
                       sf_sel_mask : pygame.Surface, 
                       sf_err_mask : pygame.Surface, 
                       pos : tuple[float, float], id : tuple[int, int]):
        self.sf_cell = sf_cell
        self.sf_sel_mask = sf_sel_mask
        self.sf_err_mask = sf_err_mask

        self.rect = sf_cell.get_rect(topleft = pos) 
        self.value = None
        self.id = id
        self.selected = False
        self.marked = False
    
    def draw(self, screen : pygame.Surface):
        screen.blit(self.sf_cell, self.rect)
        if self.selected: screen.blit(self.sf_sel_mask, self.rect)
        if self.marked: screen.blit(self.sf_err_mask, self.rect)
        if self.value is not None: screen.blit(self.sf_dig, self.rect)

    def set(self, value, sf_dig : pygame.Surface):
        self.value = value
        self.sf_dig = sf_dig

    def collidepoint(self, x : float, y : float) -> bool:
        return self.rect.collidepoint(x,y)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False