from abc import ABC, abstractmethod

import pygame


class GUIobject(ABC):
    __id: str = None

    def __init__(self, id):
        self.__id = id

    @property
    def id(self): return self.__id

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def collidepoint(self, x: float, y: float) -> bool:
        pass

    @abstractmethod
    def on_enter(self) -> None:
        pass

    @abstractmethod
    def on_leave(self) -> None:
        pass

    @abstractmethod
    def on_click(self) -> None:
        pass

    @abstractmethod
    def on_release(self) -> None:
        pass
