import pygame as pg
import random
NEGRO = (0,0,0)
BLANCO = (255,255,255)
AZUL_M=(0,0,128)
FPS=50
ANCHO=800
ALTO=800
RESOLUCION=(800,800)









class Meter(pg.sprite.Sprite): #clase meteorito
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/meteoro/meter.png")
        self.rect = self.image.get_rect() #variable para posicionarnuestro sprite



       
 
        
    def update(self):
        self.rect.y += 1  