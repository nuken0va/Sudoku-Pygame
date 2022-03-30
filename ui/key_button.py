import pygame
import pygame.locals

from ui.button import Button
from ui.constants import COLOR_TEXT


class KeyButton(Button):
    def __init__(self,
                 pos: tuple[float, float],
                 key: int,
                 icon: pygame.surface.Surface = None,
                 font: pygame.freetype.Font = None,
                 text: str = None,
                 text_color=COLOR_TEXT,
                 id=None,
                 mod=0,
                 unicod=None,
                 scancode=None
                 ):
        self._key = key
        self._mod = mod
        self._unicode = unicod
        self._scancode = scancode
        super().__init__(pos,
                         icon=icon,
                         font=font,
                         text=text,
                         text_color=text_color,
                         id=id
                         )

    def on_click(self):
        event_data = {'key': self._key,
                      'mod': self._mod,
                      'unicode': self._unicode,
                      'scancode': self._scancode}
        pygame.event.post(pygame.event.Event(
            pygame.locals.KEYDOWN, event_data))

        self._pressed = True
