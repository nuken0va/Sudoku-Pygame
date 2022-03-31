import sys
from typing import Tuple

import pygame
from pygame.locals import *
from res_manager import ResourceManager

import ui.constants
from config import load_config
from game.field import GameField
from logic.generator import SudokuGenerator
from ui.button import Button
from ui.key_button import KeyButton
from ui.logo import Logo
from ui.manager import UImanager
from ui.switch import Switch
from ui.timer import Timer
from ui.constants import *


class Game():
    # Game states:
    pause: bool = False
    win: bool = False
    candidate_mode: bool = False
    highlight_mode: bool = False
    # Game states:

    gui_manager: UImanager
    timer: Timer

    field: GameField
    generator: SudokuGenerator

    window_size: Tuple[int, int]
    screen: pygame.Surface
    fps_clock: pygame.time.Clock

    def __init__(self):
        config = load_config()
        self.window_size = (config["screen"]["width"],
                            config["screen"]["height"])
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Sudoku")
        self.fps_clock = pygame.time.Clock()

        self.rm = ResourceManager()
        self.generator = SudokuGenerator()
        puzzle, solution, difficulty = self.generator.gen()
        self.field = GameField(puzzle, solution,
                               mask=self.rm["ui"]["field_grid"],
                               cell_mark_font=self.rm["fonts"]["broken"],
                               cell_value_font=self.rm["fonts"]["monainn"])

        self.gui_manager = UImanager(
            Button(pos=(24, 41),
                   icon=self.rm["icons"]["reset"],
                   id="ui_button_reset"),
            Timer(pos=(104, 25),
                  id="ui_timer",
                  mask=self.rm["ui"]["timer_frame"],
                  font=self.rm["fonts"]["digital"]),
            Switch(pos=(322, 41),
                   icon_false=self.rm["icons"]["auto_candidate_false"],
                   icon_true=self.rm["icons"]["auto_candidate_true"],
                   id="ui_switch_auto_candidate",
                   init_state=self.field.auto_update_neigbours),
            Button(pos=(388, 41),
                   icon=self.rm["icons"]["fill"],
                   id="ui_button_fill_candidate"),
            Switch(pos=(454, 41),
                   icon_false=self.rm["icons"]["auto_correction_false"],
                   icon_true=self.rm["icons"]["auto_correction_true"],
                   id="ui_switch_correction",
                   init_state=self.field.auto_cerrection),
            Button(pos=(520, 41),
                   icon=self.rm["icons"]["hint"],
                   id="ui_button_hint"),
            Button(pos=(641, 218),
                   icon=self.rm["icons"]["undo"],
                   id="ui_button_undo"),
            Button(pos=(707, 218),
                   icon=self.rm["icons"]["redo"],
                   id="ui_button_redo"),
            Switch(pos=(641, 284),
                   icon_false=self.rm["icons"]["eye_closed"],
                   icon_true=self.rm["icons"]["eye_opened"],
                   id="ui_button_highlight"),
            Switch(pos=(707, 284),
                   icon_false=self.rm["icons"]["pen2"],
                   icon_true=self.rm["icons"]["pen"],
                   id="ui_switch_candidate"),
            KeyButton(pos=(608, 417),
                      key=K_1,
                      font=self.rm["fonts"]["monainn"],
                      text="1"),
            KeyButton(pos=(674, 417),
                      key=K_2,
                      font=self.rm["fonts"]["monainn"],
                      text="2"),
            KeyButton(pos=(740, 417),
                      key=K_3,
                      font=self.rm["fonts"]["monainn"],
                      text="3"),
            KeyButton(pos=(608, 483),
                      key=K_4,
                      font=self.rm["fonts"]["monainn"],
                      text="4"),
            KeyButton(pos=(674, 483),
                      key=K_5,
                      font=self.rm["fonts"]["monainn"],
                      text="5"),
            KeyButton(pos=(740, 483),
                      key=K_6,
                      font=self.rm["fonts"]["monainn"],
                      text="6"),
            KeyButton(pos=(608, 549),
                      key=K_7,
                      font=self.rm["fonts"]["monainn"],
                      text="7"),
            KeyButton(pos=(674, 549),
                      key=K_8,
                      font=self.rm["fonts"]["monainn"],
                      text="8"),
            KeyButton(pos=(740, 549),
                      key=K_9,
                      font=self.rm["fonts"]["monainn"],
                      text="9"),
            KeyButton(pos=(674, 615),
                      key=K_BACKSPACE,
                      icon=self.rm["icons"]["eraser"]),
            Logo(pos=(self.window_size[0] - 104, 74),
                 font=self.rm["fonts"]["shippori"],
                 dif_font=self.rm["fonts"]["monainn"],
                 difficulty=difficulty,
                 id="ui_logo")
        )
        self.timer = self.gui_manager["ui_timer"]
        pass

    def reset(self):
        self.generator.reset()
        puzzle, solution, difficulty = self.generator.gen()
        self.field = GameField(puzzle, solution,
                               mask=self.rm["ui"]["field_grid"],
                               cell_mark_font=self.rm["fonts"]["broken"],
                               cell_value_font=self.rm["fonts"]["monainn"])
        self.gui_manager["ui_logo"].difficulty = difficulty

        self.timer.restart()
        pass

    def pause_proc(self):
        self.screen.fill(COLOR_BACKGROUND_PAUSE)
        pause_font = self.rm["fonts"]["monainn"]
        text, text_rect = pause_font.render("Pause", COLOR_TEXT, size=100)
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.pause = self.timer.pause()

    def win_proc(self):
        self.screen.fill(COLOR_BACKGROUND_WIN)
        win_font = self.rm["fonts"]["monainn"]
        text, text_rect = win_font.render(
            "Congratulations!", COLOR_TEXT, size=100)
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.reset()
                self.win = False

    def game_proc(self):
        for event in pygame.event.get():
            self.gui_manager.proccess_event(event)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.field.collidepoint(*pos):
                    if not self.highlight_mode:
                        self.field.select_colide_cell(*pos)
                    else:
                        self.field.highlight_colide_cell(*pos)
                        if self.field.highlight_marks != self.candidate_mode:
                            self.candidate_mode = not self.candidate_mode
                            self.gui_manager["ui_switch_candidate"].swap()

            elif event.type == KEYDOWN:
                if event.key in [K_1, K_2, K_3,
                                 K_4, K_5, K_6,
                                 K_7, K_8, K_9,
                                 K_BACKSPACE]:
                    dig = None
                    if event.key not in [K_BACKSPACE, K_DELETE]:
                        dig = int(pygame.key.name(event.key))
                    if self.highlight_mode:
                        self.field.highlight_value = dig
                        self.field.update_highlights()
                    elif self.candidate_mode and self.field.selected and dig:
                        self.field.flip_mark(dig)
                    elif self.field.selected:
                        self.win = self.field.set_cell(dig)
                elif event.key == K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.field.undo()
                elif event.key == K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.field.redo()

            elif event.type == ui.constants.UI_BUTTON_ON_CLICK:
                if event.ui_element.id == "ui_button_undo":
                    self.field.undo()
                elif event.ui_element.id == "ui_button_redo":
                    self.field.redo()
                elif event.ui_element.id == "ui_button_fill_candidate":
                    self.field.auto_crme()
                elif event.ui_element.id == "ui_button_hint":
                    if not self.field.hint():
                        self.timer.display("IDK,SRY")
                    else:
                        self.win = self.field.check()
                elif event.ui_element.id == "ui_button_reset":
                    self.reset()

            elif event.type == ui.constants.UI_SWITCH_ON_CLICK:
                if event.ui_element.id == "ui_switch_candidate":
                    self.candidate_mode = event.state
                    if self.highlight_mode:
                        self.field.highlight_marks = event.state
                        self.field.update_highlights()

                elif event.ui_element.id == "ui_button_highlight":
                    self.highlight_mode = event.state
                    self.field.highlight = event.state
                    if self.highlight_mode:
                        self.field.deselect()
                        self.field.highlight_marks = self.candidate_mode
                    else:
                        self.field.highlight_marks = False
                        self.field.highlight_value = 0
                    self.field.update_highlights()

                elif event.ui_element.id == "ui_switch_correction":
                    self.field.auto_cerrection = event.state
                    self.field.check()

                elif event.ui_element.id == "ui_switch_auto_candidate":
                    self.field.auto_update_neigbours = event.state

            elif event.type == ui.constants.UI_TIMER_ON_CLICK:
                self.pause = event.ui_element.pause()

        self.screen.fill(COLOR_BACKGROUND_DEFAULT)
        self.field.draw(self.screen)
        self.gui_manager.draw(self.screen)

    def main_loop(self):
        self.timer.restart()
        while True:
            if self.pause:
                self.pause_proc()
            elif self.win:
                self.win_proc()
            else:
                self.game_proc()
            pygame.display.flip()
            self.fps_clock.tick(30)
