from typing import Tuple
import pygame

from pygame.locals import (MOUSEMOTION,
                           MOUSEBUTTONDOWN,
                           MOUSEBUTTONUP)
from res_manager import ResourceManager
from ui.UI_base import UiObject


class UiManager():
    resource_manager: ResourceManager = None
    ui_elements: list[UiObject] = None
    popup_elements: list[UiObject] = None

    def __init__(self, window_size: Tuple[int, int], resource_manager: ResourceManager, *args):
        self.window_size = window_size
        self.resource_manager = resource_manager
        self.ui_elements = [*args]
        for ui_element in self.ui_elements:
            ui_element.manager = self
        self.popup_elements = []

    def __getitem__(self, key):
        for element in self.ui_elements:
            if element.id == key:
                return element
        return None

    def get_hint_font(self):
        return self.resource_manager["fonts"]["winterthur"]

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
        for ui_element in self.ui_elements:
            ui_element.draw(screen)

        for popup_element in self.popup_elements:
            popup_element.draw(screen)
