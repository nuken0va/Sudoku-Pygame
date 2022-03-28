from typing import Callable, ClassVar, Tuple
from ui.GUI import GUIobject
from ui.constants import *
from logic.cell import Cell
import pygame
import pygame.freetype

class Button(GUIobject):
    # __sf_bg: ClassVar[pygame.surface.Surface]
    __f_text: ClassVar[pygame.freetype.Font]
    __sf_icon: pygame.surface.Surface
    __text: str = None
    __text_color = None
    hover: bool = False
    pressed: bool = False
    __type: str

    def __init__(self, 
                 pos: tuple[float, float], 
                 filename: str,
                 text: str = None,
                 text_color = (0,0,0),
                 id = None
                 ):
        if text: 
            self.__type = "text"
            self.__f_text = pygame.freetype.Font("res\\fonts\\" + filename, 32)
            self.__text_color = text_color
            self.__text = text
        else:
            self.__type = "icon"
            self.__sf_icon = pygame.image.load("res\\ico\\" + filename).convert_alpha() 
        self.__rect = pygame.rect.Rect(pos,(64,64))
        super().__init__(id)

    def init():
        pass

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def on_hovered(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_HOVERED, event_data))

        self.hover = True

    def on_click(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_CLICK, event_data))

        self.pressed = True

    def on_release(self): 
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_BUTTON_ON_RELEASE, event_data))

        self.pressed = False
        
    def draw(self, screen: pygame.Surface):
        if self.pressed:
            pygame.draw.rect(screen, 'azure3', self.__rect)
        elif self.hover:
            pygame.draw.rect(screen, 'azure', self.__rect)
        else: 
            pygame.draw.rect(screen, (154, 208, 236), self.__rect)
        if self.__type == "icon":
            screen.blit(self.__sf_icon, self.__rect)
        elif self.__type == "text":
            text, text_rect = self.__f_text.render(self.__text, self.__text_color)
            text_rect = text.get_rect(center = self.__rect.center)
            screen.blit(text, text_rect)
            
        

