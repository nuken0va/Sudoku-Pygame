import sys

import pygame
from pygame.locals import *

from config import load_config
from field import GameField
from button import Button
from timer import Timer
from solution_gen import SudokuGenerator

example_sudoku = [
    [9, 6, 4, 3, 8, 2, 7, 5, 1],
    [3, 8, 5, 7, 1, 6, 9, 2, 4],
    [2, 1, 7, 4, 9, 5, 8, 3, 6],
    [7, 9, 3, 6, 4, 1, 2, 8, 5],
    [6, 5, 2, 8, 3, 7, 1, 4, 9],
    [1, 4, 8, 5, 2, 9, 3, 6, 7],
    [5, 3, 9, 1, 6, 8, 4, 7, 2],
    [4, 7, 1, 2, 5, 3, 6, 9, 8],
    [8, 2, 6, 9, 7, 4, 5, 1, 3]]

config = load_config()
pygame.init()
screen = pygame.display.set_mode((config["screen"]["width"], config["screen"]["height"]))
pygame.display.set_caption("schizophrenia sudoku")
clock = pygame.time.Clock()

gen = SudokuGenerator()

GameField.init()
Button.init()
Timer.init()
field = GameField(gen.gen(0))
buttons = [Button((641,150),"undo", field.undo),
            Button((707,150),"redo", field.redo)]
timer = Timer((199,25))

timer.restart_timer()
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                button.hover = button.collidepoint(*pos)
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            field.select_colide_cell(*pos)
            for button in buttons:
                if button.collidepoint(*pos):
                    button.pressed = True
                    button.on_click()
        elif event.type == MOUSEBUTTONUP:
            for button in buttons:
                button.pressed = False
        elif event.type == KEYDOWN:
            if field.selected and event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]:
                dig = None
                if event.key != K_BACKSPACE:
                    dig = int(pygame.key.name(event.key))
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    field.set_mark(dig)
                else:
                    field.set_cell(dig)
                print(field.undo_list)
                #undo.append(Move(field.selected.id, dig, field.selected.get_value()))
            elif event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                field.undo()
            elif event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:    
                field.redo()

    screen.fill('aliceblue')
    field.draw(screen) 
    for button in buttons:
        button.draw(screen)
    timer.draw(screen)
    pygame.display.flip()
    clock.tick(30)
