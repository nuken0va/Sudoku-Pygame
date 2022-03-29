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

config = load_config()
pygame.init()
screen = pygame.display.set_mode((config["screen"]["width"], config["screen"]["height"]))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()

gen = SudokuGenerator()

GameField.init()
Button.init()
Timer.init()
field = GameField(*gen.gen())
#field = GameField([None, None, None, None, 5, None, 7, 8, None, 4, None, None, 7, 8, None, 1, 2, None, None, None, None, None, None, None, 4, None, None, None, None, None, None, None, None, None, None, None, 3, None, 5, None, None, 7, None, None, None, None, None, 7, 2, 1, None, None, None, 5, None, 3, None, None, 4, 2, 9, None, None, None, None, 2, 9, None, 8, None, 3, None, 9, 7, None, None, None, 1, 6, 4, 2], [1, 2, 3, 4, 5, 6, 7, 8, 9, 4, 5, 6, 7, 8, 9, 1, 2, 3, 7, 8, 9, 1, 2, 3, 4, 5, 6, 2, 1, 4, 3, 6, 5, 8, 9, 7, 3, 6, 5, 8, 9, 7, 2, 1, 4, 8, 9, 7, 2, 1, 4, 3, 6, 5, 5, 3, 1, 6, 4, 2, 9, 7, 8, 6, 4, 2, 9, 7, 8, 5, 3, 1, 9, 7, 8, 5, 3, 1, 6, 4, 2])
pause_font = pygame.freetype.Font("res\\fonts\\Saenensis.otf", 32)

gui_manager = GUImanager(Button((641,150), icon_filename="undo.png", id="ui_button_undo"),
                         Button((707,150), icon_filename="redo.png", id="ui_button_redo"),
                         Switch((641,216), icon_false_filename="eye_closed.png",
                                           icon_true_filename="eye_opened2.png",
                                           id="ui_button_highlight"),
                         Switch((707,216), icon_false_filename="pen2.png",
                                           icon_true_filename="pen.png",
                                           id="ui_switch_candidate"),

                         Switch((420,41), icon_false_filename="auto_candidate2.png",
                                          icon_true_filename="auto_candidate.png",
                                          id="ui_button_auto_candidate"),
                         Button((486,41),"fill.png", id="ui_button_fill_candidate"),
                         Switch((552,41), icon_false_filename="auto_correction2.png",
                                          icon_true_filename="auto_correction.png",
                                          id="ui_switch_correction"),
                         Button((618,41),"hint.png", id="ui_button_hint"),

                         Timer((202,25), id="ui_timer"),

                         KeyButton((608, 349), K_1, font_filename="Saenensis.otf", text="1"),
                         KeyButton((674, 349), K_2, font_filename="Saenensis.otf", text="2"),
                         KeyButton((740, 349), K_3, font_filename="Saenensis.otf", text="3"),
                         KeyButton((608, 415), K_4, font_filename="Saenensis.otf", text="4"),
                         KeyButton((674, 415), K_5, font_filename="Saenensis.otf", text="5"),
                         KeyButton((740, 415), K_6, font_filename="Saenensis.otf", text="6"),
                         KeyButton((608, 481), K_7, font_filename="Saenensis.otf", text="7"),
                         KeyButton((674, 481), K_8, font_filename="Saenensis.otf", text="8"),
                         KeyButton((740, 481), K_9, font_filename="Saenensis.otf", text="9"),
                         KeyButton((674, 547), K_BACKSPACE, font_filename="Saenensis.otf", text="_")
                        )

# Game states:
pause = False
end_game = False
candidate_mode = False
highlight_mode = False

gui_manager["ui_timer"].restart()
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
            elif event.type == MOUSEBUTTONDOWN:
                pause = gui_manager["ui_timer"].pause()

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
                if (not highlight_mode) and field.collidepoint(*pos):
                    field.select_colide_cell(*pos)

            elif event.type == KEYDOWN:
                if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE]:
                    dig = None
                    if event.key not in [K_BACKSPACE, K_DELETE]:
                        dig = int(pygame.key.name(event.key))
                    if highlight_mode:
                        field.highlight_value = dig
                        field.update_highlights()
                    elif candidate_mode and field.selected:
                        field.set_mark(dig)
                    elif field.selected:
                        end_game = field.set_cell(dig)                        

                elif event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    field.undo()
                elif event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:    
                    field.redo()
                elif event.key == K_a and pygame.key.get_mods() & pygame.KMOD_CTRL: 
                    gui_manager["ui_switch_correction"].swap()
                    field.auto_cerrection = not field.auto_cerrection
                    field.check_solution()

            elif event.type == ui.constants.UI_BUTTON_ON_CLICK:
                if event.ui_element.id == "ui_button_undo":
                    field.undo()
                elif event.ui_element.id == "ui_button_redo":
                    field.redo()
                elif event.ui_element.id == "ui_button_fill_candidate":
                    field.auto_crme()
                else:
                    print("click")

            elif event.type == ui.constants.UI_SWITCH_ON_CLICK:
                if event.ui_element.id == "ui_switch_candidate":
                    candidate_mode = event.state
                    if highlight_mode:
                        field.highlight_marks = event.state
                        field.update_highlights()

                elif event.ui_element.id == "ui_button_highlight":
                    highlight_mode = event.state
                    field.highlight = event.state
                    if highlight_mode:
                        field.deselect()
                        field.highlight_marks = candidate_mode
                    else:
                        field.highlight_marks = False
                        field.highlight_value = 0
                    field.update_highlights()

                elif event.ui_element.id == "ui_switch_correction":
                    field.auto_cerrection = not field.auto_cerrection
                    field.check_solution()
                    
                elif event.ui_element.id == "ui_switch_auto_candidate":
                    field.auto_update_neigbours = event.state
                

            elif event.type == ui.constants.UI_TIMER_ON_CLICK:
                pause = event.ui_element.pause()

        

        screen.fill((21, 114, 161))
        field.draw(screen) 
        gui_manager.draw(screen)
    pygame.display.flip()
    clock.tick(30)
