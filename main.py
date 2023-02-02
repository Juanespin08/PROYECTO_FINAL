import pygame as pg
import random
from random import randint
from pygame.locals import *
import sys, os


NEGRO= (0,0,0)
BLANCO = (255,255,255)
VERDE =  (0,179,71)
AZUL_M=(0,0,128)
FPS=60
ANCHO=800
ALTO=800
RESOLUCION=(800,800)
WIDTH=800 #ancho
HEIGHT=800
SCORE = 0



class Nave(pg.sprite.Sprite):#clase nave jugador
    def __init__(self ):
        super().__init__() #funcion super class
        self.image = pg.image.load("images/nave11.png")#cargar imagen nave       
        self.rect = self.image.get_rect()#para poder posicionar el ractangulo
        self.image.set_colorkey(NEGRO)
        self.rect.centerx = ANCHO // 2 #posicion central salida nave con el rectangulo
        self.rect.y= 650 #posicion altura salida nave con el rect
        self.vel_x = 0 #velOcidad
        self.fps = 0



    def cambio_vel(self,x):
        self.vel_x += x



        

    def update(self):#eventos mouse
        self.rect.x += self.vel_x
        nave.rect.y = 650
        #mouse_pos = pg.mouse.get_pos()
        #nave.rect.centerx = mouse_pos[0]
        #nave.rect.y = 650
        pass

class Meter(pg.sprite.Sprite): #clase meteorito
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/meteoro/meter.png")
        self.rect = self.image.get_rect() #variable para posicionarnuestro sprite
        
    def update(self):   #funcion update para  
        self.rect.y += 1
        if self.rect.y > 800:
            self.rect.y = -10
            self.rect.x = random.randrange(800)#metodo para que al volver a salir los meters sigan siendo ramdom


class Laser(pg.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/laser.png")
        self.rect = self.image.get_rect() #variable para posicionarnuestro sprite    

    def update(self):
        self.rect.y -=10
       


#class Game:
    #def __init__(self):
pg.init()#inicializar pygame
pg.mixer.init()#inicializar musica, sonidos

fondo= pg.image.load('images/fondo.png') #imagen fondo mde pantalla
#nave= pg.image.load('images/nave11.png') #imagen nave
main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla
pg.display.set_caption("THE COLONIZERS by Juan_A Espin")#Nombre del juego en la pantalla

clock = pg.time.Clock() #reloj para controlar fps


game_over = False


#coordenadas posicion nave en pantalla
centerx=350
y=700
#velocidad
vel_x=0
vel_y=0






lista_coor= []#lista de coordenadas
for i in range(80):#para hacer estrellas aleatorias
    pos_x = random.randint(0,800)
    pos_y =  random.randint(0,800) 
    lista_coor.append([pos_x,pos_y])



meter_list = pg.sprite.Group()#lista para almacenar todas las instancias de meteoro y poder detectar las colisiones
all_sprite_list = pg.sprite.Group()#lista para  almacenar todos los sprites
lista_laser = pg.sprite.Group()



for i in range(60): #crear meteoros 
    meter = Meter() #llamar clase
    meter.rect.x= random.randrange(800)#para que aparezcan los meteoros aleatoriamente
    meter.rect.y = random.randrange(600)

    meter_list.add(meter)#agregar elementos a la lista
    all_sprite_list.add(meter)

laser=Laser()
meter = Meter()
nave = Nave()
all_sprite_list.add(nave)




while not game_over:  #pequeña estrucctura que siempre se usa en pygame para cerrar
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
            sys.exit()
            

            #eventos teclado
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_LEFT:
                nave.cambio_vel(-8)
            if evento.key == pg.K_RIGHT:
                nave.cambio_vel(8) 


            if evento.key == pg.K_SPACE:
                laser = Laser()
                laser.rect.x = nave.rect.x +45 
                laser.rect.y = nave.rect.y -20 

                all_sprite_list.add(laser)
                lista_laser.add(laser)    

        if evento.type == pg.KEYUP:  
            if evento.key == pg.K_LEFT:
                nave.cambio_vel(8) 
            if evento.key == pg.K_RIGHT: 
                nave.cambio_vel(-8) 


    for laser in lista_laser:
        meter_list_collide = pg.sprite.spritecollide(laser, meter_list, True)
        for meter in meter_list_collide:
            all_sprite_list.remove(laser)
            lista_laser.remove(laser)
            SCORE +=1
    if laser.rect.y <- 10:
        all_sprite_list.remove(laser)
        lista_laser.remove(laser)      

                

    all_sprite_list.update() #update, para que funcionen todos los sprites
    main_screen.blit(fondo,[0,0])   #posicionamiento imagend e fondo

    for coorde in lista_coor: #bucle para estrellas cayendo
        pos_x = coorde[0]
        pos_y = coorde[1]        
        pg.draw.circle(main_screen, BLANCO,(pos_x,pos_y), 2 ) 
        coorde[1] +=1 
        if coorde[1]>800:
            coorde[1]=0




    
     #funcion para contar los choques de los meteoros con la nave
    meter_list_collide = pg.sprite.spritecollide(nave,meter_list, True)   #lista para colisiones nave meteoros
    for meter in meter_list_collide:
        SCORE +=1
        
    all_sprite_list.draw(main_screen)#dibujar lista de todos los sprites en la pantalla
   
    centerx += vel_x #mover nave
    
   
    #pg.draw.line(main_screen,VERDE, [0,100],[100,100], 5 ) #linea verde para marcador
    #main_screen.blit(nave,[centerx,y])#colocar nave en la pantalla
    pg.display.flip() #actualizar pantalla
    clock.tick(40)
    