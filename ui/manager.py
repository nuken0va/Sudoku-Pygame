import pygame

from pygame.locals import *
from ui.GUI import GUIobject

class GUImanager():

    ui_elements: list[GUIobject] = None

    def __init__(self, *args):
        self.ui_elements = [*args]
        pass
    
    def __getitem__(self, key): 
        for element in self.ui_elements:
            if element.id == key:
                return element
        return None


    def proccess_event(self, event: pygame.event.Event):
        if event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in self.ui_elements:
                colision = button.collidepoint(*pos)
                if button.hover and not colision:
                    button.on_leave()
                elif not button.hover and colision:
                    button.on_enter()

        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.ui_elements:
                if button.collidepoint(*pos) and not button.pressed:
                    button.on_click()

        elif event.type == MOUSEBUTTONUP:
            for button in self.ui_elements:
                if button.pressed:
                    button.on_release()
    
    def draw(self, screen):
        for button in self.ui_elements:
            button.draw(screen)