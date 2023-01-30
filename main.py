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


class Meter(pg.sprite.Sprite): #clase meteorito
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/meteoro/meter.png")
        self.rect = self.image.get_rect()







#class Game:
    #def __init__(self):
pg.init()#inicializar pygame
pg.mixer.init()#inicializar musica, sonidos

fondo= pg.image.load('images/fondo.png') #imagen fondo mde pantalla
nave= pg.image.load('images/nave11.png') #imagen nave

main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla

pg.display.set_caption("THE COLONIZERS by Juan_A Espin")#Nombre del juego en la pantalla

clock = pg.time.Clock() #reloj para controlar fps
###pg.mouse.set_visible(0)  para que la flecha del raton no se vea


game_over = False


#coordenadas cuadrado
coord_x=350
coord_y=700
#velocidad
vel_x=0
vel_y=0






lista_coor= []#lista de coordenadas
for i in range(80):#para hacer estrellas aleatorias
    pos_x = random.randint(0,800)
    pos_y =  random.randint(0,800) 
    lista_coor.append([pos_x,pos_y])



meter_list = pg.sprite.Group()
all_sprite_list = pg.sprite.Group()

for i in range(50):
    meter = Meter() 
    meter.rect.x= random.randrange(800)
    meter.rect.y = random.randrange(600)
     
    meter_list.add(meter)
    all_sprite_list.add(meter)



while not game_over:  #pequeña estrucctura que siempre se usa en pygame para cerrar
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
            sys.exit()

           
    #eventos teclado
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_LEFT:
                vel_x = -3
            if evento.key == pg.K_RIGHT:
                vel_y = 3

        if evento.type == pg.KEYUP:  
            if evento.key == pg.K_LEFT:
                vel_x =0

            if evento.key == pg.K_RIGHT: 
                vel_y = 0   
                


    main_screen.blit(fondo,[0,0])   #posicionamiento imagend e fondo

    for coorde in lista_coor: #bucle para estrellas cayendo
        pos_x = coorde[0]
        pos_y = coorde[1]        
        pg.draw.circle(main_screen, BLANCO,(pos_x,pos_y), 2 ) 
        coorde[1] +=1 
        if coorde[1]>800:
            coorde[1]=0




    
    all_sprite_list.draw(main_screen)
   
    
    #pg.draw.rect(main_screen, VERDE,(x, y, 100, 100))
    #pg.draw.rect(main_screen, VERDE,(x, y, 100, 100))
    #pg.draw.line(main_screen,VERDE, [0,100],[100,100], 5 ) #linea verde para marcador
    main_screen.blit(nave,[coord_x,coord_y])
    pg.display.flip() #actualizar pantalla
    clock.tick(40)
    