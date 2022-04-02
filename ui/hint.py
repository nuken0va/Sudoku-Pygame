from typing import ClassVar, Tuple
import pygame
import pygame.freetype

from ui.UI_base import PopupObject, UiObject
from ui.constants import (COLOR_BUTTON_DEFAULT,
                          COLOR_BUTTON_HOVER,
                          COLOR_BUTTON_PRESSED, COLOR_HINT_BG, COLOR_HINT_FRAME,
                          COLOR_TEXT,
                          UI_BUTTON_ON_CLICK,
                          UI_BUTTON_ON_ENTER,
                          UI_BUTTON_ON_LEAVE,
                          UI_BUTTON_ON_RELEASE)
from ui.manager import UiManager

class Hint(PopupObject):
    def __init__(self,
                 pos: Tuple[float, float],
                 parent: UiObject ,
                 manager: UiManager,
                 text: str = "",
                 text_color = COLOR_TEXT,
                 bg_color = COLOR_HINT_BG,
                 frame_color = COLOR_HINT_FRAME
                 ):
        self._pos = pos
        self._parent = parent
        self._manager = manager
        self._text = text
        self._text_color = text_color
        self._bg_color = bg_color
        self._frame_color = frame_color
        self._f_text = manager.get_hint_font()
        self._manager.popup_elements.append(self)

    def draw(self, screen: pygame.Surface):
        if not self._text:
            return
        text, text_rect = self._f_text.render(
            self._text,
            self._text_color,
            size=19)
        text_rect = text.get_rect(topleft=self._pos)
        if text_rect.right + 5 > self._manager.window_size[0]:
            text_rect.right = self._manager.window_size[0] - 5
        if text_rect.bottom + 5 > self._manager.window_size[1]:
            text_rect.bottom = self._manager.window_size[1] - 5

        window_rect = pygame.Rect(text_rect.left - 5,
                                  text_rect.top - 5,
                                  text_rect.width + 10,
                                  text_rect.height + 10)
        frame_rect = pygame.Rect(text_rect.left - 4,
                                  text_rect.top - 4,
                                  text_rect.width + 8,
                                  text_rect.height + 8)
        pygame.draw.rect(screen, self._bg_color, window_rect)
        pygame.draw.rect(screen, self._frame_color, frame_rect, width=1)
        screen.blit(text, text_rect)

    def delete(self):
        self._manager.popup_elements.remove(self)