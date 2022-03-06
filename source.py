from itertools import product
import pygame
from pygame.locals import *
from field import Field
import sys
import glob
import math
import random
from config import load_config

example_sudoku = [[1, 5, 9, 3, 6, 4, 8, 2, 7], 
[2, 8, 6, 7, 9, 5, 3, 1, 4],
[3, 4, 7, 2, 1, 8, 6, 9, 5],
[6, 2, 1, 4, 5, 7, 9, 8, 3],
[7, 3, 4, 6, 8, 9, 2, 5, 1],
[8, 9, 5, 1, 3, 2, 4, 7, 6],
[9, 7, 3, 5, 2, 6, 1, 4, 8],
[4, 6, 2, 8, 7, 1, 5, 3, 9],
[5, 1, 8, 9, 4, 3, 7, 6, 2]]

config = load_config()

pygame.init()
screen = pygame.display.set_mode((config["screen"]["width"], config["screen"]["height"]))
pygame.display.set_caption("schizophrenia sudoku")
clock = pygame.time.Clock()

digit_surf = []
for i in range(1,10):
    digit_surf.append([])
    for file in glob.glob(f"dig\\{i}_v*.png"):
        digit_surf[i-1].append(pygame.image.load(file).convert_alpha())
cell_surf = pygame.image.load("dig\\cell.png")
sel_cell_surf = pygame.image.load("dig\\selected_mask.png")
err_cell_surf = pygame.image.load("dig\\error_mask.png")

field = Field(cell_surf, sel_cell_surf, err_cell_surf)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            field.select_cell(pos[0], pos[1])
        elif event.type == KEYDOWN:
            if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                dig = int(pygame.key.name(event.key))
                field.set_cell(dig, random.choice(digit_surf[dig-1]))
            if event.key == K_BACKSPACE:
                field.set_cell(None, None)


    field.draw(screen) 
    pygame.display.update()
    clock.tick(30)