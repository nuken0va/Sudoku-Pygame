from typing import Callable, ClassVar
from ui.GUI import GUIobject
from logic.cell import Cell
import pygame

class Timer(GUIobject):
    __f_dig: ClassVar[pygame.font.Font]
    start_time: 0

    def __init__(self, pos: tuple[float, float], id: str = None):
        self.__rect = pygame.rect.Rect(pos,(202,96))
        super().__init__(id)

    def init():
        Timer.__f_dig = pygame.font.Font("res\\fonts\\digital.ttf", 64)

    def collidepoint(self, x: float, y: float) -> bool:
        return self.__rect.collidepoint(x, y)
        
    def on_hovered(self) -> None:
        pass

    def on_click(self) -> None: 
        pass

    def on_release(self) -> None: 
        pass

    def restart_timer(self):
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (239, 218, 215), self.__rect)
        pygame.draw.rect(screen, (239, 218, 215), self.__rect, width=2)
        text_color = 'gray0'
        time = (pygame.time.get_ticks() - self.start_time)//1000
        m, s = time // 60, time % 60
        if m < 100:
            text = Timer.__f_dig.render(f"{m:02d}:{s:02d}", False, text_color)
        else: 
            text = Timer.__f_dig.render(f"X_X", False, text_color)
        text_rect = text.get_rect(center = self.__rect.center)
        screen.blit(text, text_rect)

        

