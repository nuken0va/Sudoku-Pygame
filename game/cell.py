import glob
import imp
import random
from typing import ClassVar
from logic.cell import Cell
import pygame

class GameCell(Cell):
    __f_value: ClassVar[pygame.font.Font]
    __f_marks: ClassVar[pygame.font.Font]

    marks: list[int]
    __rect: pygame.Rect

    selected: bool = False
    neigbour: bool = False
    marked: bool = False

    def __init__(self, pos: tuple[float, float], index: int, value: int = None):
        self.__rect = pygame.Rect(pos, (64, 64))
        self.marks = []
        super().__init__(index, value, None)

    def init():
        GameCell.__f_value = pygame.font.Font("res\\fonts\\Saenensis.otf", 64)
        GameCell.__f_marks = pygame.font.Font("res\\fonts\\Saenensis.otf", 20)

    def draw(self, screen: pygame.Surface):
        if self.selected:
            pygame.draw.rect(screen, 'lightskyblue', self.__rect)
        elif self.neigbour:
            pygame.draw.rect(screen, 'lightskyblue1', self.__rect)
        
        text_color = 'dodgerblue4'
        if self.marked:
            text_color = 'orangered'
        elif self.fixed:
            text_color = 'gray0'
        
        if self.value:
            text = GameCell.__f_value.render(str(self.value), False, text_color)
            text_rect = text.get_rect(center = self.__rect.center)
            screen.blit(text, text_rect)
        else:
            for mark in self.marks:
                x, y = (mark - 1) % 3, (mark - 1) // 3
                pos = self.__rect.topleft
                pos = (
                    pos[0] + x * 20 + x * 2 ,  
                    pos[1] + y * 20 + y * 2,
                )
                text = GameCell.__f_marks.render(str(mark), False, 'grey21')
                text_rect = text.get_rect(topleft = pos)
                screen.blit(text, text_rect)

    def set_value(self, value):
        marks = self.marks
        self.marks = []
        self.value = value
        #if self.__value:
        #    self.__type = random.randrange(len(Cell.__sf_dig[value - 1]))

    def set_mark(self, value):
        if self.value:
            return
        if not value:
            self.marks.clear()
        elif value in self.marks:
            self.marks.remove(value)
        else: 
            self.marks.append(value)

    def get_value(self):
        return self.value

    def get_id(self) -> int:
        return self.index

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False
