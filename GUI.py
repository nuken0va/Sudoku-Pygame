from abc import ABC, abstractmethod

import pygame


class GUI_object(ABC):    

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def collidepoint(self, x: float, y: float) -> bool:
        pass