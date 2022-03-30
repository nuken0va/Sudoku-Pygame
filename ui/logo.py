from typing import ClassVar
import pygame
import pygame.freetype

from ui.button import Button
from ui.constants import (COLOR_BUTTON_DEFAULT,
                          COLOR_BUTTON_HOVER,
                          COLOR_BUTTON_PRESSED,
                          COLOR_LOGO,
                          UI_BUTTON_ON_CLICK,
                          UI_BUTTON_ON_ENTER,
                          UI_BUTTON_ON_LEAVE,
                          UI_BUTTON_ON_RELEASE)


class Logo(Button):
    def __init__(self,
                 pos: tuple[float, float],
                 font: pygame.freetype.Font = None,
                 text: str="数独",
                 text_color=COLOR_LOGO,
                 id=None
                 ):
        super().__init__(pos, id=id)
        self._type = "text"
        self._f_text = font
        self._text_color = text_color
        self._text = text
        self._rect = pygame.rect.Rect(pos, (64, 64))

    def collidepoint(self, x: float, y: float) -> bool:
        return self._rect.collidepoint(x, y)

    def on_enter(self):
        self._hover = True

    def on_leave(self):
        self._hover = False

    def on_click(self):
        self._pressed = True

    def on_release(self):
        self._pressed = False

    def draw(self, screen: pygame.Surface):
        game_name, game_name_rect = self._f_text.render("数独", COLOR_LOGO,size=80)
        game_name_rect.center = self._rect.topleft
        screen.blit(game_name, game_name_rect)
