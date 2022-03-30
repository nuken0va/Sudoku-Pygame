import pygame
import pygame.freetype
from ui.button import Button
from ui.constants import (UI_SWITCH_ON_CLICK,
                          UI_SWITCH_ON_ENTER,
                          UI_SWITCH_ON_LEAVE,
                          UI_SWITCH_ON_RELEASE)


class Switch(Button):
    _sf_alt_icon: pygame.surface.Surface
    _alt_text: str = None
    _state: bool = False
    _type: str

    def __init__(self,
                 pos: tuple[float, float],
                 icon_false: pygame.surface.Surface = None,
                 icon_true: pygame.surface.Surface = None,
                 font: pygame.freetype.Font = None,
                 text_false: str = None,
                 text_true: str = None,
                 text_color=(0, 0, 0),
                 init_state=False,
                 id=None
                 ):
        if text_false and text_true and font:
            self._alt_text = text_true
            super().__init__(pos=pos,
                             font=font,
                             str=text_false,
                             text_color=text_color,
                             id=id
                             )
        elif icon_false and icon_true:
            self._sf_alt_icon = icon_true
            super().__init__(pos=pos,
                             icon=icon_false,
                             id=id
                             )
        if init_state:
            self.swap()

    def on_enter(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_ENTER, event_data))

        self._hover = True

    def on_leave(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_LEAVE, event_data))

        self._hover = False

    def on_click(self):
        self.swap()
        event_data = {'ui_element': self,
                      'state': self.state}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_CLICK, event_data))

        self._pressed = True

    def on_release(self):
        event_data = {'ui_element': self}
        pygame.event.post(pygame.event.Event(UI_SWITCH_ON_RELEASE, event_data))

        self._pressed = False

    def swap(self):
        self._state = not self._state
        self._text, self._alt_text = self._alt_text, self._text
        self._sf_icon, self._sf_alt_icon = self._sf_alt_icon, self._sf_icon

    @property
    def state(self): return self._state

    @state.setter
    def state(self, value: bool):
        if self._state != value:
            self.swap()
