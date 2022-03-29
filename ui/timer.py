from typing import ClassVar

import pygame

from ui.constants import *
from ui.button import Button


class Timer(Button):
    __start_time: int = 0
    __time_passed: int = 0
    __paused: bool = False
    '''
    __pause_size_coef: float = 1.02
    __pause_size: float = 12.00
    __pause_min_size: float = 12.00
    __pause_max_size: float = 14.00
    '''
    def __init__(self, pos: tuple[float, float], 
                    id: str = None):
        super().__init__(pos=pos, id=id)
        self._rect = pygame.rect.Rect(pos,(202,96))
        self._f_text = pygame.freetype.Font("res\\fonts\\digital.ttf", 64)

    def collidepoint(self, x: float, y: float) -> bool:
        return self._rect.collidepoint(x, y)

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

    def on_enter(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_TIMER_ON_ENTER, event_data))

        self._hover = True

    def on_leave(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_TIMER_ON_LEAVE, event_data))

        self._hover = False

    def on_click(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_TIMER_ON_CLICK, event_data))

        self._pressed = True

    def on_release(self): 
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_TIMER_ON_RELEASE, event_data))

        self._pressed = False
    '''
    def step(self):
        if self._hover and self.__pause_size < self.__pause_max_size:
            self.__pause_size *= self.__pause_size_coef
            if self.__pause_size > self.__pause_max_size:
                self.__pause_size = self.__pause_max_size
        elif (not self.hover) and self.__pause_size > self.__pause_min_size:
            self.__pause_size /= self.__pause_size_coef
            if self.__pause_size < self.__pause_min_size:
                self.__pause_size = self.__pause_min_size
    '''
    def draw(self, screen: pygame.Surface):
        if self.__paused:
            return
        pygame.draw.rect(screen, (154, 208, 236), self._rect)
        pygame.draw.rect(screen, (239, 218, 215), self._rect, width=2)
        time = (self.__time_passed + pygame.time.get_ticks() - self.__start_time) // 1000
        m, s = time // 60, time % 60
        if m < 100:
            text, text_rect = self._f_text.render(f"{m:02d}:{s:02d}", self._text_color)
        else: 
            text = Timer.__f_dig.render(f"X_X", False, self._text_color)
        text_rect = text.get_rect(center = self._rect.center)
        screen.blit(text, text_rect)

        

