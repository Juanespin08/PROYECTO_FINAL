import pygame as pg

NEGRO = (0,0,0)
BLANCO = (255,255,255)
AZUL_M=(0,0,128)
FPS=50
ANCHO=800
ALTO=800
RESOLUCION=(800,800)






class Nave(pg.sprite.Sprite):#clase nave jugador
    def __init__(self):
        super().__init__() #funcion super class
        self.image = pg.image.load("images/nave1.png").convert() #cargar imagen nave
        self.image.set_colorkey(NEGRO) #funcion para remover el fondo negro de la imagen de la nave
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2 #posicion central salida nave con el rectangulo
        self.rect.y= ALTO -10  #posicion altura salida nave con el rect
        self.speed_x = 0 #velicidad
        self.fps = 0

    
    