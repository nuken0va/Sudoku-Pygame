from typing import ClassVar

import pygame
import pygame.freetype
from logic.cell import Cell
from ui.constants import (COLOR_CELL_HIGHLIGHTED,
                          COLOR_CELL_HIGHLIGHTED_2,
                          COLOR_CELL_NEIGHBOUR,
                          COLOR_CELL_SELECTED,
                          COLOR_DIGIT_CONFLICT,
                          COLOR_DIGIT_DEFAULT,
                          COLOR_DIGIT_FIXED,
                          COLOR_DIGIT_INCORRECT,
                          COLOR_MARK_DEFAULT,
                          COLOR_MARK_HIGHLIGHTED)


class GameCell(Cell):
    # Visual
    __f_value: pygame.freetype.Font
    __f_marks: pygame.freetype.Font
    __rect: pygame.Rect
    # Value
    marks: list[int]
    # States
    selected: bool = False
    neigbour: bool = False
    conflict: bool = False
    incorrect: bool = False
    highlighted: bool = False
    highlighted_neigbour: bool = False

    marks_higlight_value: int = 0

    def __init__(self,
                 pos: tuple[float, float],
                 index: int,
                 value: int = None,
                 value_font: pygame.freetype.Font = None,
                 mark_font: pygame.freetype.Font = None
                 ):
        self.__rect = pygame.Rect(pos, (64, 64))
        self.marks = []

        if value_font:
            self.__f_value = value_font
        else:
            self.__f_value = pygame.freetype.SysFont("arial", 32)

        if mark_font:
            self.__f_marks = mark_font
        else:
            self.__f_marks = pygame.freetype.SysFont("arial", 32)

        super().__init__(index, value, None)

    def draw(self, screen: pygame.Surface):
        # Cell Background
        bg_color = None
        if self.selected:
            bg_color = COLOR_CELL_SELECTED
        elif self.neigbour:
            bg_color = COLOR_CELL_NEIGHBOUR
        elif self.highlighted:
            bg_color = COLOR_CELL_HIGHLIGHTED
        elif self.highlighted_neigbour:
            bg_color = COLOR_CELL_HIGHLIGHTED_2
        if bg_color:
            pygame.draw.rect(screen, bg_color, self.__rect)

        # Cell Value
        text_color = COLOR_DIGIT_DEFAULT
        if self.conflict:
            text_color = COLOR_DIGIT_CONFLICT
        elif self.fixed:
            text_color = COLOR_DIGIT_FIXED
        if self.value:
            text, text_rect = self.__f_value.render(
                str(self.value), text_color, size=64)
            text_rect.center = self.__rect.center
            screen.blit(text, text_rect)

        # Cell Mask
        if self.value and self.incorrect:
            pygame.draw.line(screen,
                             COLOR_DIGIT_INCORRECT,
                             self.__rect.topleft,
                             self.__rect.bottomright,
                             width=3)

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
                text, text_rect = self.__f_marks.render(
                    str(mark), COLOR_MARK_DEFAULT, size=20)
                text_rect.center = pos
                screen.blit(text, text_rect)

                if self.marks_higlight_value == mark:
                    pygame.draw.circle(screen, COLOR_MARK_HIGHLIGHTED, pos, 10)
                screen.blit(text, text_rect)

    def set_value(self, value):
        self.marks = []
        self.value = value

    def flip_mark(self, value):
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

    def mark_collidepoint(self, x: float, y: float) -> int:
        for mark in self.marks:
            m_x, m_y = (mark - 1) % 3, (mark - 1) // 3
            pos = self.__rect.topleft
            pos = (
                pos[0] + m_x * 22,
                pos[1] + m_y * 22,
            )
            if pygame.Rect(pos, (20, 20)).collidepoint(x, y):
                return mark
        return None

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def reset_mistake_highlight(self):
        self.conflict = False
        self.incorrect = False
