from typing import ClassVar
import pygame
import pygame.freetype

from ui.GUI import GUIobject
from ui.constants import (COLOR_BUTTON_DEFAULT,
                          COLOR_BUTTON_HOVER,
                          COLOR_BUTTON_PRESSED,
                          COLOR_TEXT,
                          UI_BUTTON_ON_CLICK,
                          UI_BUTTON_ON_ENTER,
                          UI_BUTTON_ON_LEAVE,
                          UI_BUTTON_ON_RELEASE)


class Button(GUIobject):
    # __sf_bg: ClassVar[pygame.surface.Surface]
    _f_text: ClassVar[pygame.freetype.Font]
    _sf_icon: pygame.surface.Surface
    _text: str = None
    _text_color = None
    _hover: bool = False
    _pressed: bool = False
    _type: str

    def __init__(self,
                 pos: tuple[float, float],
                 # size: tuple[float, float] = (64, 64),
                 icon: pygame.surface.Surface = None,
                 font: pygame.freetype.Font = None,
                 text: str = None,
                 text_color=COLOR_TEXT,
                 id=None
                 ):
        if text and font:
            self._type = "text"
            self._f_text = font
            self._text_color = text_color
            self._text = text
        elif icon:
            self._type = "icon"
            self._sf_icon = icon
        self._rect = pygame.rect.Rect(pos, (64, 64))
        super().__init__(id)

    def init():
        pass

    def collidepoint(self, x: float, y: float) -> bool:
        return self._rect.collidepoint(x, y)

    def on_enter(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_ENTER, event_data))

        self._hover = True

    def on_leave(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_LEAVE, event_data))

        self._hover = False

    def on_click(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_CLICK, event_data))

        self._pressed = True

    def on_release(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_RELEASE, event_data))

        self._pressed = False

    @property
    def pressed(self): return self._pressed

    @property
    def hover(self): return self._hover

    def draw(self, screen: pygame.Surface):
        if self._pressed:
            pygame.draw.rect(screen, COLOR_BUTTON_PRESSED, self._rect)
        elif self._hover:
            pygame.draw.rect(screen, COLOR_BUTTON_HOVER, self._rect)
        else:
            pygame.draw.rect(screen, COLOR_BUTTON_DEFAULT, self._rect)
        if self._type == "icon":
            screen.blit(self._sf_icon, self._rect)
        elif self._type == "text":
            text, text_rect = self._f_text.render(
                self._text, self._text_color, style=pygame.freetype.STYLE_STRONG)
            text_rect = text.get_rect(center=self._rect.center)
            screen.blit(text, text_rect)
