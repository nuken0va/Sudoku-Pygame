from typing import Callable, ClassVar
from logic.cell import Cell
import pygame

class Timer():
    __f_dig: ClassVar[pygame.font.Font]
    __start_time: int = 0
    __time_passed: int = 0
    __paused: bool = False

    def __init__(self, pos: tuple[float, float]):
        self.__rect = pygame.rect.Rect(pos,(202,96))

    def init():
        Timer.__f_dig = pygame.font.Font("res\\fonts\\digital.ttf", 64)

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)

    def restart(self):
        self.__start_time = pygame.time.get_ticks()
        self.__time_passed = pygame.time.get_ticks()

    @property
    def paused(self): return self.__paused

    def pause(self):
        if self.__paused:
            self.__paused = False
            self.__start_time = pygame.time.get_ticks()
        else:
            self.__paused = True
            self.__time_passed += pygame.time.get_ticks() - self.__start_time
        return self.__paused

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (239, 218, 215), self.__rect)
        pygame.draw.rect(screen, (239, 218, 215), self.__rect, width=2)
        text_color = 'gray0'
        time = (self.__time_passed + pygame.time.get_ticks() - self.__start_time)//1000
        m, s = time // 60, time % 60
        if m < 100:
            text = Timer.__f_dig.render(f"{m:02d}:{s:02d}", False, text_color)
        else: 
            text = Timer.__f_dig.render(f"X_X", False, text_color)
        text_rect = text.get_rect(center = self.__rect.center)
        screen.blit(text, text_rect)

        

