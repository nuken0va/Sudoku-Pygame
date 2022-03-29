from typing import ClassVar

import pygame
import pygame.freetype
from logic.cell import Cell


class GameCell(Cell):
    __f_value: ClassVar[pygame.freetype.Font]
    __f_marks: ClassVar[pygame.freetype.Font]

    marks: list[int]
    __rect: pygame.Rect

    selected: bool = False
    neigbour: bool = False
    conflict: bool = False
    incorrect: bool = False
    higlighted: bool = False
    higlighted_neigbour: bool = False

    marks_higlight_value: int = 0

    def __init__(self, pos: tuple[float, float], index: int, value: int = None):
        self.__rect = pygame.Rect(pos, (64, 64))
        self.marks = []
        super().__init__(index, value, None)

    def init():
        GameCell.__f_value = pygame.freetype.Font("res\\fonts\\Monainn.otf", 64)
        GameCell.__f_marks = pygame.freetype.Font("res\\fonts\\Broken.ttf", 20)

    def draw(self, screen: pygame.Surface):
        # Cell Background
        bg_color = None
        if self.selected:
            bg_color = 'lightskyblue'
        elif self.neigbour:
            bg_color = 'lightskyblue1'
        elif self.higlighted:
            bg_color = 'lightgreen'
        elif self.higlighted_neigbour:
            bg_color = 'darkolivegreen1'
        if bg_color:
            pygame.draw.rect(screen, bg_color, self.__rect)

        # Cell Value        
        text_color = 'dodgerblue4'
        if self.conflict:
            text_color = 'orangered'
        elif self.incorrect:
            text_color = 'orange'
        elif self.fixed:
            text_color = 'gray0'
        if self.value:
            text, text_rect = GameCell.__f_value.render(str(self.value), text_color)
            text_rect.center = self.__rect.center
            screen.blit(text, text_rect)
        # Cell Marks
        else:
            for mark in self.marks:
                x, y = (mark - 1) % 3, (mark - 1) // 3
                pos = self.__rect.topleft
                pos = (
                    # 20x20 square, 
                    # +2 offset from each squre
                    # +10 center
                    pos[0] + x * 22 + 10,  
                    pos[1] + y * 22 + 10,
                )
                text, text_rect = GameCell.__f_marks.render(str(mark), 'grey21')
                text_rect.center = pos
                screen.blit(text, text_rect)
                
                if self.marks_higlight_value == mark:
                    text_color = 'lightgreen'
                    pygame.draw.circle(screen, 'lightgreen', pos, 10)
                screen.blit(text, text_rect)


    def set_value(self, value):
        self.marks = []
        self.value = value

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

    def reset_highlight(self):
        self.conflict = False
        self.incorrect = False
