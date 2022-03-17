import glob
import random
from typing import ClassVar

import pygame

from point import Point


class Cell:
    __sf_cell: ClassVar[pygame.Surface]
    __sf_sel_mask: ClassVar[pygame.Surface]
    __sf_err_mask: ClassVar[pygame.Surface]
    __sf_dig: ClassVar[list[pygame.Surface]]

    __id: int
    __value: int = None
    __type: int = None
    __rect: pygame.Rect

    __selected: bool = False
    __marked: bool = False

    def __init__(self, pos: tuple[float, float], id: Point):
        self.__rect = Cell.__sf_cell.get_rect(topleft=pos)
        self.id = id

    def init():
        Cell.__sf_cell = pygame.image.load("dig\\cell.png").convert_alpha()
        Cell.__sf_sel_mask = pygame.image.load("dig\\selected_mask.png")\
            .convert_alpha()
        Cell.__sf_err_mask = pygame.image.load("dig\\error_mask.png")\
            .convert_alpha()
        Cell.__sf_dig = [
            [pygame.image.load(file).convert_alpha()
                for file in glob.glob(f"dig\\{i}_v*.png")]
            for i in range(1, 10)]

    def draw(self, screen: pygame.Surface):
        screen.blit(Cell.__sf_cell, self.__rect)
        if self.__selected:
            screen.blit(Cell.__sf_sel_mask, self.__rect)
        if self.__marked:
            screen.blit(Cell.__sf_err_mask, self.__rect)
        if self.__value:
            screen.blit(Cell.__sf_dig[self.__value - 1][self.__type],
                        self.__rect)

    def set_value(self, value):
        self.__value = value
        if self.__value:
            self.__type = random.randrange(len(Cell.__sf_dig[value - 1]))

    def get_value(self):
        return self.__value

    def get_id(self) -> int:
        return self.__id

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    def mark(self):
        self.__marked = True

    def unmark(self):
        self.__marked = False
