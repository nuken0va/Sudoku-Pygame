import sys

import pygame
from pygame.locals import *

from config import load_config
from game.field import GameField
from ui.manager import GUImanager
from ui.timer import Timer
from ui.button import Button
from ui.keyboard import Keyboard
from logic.solution_gen import SudokuGenerator
import ui.constants

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

gui_manager = GUImanager(Button((641,150),"undo.png", id="ui_button_undo"),
                         Button((707,150),"redo.png", id="ui_button_redo"),
                         Button((641,216),"blop.png"),
                         Button((707,216),"pen.png"),
                         Keyboard((608, 349), K_1, "Saenensis.otf", "1"),
                         Keyboard((674, 349), K_2, "Saenensis.otf", "2"),
                         Keyboard((740, 349), K_3, "Saenensis.otf", "3"),
                         Keyboard((608, 415), K_4, "Saenensis.otf", "4"),
                         Keyboard((674, 415), K_4, "Saenensis.otf", "5"),
                         Keyboard((740, 415), K_4, "Saenensis.otf", "6"),
                         Keyboard((608, 481), K_7, "Saenensis.otf", "7"),
                         Keyboard((674, 481), K_7, "Saenensis.otf", "8"),
                         Keyboard((740, 481), K_7, "Saenensis.otf", "9"))

timer = Timer((199,25))
pic = pygame.image.load("res\\pic.png").convert_alpha() 
pic_rect = pic.get_rect(bottomright=(880,800))

timer.restart_timer()
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        gui_manager.proccess_event(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if field.collidepoint(*pos):
                field.select_colide_cell(*pos)
        elif event.type == KEYDOWN:
            print(event)
            if field.selected and event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]:
                dig = None
                if event.key not in [K_BACKSPACE, K_DELETE]:
                    dig = int(pygame.key.name(event.key))
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    field.set_mark(dig)
                else:
                    field.set_cell(dig)
                print(field.undo_list)
            elif event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                field.undo()
            elif event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:    
                field.redo()
        elif event.type == ui.constants.UI_BUTTON_ON_CLICK:
            if event.ui_element.id == "ui_button_undo":
                field.undo()
            elif event.ui_element.id == "ui_button_redo":
                field.redo()
            else:
                print("click")
        
    

    screen.fill((21, 114, 161))
    field.draw(screen) 
    gui_manager.draw(screen)
    timer.draw(screen)
    screen.blit(pic, pic_rect)
    pygame.display.flip()
    clock.tick(30)
