import pygame
import pygame.freetype

from ui.button import Button
from ui.constants import (COLOR_DISPLAY,
                          COLOR_TIMER_DEFAULT,
                          UI_TIMER_ON_CLICK,
                          UI_TIMER_ON_ENTER,
                          UI_TIMER_ON_LEAVE,
                          UI_TIMER_ON_RELEASE)


class Timer(Button):
    __start_time: int = 0
    __time_passed: int = 0
    __paused: bool = False
    __display_text: str = ""
    __display_end_time: int

    def __init__(self, pos: tuple[float, float],
                 id: str = None,
                 mask: pygame.surface.Surface = None,
                 font: pygame.freetype.Font = None,
                 size: tuple[float, float] = (202, 96)
                 ):
        super().__init__(pos=pos, id=id)
        self._rect = pygame.rect.Rect(pos, size)
        self._f_text = font
        self._sf_mask = mask
        self._text_color = COLOR_DISPLAY

    def collidepoint(self, x: float, y: float) -> bool:
        return self._rect.collidepoint(x, y)

    def restart(self):
        self.__start_time = pygame.time.get_ticks()
        self.__time_passed = 0

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

    def display(self, text: str, time=1000):
        self.__display_text = text
        self.__display_end_time = pygame.time.get_ticks() + time

    def draw(self, screen: pygame.Surface):
        time = pygame.time.get_ticks()
        pygame.draw.rect(screen, COLOR_TIMER_DEFAULT, self._rect)
        if self.__paused:
            return
        if self.__display_text:
            text, text_rect = self._f_text.render(
                self.__display_text, self._text_color)
            if time > self.__display_end_time:
                self.__display_text = ""
        else:
            time = (self.__time_passed + time - self.__start_time) // 1000
            m, s = time // 60, time % 60
            if m < 100:
                text, text_rect = self._f_text.render(
                    f"{m:02d}:{s:02d}", self._text_color, size=64)
            else:
                text, text_rect = self._f_text.render(f"X_X", self._text_color, size=64)
        text_rect = text.get_rect(center=self._rect.center)
        screen.blit(text, text_rect)
        screen.blit(self._sf_mask, self._rect)
