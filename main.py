import pygame as pg
import random
from pygame.locals import *
import sys, os

BLANCO = (255,255,255)
AZUL_M=(0,0,128)
FPS=50
ANCHO=800
ALTO=800
RESOLUCION=(800,800)
WIDTH=800
HEIGHT=800


#class Game:
    #def __init__(self):
pg.init()#inicializar pygame
pg.mixer.init()#inicializar musica, sonidos

#fund = pg.image.load('images/fondo.png') #fondo de pantalla estrellas

main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla
pg.display.set_caption("THE COLONIZERS")#Nombre del juego en la pantalla
clock = pg.time.Clock() #reloj para controlar fps



game_over = False

while not game_over:  #pequeña estrucctura que siempre se usa en pygame para cerrar
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
            
    main_screen.fill((0,0,128))   #color pantalla 
    pg.display.flip()