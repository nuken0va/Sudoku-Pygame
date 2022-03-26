from typing import Callable, ClassVar
from GUI import GUI_object
from logic.cell import Cell
import pygame

class Button(GUI_object):
    __sf_bg: ClassVar[pygame.surface.Surface]
    #__sf_bg_pressed: ClassVar[pygame.surface.Surface]
    #__sf_icon: pygame.surface.Surface
    on_click: Callable
    hover: bool = False
    pressed: bool = False

    def __init__(self, pos: tuple[float, float], filename: str, on_click:Callable = None):
        self.__sf_icon = pygame.image.load("dig\\"+filename+".png").convert() 
        self.__rect = self.__sf_icon.get_rect(topleft=pos)
        self.on_click = on_click

    def init():
        pass
        #Button.__sf_bg = pygame.image.load("dig\\button.png").convert()
        #Button.__sf_bg_pressed = pygame.image.load("dig\\button_pressed.png").convert()

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def draw(self, screen: pygame.Surface):
        if self.pressed:
            pygame.draw.rect(screen, 'azure3', self.__rect)
        elif self.hover:
            pygame.draw.rect(screen, 'azure', self.__rect)
        else: 
            pygame.draw.rect(screen, 'azure2', self.__rect)
        screen.blit(self.__sf_icon, self.__rect)
            
        

