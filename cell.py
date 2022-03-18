import glob
import random
from typing import ClassVar

import pygame

from point import Point


class Cell:

    __f_value: ClassVar[pygame.font.Font]
    __f_marks: ClassVar[pygame.font.Font]

    __id: int
    __value: int = None
    __marks: list[int]
    __type: int = None
    __rect: pygame.Rect

    __selected: bool = False
    __marked: bool = False

    def __init__(self, pos: tuple[float, float], id: Point):
        #self.__rect = Cell.__sf_cell.get_rect(topleft=pos)
        self.__rect = pygame.Rect(pos, (64,64))
        self.__marks = []
        self.id = id

    def init():
        Cell.__f_value = pygame.font.Font("dig\\Saenensis.otf", 64)
        Cell.__f_marks = pygame.font.Font("dig\\Saenensis.otf", 20)

    def draw(self, screen: pygame.Surface):
        if self.__selected:
            pygame.draw.rect(screen, (255,255,0), self.__rect,width=2)
        if self.__marked:
            pygame.draw.rect(screen, (255,0,0), self.__rect, width=4)
        if self.__value:
            text = Cell.__f_value.render(str(self.__value), False, 'black')
            text_rect = text.get_rect(center = self.__rect.center)
            screen.blit(text, text_rect)
        else:
            for mark in self.__marks:
                x, y = (mark - 1) % 3, (mark - 1) // 3
                pos = self.__rect.topleft
                pos = (
                    pos[0] + x * 20 + x * 2 ,  
                    pos[1] + y * 20 + y * 2,
                )
                text = Cell.__f_marks.render(str(mark), False, 'darkgray')
                text_rect = text.get_rect(topleft = pos)
                screen.blit(text, text_rect)
                

    def set_value(self, value):
        self.__marks.clear()
        self.__value = value
        #if self.__value:
        #    self.__type = random.randrange(len(Cell.__sf_dig[value - 1]))

        
    def set_mark(self, value):
        if self.__value:
            return
        if not value:
            self.__marks.clear()
        elif value in self.__marks:
            self.__marks.remove(value)
        else: 
            self.__marks.append(value)

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
