import os

import pygame
import pygame.freetype
from pygame.locals import *

from ui.constants import *


class ResourceManager():
    def __init__(self):
        self.main_dict = {}

        directory = "res\\fonts\\"
        self.main_dict["fonts"] = {}
        for filename in os.listdir(directory):
            path = directory + filename
            if not os.path.isfile(path):
                continue
            name = os.path.splitext(filename)[0]
            self.main_dict["fonts"][name] = pygame.freetype.Font(path, 32)

        directory = "res\\ico\\"
        self.main_dict["icons"] = {}
        for filename in os.listdir(directory):
            path = directory + filename
            if not os.path.isfile(path):
                continue
            name = os.path.splitext(filename)[0]
            self.main_dict["icons"][name] = pygame.image.load(
                path).convert_alpha()

        directory = "res\\ui\\"
        self.main_dict["ui"] = {}
        for filename in os.listdir(directory):
            path = directory + filename
            if not os.path.isfile(path):
                continue
            name = os.path.splitext(filename)[0]
            self.main_dict["ui"][name] = pygame.image.load(
                path).convert_alpha()

    def __getitem__(self, key: str):
        return self.main_dict[key.lower()]
