from dataclasses import dataclass
from typing import Callable, ClassVar, Tuple
from ui.GUI import GUIobject
from ui.button import Button
from ui.constants import *
from logic.cell import Cell
import pygame
import pygame.freetype

class Switch(GUIobject):
    __f_text: ClassVar[pygame.freetype.Font]
    __sf_icon: pygame.surface.Surface
    __sf_alt_icon: pygame.surface.Surface
    __text: str = None
    __alt_text: str = None
    __text_color = None
    __hover: bool = False
    __pressed: bool = False
    __state: bool = False
    __type: str

    def __init__(self, 
                 pos: tuple[float, float], 
                 icon_false_filename: str = "",
                 icon_true_filename: str = "",
                 font_filename: str = "",
                 text_false: str = None,
                 text_true: str = None,
                 text_color = (0,0,0),
                 id = None
                 ):
        if text_false and text_true and font_filename: 
            self.__type = "text"
            self.__f_text = pygame.freetype.Font("res\\fonts\\" + font_filename, 32)
            self.__text_color = text_color
            self.__text = text_false
            self.__alt_text = text_true
        elif icon_false_filename and icon_true_filename:
            self.__type = "icon"
            self.__sf_icon = pygame.image.load("res\\ico\\" + icon_false_filename).convert_alpha() 
            self.__sf_alt_icon = pygame.image.load("res\\ico\\" + icon_true_filename).convert_alpha() 
        self.__rect = pygame.rect.Rect(pos,(64,64))
        super().__init__(id)

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def on_enter(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_ENTER, event_data))

        self.__hover = True

    def on_leave(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_LEAVE, event_data))

        self.__hover = False

    def on_click(self):
        self.swap()
        event_data = {'ui_element': self,
                      'state': self.state}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_CLICK, event_data))

        self.__pressed = True

    def on_release(self): 
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_RELEASE, event_data))

        self.__pressed = False

    def swap(self):
        self.__state = not self.__state
        self.__text, self.__alt_text = self.__alt_text, self.__text
        self.__sf_icon, self.__sf_alt_icon = self.__sf_alt_icon, self.__sf_icon
    
    @property
    def state(self): return self.__state

    @state.setter
    def state(self, value: bool):
        if self.__state != value:
            self.swap()
        
    @property
    def pressed(self): return self.__pressed

    @property
    def hover(self): return self.__hover

    def draw(self, screen: pygame.Surface):
        if self.__pressed:
            pygame.draw.rect(screen, 'azure3', self.__rect)
        elif self.__hover:
            pygame.draw.rect(screen, 'azure', self.__rect)
        else: 
            pygame.draw.rect(screen, (154, 208, 236), self.__rect)
        if self.__type == "icon":
            screen.blit(self.__sf_icon, self.__rect)
        elif self.__type == "text":
            text, text_rect = self.__f_text.render(self.__text, self.__text_color)
            text_rect = text.get_rect(center = self.__rect.center)
            screen.blit(text, text_rect)
            
        

