import pygame as pg
import random
from random import randint
from pygame.locals import *
import sys, os

BLANCO = (255,255,255)
VERDE =  (0,179,71)
AZUL_M=(0,0,128)
FPS=60
ANCHO=800
ALTO=800
RESOLUCION=(800,800)
WIDTH=800
HEIGHT=800


#class Game:
    #def __init__(self):
pg.init()#inicializar pygame
pg.mixer.init()#inicializar musica, sonidos

fondo= pg.image.load('images/fondo.png') #imagen fondo mde pantalla

main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla

pg.display.set_caption("THE COLONIZERS by Juan_A Espin")#Nombre del juego en la pantalla

clock = pg.time.Clock() #reloj para controlar fps



game_over = False


lista_coor= []
for i in range(80):#para hacer estrellas aleatorias
    x = random.randint(0,800)
    y =  random.randint(0,800) 
    lista_coor.append([x,y])


while not game_over:  #pequeña estrucctura que siempre se usa en pygame para cerrar
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
            sys.exit()

    main_screen.blit(fondo,[0,0])   #color de fondo de pantalla 

    for coorde in lista_coor: #bucle para estrellas cayendo
        x = coorde[0]
        y = coorde[1]        
        pg.draw.circle(main_screen, BLANCO,(x,y), 2 ) 
        coorde[1] +=1 
        if coorde[1]>800:
            coorde[1]=0


    
    #pg.draw.line(main_screen,VERDE, [0,100],[100,100], 5 ) #linea verde para marcador

    pg.display.flip() #actualizar pantalla
    clock.tick(40)
    