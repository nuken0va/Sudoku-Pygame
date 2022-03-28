import pygame
import pygame.locals

from ui.button import Button


class KeyButton(Button):
    def __init__(self, 
                 pos: tuple[float, float],
                 key: int, 
                 icon_filename: str = "",
                 font_filename: str = "",
                 text: str = None,
                 text_color = (0,0,0),
                 id = None,
                 mod = 0,
                 unicod = None,
                 scancode = None
                 ):
        self.__key = key
        self.__mod = mod
        self.__unicode = unicod
        self.__scancode = scancode
        super().__init__(pos, 
                         icon_filename=icon_filename,
                         font_filename=font_filename,
                         text=text, 
                         text_color=text_color, 
                         id=id
                         )
    
    def on_click(self):
        event_data = {'key': self.__key,
                      'mod': self.__mod,
                      'unicode': self.__unicode,
                      'scancode': self.__scancode}
        pygame.event.post(pygame.event.Event(pygame.locals.KEYDOWN, event_data))

        self.__pressed = True
