import pygame as pg
from utils.__init__ import *
from pantallas_class import *

class SceneController:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()

        self.font = pg.font.Font("fonts/futuristicFont.otf", 25)

        self.menuInicial = MenuInicial(self.screen, self.clock, self.font)
        self.game = Game(self.screen, self.clock, self.font)

        pg.display.set_caption("THE COLONIZERS by Juan_A Espin")

    def start(self):
        while True:
            self.menuInicial.inicio()
            self.game.inicio()