from typing import ClassVar
import pygame
import pygame.freetype

from ui.button import Button
from ui.constants import COLOR_LOGO


class Logo(Button):
    difficulty: int = 0
    _f_dif_text: pygame.freetype.Font = None

    def __init__(self,
                 pos: tuple[float, float],
                 font: pygame.freetype.Font = None,
                 dif_font: pygame.freetype.Font = None,
                 text: str = "数独",
                 text_color=COLOR_LOGO,
                 id=None,
                 difficulty: int = 0
                 ):
        super().__init__(pos, id=id)
        self._type = "text"
        self._f_text = font
        self._text_color = text_color
        self._text = text
        self._rect = pygame.rect.Rect(pos, (64, 64))
        self.difficulty = difficulty
        self._f_dif_text = dif_font

    def collidepoint(self, x: float, y: float) -> bool:
        return self._rect.collidepoint(x, y)

    def on_enter(self):
        self._hover = True

    def on_leave(self):
        self._hover = False

    def on_click(self):
        self._pressed = True

    def on_release(self):
        self._pressed = False

    def draw(self, screen: pygame.Surface):
        # Logo
        text, text_rect = self._f_text.render("数独", COLOR_LOGO, size=80)
        text_rect.center = self._rect.topleft
        screen.blit(text, text_rect)
        # Difficulty info
        dif_text, dif_text_rect = self._f_dif_text.render(
            f"Difficulty {self.difficulty}", COLOR_LOGO, size=12)
        dif_text_rect.midtop = (text_rect.centerx, text_rect.bottom + 10)
        screen.blit(dif_text, dif_text_rect)
