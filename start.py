import pygame
from game.main import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.main_loop()