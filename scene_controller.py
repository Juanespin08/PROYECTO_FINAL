import pygame as pg
from utils.__init__ import *
from nave import Nave
from meter import Meter
import random, os
from explosion import Explosion

class Pantallas:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.clock = pg.time.Clock()

        self.gameBackground = pg.image.load('images/fondo.png')
        pg.display.set_caption("THE COLONIZERS by Juan_A Espin")

        self.game_over = False
        
        # valores para la nave
        velocidadNave = 6
        vidas = 3
        cooldownDisparo = FPS*0.25#fraccion de un segundo
        self.nave = Nave(self.screen, velocidadNave, cooldownDisparo, vidas)

        # valores para los meteoritos
        self.meteorImagesPath = "images/meteoro/"
        self.meteorImages = os.listdir(self.meteorImagesPath)

        self.meteoros = []
        self.meteorosEnPantalla = 10 #numero de meteoros que pueden existir a la vez

        # valores para las explosiones
        self.explosionImages = self.getListOfAnimationImages('images/explosion.jpg', 3)
        self.explosions = []
        self.explosionAnimationSpeed = 0.125

    def getListOfAnimationImages(self, spriteSheet, numOfImages):
        images = []
        spriteSheet = pg.image.load(spriteSheet).convert()
        spriteWidth = spriteSheet.get_width() // numOfImages
        for i in range(numOfImages):
            image = spriteSheet.subsurface(pg.Rect(i * spriteWidth, 0, spriteWidth, spriteSheet.get_height()))
            image = pg.transform.scale(image, (100, 100))
            mask = pg.mask.from_threshold(image, (255, 255, 255), (0, 0, 0, 0))
            image.set_colorkey((255, 255, 255))
            images.append(image)

        return images

    def createExplosion(self, x, y):
        return Explosion(self.screen, [x, y], self.explosionImages, self.explosionAnimationSpeed)

    def explosionManager(self):
        for explosion in self.explosions:
            explosion.update()
            if explosion.imageIndex >= explosion.nImagesInSpriteSheet-1:
                self.explosions.remove(explosion)

    #crear un meteoro
    def createMeteor(self):
        #coger una imagen random de los meteoritos
        image = pg.image.load(self.meteorImagesPath + random.choice(self.meteorImages))

        # las coordenadas requieren para que el meteorito esté completamente dentro
        # y que tengan un espacio razonable entre ellos, por eso los genero una pantalla encima (-HEIGHT)
        x, y = random.randint(0, WIDTH-image.get_width()), random.randint(-HEIGHT, 0)

        speed = random.uniform(2, 4)

        return Meter(self.screen, image, [x, y], speed)

    def isPlayerColliding(self, obstacle):
        if self.nave.rect.colliderect(obstacle.rect):
            return True
        return False

    def meteorUpdate(self):
        for meteor in self.meteoros:
            meteor.update()

            if self.isPlayerColliding(meteor):
                self.meteoros.remove(meteor)
                self.nave.lives -= 1
                self.explosions.append(self.createExplosion(self.nave.rect.centerx, self.nave.rect.y))
                continue

            #si el meteoro no esta en pantalla, que desaparezca
            if not meteor.onScreen():
                self.meteoros.remove(meteor)
    
    def meteorManager(self):
        self.meteorUpdate()
        
        # si hay menos meteoros de los especificados (self.meteorosEnPantalla)
        if len(self.meteoros) < self.meteorosEnPantalla:
            #generar los meteoritos que hacen falta
            for i in range(self.meteorosEnPantalla - len(self.meteoros)):
                self.meteoros.append(self.createMeteor()) #poner el meteoro en la lista

    def bulletUpdate(self):
        for bullet in self.nave.bullets:
            bullet.update()

            #eliminar de la lista si sale de la pantalla
            if not bullet.onScreen():
                self.nave.bullets.remove(bullet)
                continue

            #comparar a todos los meteoritos para ver si han colisionado
            for meteor in self.meteoros:
                #si han colisionado se elimina el meteoro
                if bullet.rect.colliderect(meteor.rect):
                    self.explosions.append(self.createExplosion(bullet.rect.centerx, bullet.rect.top))
                    
                    self.meteoros.remove(meteor)
                    self.nave.bullets.remove(bullet)

    def events(self):
        # eventos
        for event in pg.event.get():
            #si se cancela la pantalla que se pare el "while" del gameloop
            if event.type == pg.QUIT:
                self.game_over = True

    def gameUpdate(self):
        self.events()
        self.screen.blit(self.gameBackground, (0, 0))

        # Game Elements

        self.bulletUpdate()
        self.nave.update()
        self.meteorManager()
        self.explosionManager()

        ###############

        self.clock.tick(FPS)
        pg.display.flip()

    def inicio(self):
        while not self.game_over:
            self.gameUpdate()
        