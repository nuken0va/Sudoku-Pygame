import sys

import pygame
from pygame.locals import *

import ui.constants
from config import load_config
from game.field import GameField
from logic.solution_gen import SudokuGenerator
from ui.button import Button
from ui.key_button import KeyButton
from ui.manager import GUImanager
from ui.switch import Switch
from ui.timer import Timer

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
field = GameField(*gen.gen())
pause_font = pygame.freetype.Font("res\\fonts\\Saenensis.otf", 32)

gui_manager = GUImanager(Button((641,150), icon_filename="undo.png", id="ui_button_undo"),
                         Button((707,150), icon_filename="redo.png", id="ui_button_redo"),
                        #Switch((641,216), icon_false_filename="bulb2.png",
                        #                  icon_true_filename="bulb.png"),
                         Switch((707,216), icon_false_filename="pen2.png",
                                           icon_true_filename="pen.png",
                                           id="ui_switch_candidate"),

                        #Button((483,41),"auto_candidate.png"),
                         Switch((417,41), icon_false_filename="auto_correction2.png",
                                          icon_true_filename="auto_correction.png",
                                          id="ui_switch_correction"),

                         KeyButton((608, 349), K_1, font_filename="Saenensis.otf", text="1"),
                         KeyButton((674, 349), K_2, font_filename="Saenensis.otf", text="2"),
                         KeyButton((740, 349), K_3, font_filename="Saenensis.otf", text="3"),
                         KeyButton((608, 415), K_4, font_filename="Saenensis.otf", text="4"),
                         KeyButton((674, 415), K_5, font_filename="Saenensis.otf", text="5"),
                         KeyButton((740, 415), K_6, font_filename="Saenensis.otf", text="6"),
                         KeyButton((608, 481), K_7, font_filename="Saenensis.otf", text="7"),
                         KeyButton((674, 481), K_8, font_filename="Saenensis.otf", text="8"),
                         KeyButton((740, 481), K_9, font_filename="Saenensis.otf", text="9")
                        )

timer = Timer((199,25))
pic = pygame.image.load("res\\pic.png").convert_alpha() 
pic_rect = pic.get_rect(bottomright=(880,800))
pause = False
end_game = False
candidate_mode = False

timer.restart()
while True:
    if pause:
        screen.fill((21, 114, 161))
        text, text_rect = pause_font.render("Pause", (255,255,255))
        text_rect = text.get_rect(center = screen.get_rect().center)
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and timer.collidepoint(*pos):
                pause = timer.pause()

    elif end_game:
        screen.fill((21, 114, 161))
        text, text_rect = pause_font.render("Congratulations!", (255,255,255))
        text_rect = text.get_rect(center = screen.get_rect().center)
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    else: 
        for event in pygame.event.get():
            gui_manager.proccess_event(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if field.collidepoint(*pos):
                    field.select_colide_cell(*pos)
                elif timer.collidepoint(*pos):
                    pause = timer.pause()

            elif event.type == KEYDOWN:
                print(event)
                if field.selected and event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]:
                    dig = None
                    if event.key not in [K_BACKSPACE, K_DELETE]:
                        dig = int(pygame.key.name(event.key))
                    if  candidate_mode:
                        field.set_mark(dig)
                    else:
                        end_game = field.set_cell(dig)                        

                elif event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    field.undo()
                elif event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:    
                    field.redo()
                elif event.key == K_a and pygame.key.get_mods() & pygame.KMOD_CTRL: 
                    gui_manager["ui_switch_correction"].swap()
                    field.autocerrection = not field.autocerrection
                    field.check_solution()

                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    gui_manager["ui_switch_candidate"].state = True
                    candidate_mode = True

            elif event.type == KEYUP:
                if event.key == K_LCTRL or event.key == K_RCTRL:
                    gui_manager["ui_switch_candidate"].state = False
                    candidate_mode = False

            elif event.type == ui.constants.UI_BUTTON_ON_CLICK:
                if event.ui_element.id == "ui_button_undo":
                    field.undo()
                elif event.ui_element.id == "ui_button_redo":
                    field.redo()
                else:
                    print("click")

            elif event.type == ui.constants.UI_SWITCH_ON_CLICK:
                if event.ui_element.id == "ui_switch_candidate":
                    candidate_mode = event.state
                if event.ui_element.id == "ui_switch_correction":
                    field.autocerrection = not field.autocerrection
                    field.check_solution()

        

        screen.fill((21, 114, 161))
        field.draw(screen) 
        gui_manager.draw(screen)
        timer.draw(screen)
        #screen.blit(pic, pic_rect)
    pygame.display.flip()
    clock.tick(30)
