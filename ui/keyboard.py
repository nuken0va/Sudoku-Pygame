from typing import ClassVar
from ui.button import Button

import pygame
import pygame.locals

class Keyboard(Button):
    def __init__(self, 
                 pos: tuple[float, float],
                 key: int, 
                 filename: str,
                 text: str = None,
                 text_color = (0,0,0),
                 mod = 0,
                 unicod = None,
                 scancode = None, 
                 id = None
                 ):
        self.__key = key
        self.__mod = mod
        self.__unicode = unicod
        self.__scancode = scancode
        super().__init__(pos, filename, text, text_color, id)
    
    def on_click(self):
        event_data = {'key': self.__key,
                      'mod': self.__mod,
                      'unicode': self.__unicode,
                      'scancode': self.__scancode}
        pygame.event.post(pygame.event.Event(pygame.locals.KEYDOWN, event_data))

        self.pressed = True
