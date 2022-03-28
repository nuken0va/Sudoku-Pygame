import pygame

from pygame.locals import *
from ui.GUI import GUIobject

class GUImanager():

    ui_elements: GUIobject = None

    def __init__(self, *args):
        self.ui_elements = [*args]
        pass

    def proccess_event(self, event: pygame.event.Event):
        if event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in self.ui_elements:
                button.hover = button.collidepoint(*pos)
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.ui_elements:
                    if button.collidepoint(*pos):
                        button.pressed = True
                        button.on_click()
        elif event.type == MOUSEBUTTONUP:
            for button in self.ui_elements:
                button.pressed = False
    
    def draw(self, screen):
        for button in self.ui_elements:
            button.draw(screen)