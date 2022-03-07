from itertools import product
import pygame
from pygame.locals import *
from field import Field
from point import Move, Point
import sys
import glob
import math
import random
from config import load_config

example_sudoku = [[9, 6, 4, 3, 8, 2, 7, 5, 1], [3, 8, 5, 7, 1, 6, 9, 2, 4], [2, 1, 7, 4, 9, 5, 8, 3, 6], [7, 9, 3, 6, 4, 1, 2, 8, 5], [6, 5, 2, 8, 3, 7, 1, 4, 9], [1, 4, 8, 5, 2, 9, 3, 6, 7], [5, 3, 9, 1, 6, 8, 4, 7, 2], [4, 7, 1, 2, 5, 3, 6, 9, 8], [8, 2, 6, 9, 7, 4, 5, 1, 3]]   

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

for i, j in product(range(9), repeat = 2):
    dig = example_sudoku[i][j]
    field.safe_set_cell(i, j, dig, random.choice(digit_surf[dig-1]))

redo = []
undo = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            field.select_colide_cell(pos[0], pos[1])
        elif event.type == KEYDOWN:
            if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]:
                redo = []

                dig, dig_surf = None, None
                if event.key != K_BACKSPACE:
                    dig = int(pygame.key.name(event.key))
                    dig_surf = random.choice(digit_surf[dig-1])

                undo.append(Move(field.selected.id, dig, field.selected.value))

                field.set_cell(dig, dig_surf)
            elif undo and event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                move = undo.pop()
                redo.append(move)
                
                dig = move.prev_value
                if dig: dig_surf = random.choice(digit_surf[dig-1])  
                else: dig_surf = None 

                field.select_cell(move.pos.x, move.pos.y)   
                field.set_cell(dig, dig_surf)
            elif redo and event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:    
                move = redo.pop()
                undo.append(move)

                dig = move.value
                if dig: dig_surf = random.choice(digit_surf[dig-1])  
                else: dig_surf = None

                field.select_cell(move.pos.x, move.pos.y)   
                field.set_cell(dig, dig_surf) 
    field.draw(screen) 
    pygame.display.update()
    clock.tick(30)