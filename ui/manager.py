import pygame

from pygame.locals import (MOUSEMOTION,
                           MOUSEBUTTONDOWN,
                           MOUSEBUTTONUP)
from ui.GUI import GUIobject


class UImanager():

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
            for ui_element in self.ui_elements:
                colision = ui_element.collidepoint(*pos)
                if ui_element.hover and not colision:
                    ui_element.on_leave()
                elif not ui_element.hover and colision:
                    ui_element.on_enter()

        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for ui_element in self.ui_elements:
                if ui_element.collidepoint(*pos) and not ui_element.pressed:
                    ui_element.on_click()

        elif event.type == MOUSEBUTTONUP:
            for ui_element in self.ui_elements:
                if ui_element.pressed:
                    ui_element.on_release()

    def draw(self, screen):
        for button in self.ui_elements:
            button.draw(screen)
