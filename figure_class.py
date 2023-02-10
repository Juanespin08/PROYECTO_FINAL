from utils.__init__ import *
from bala import Bullet

#clase nave jugador
class Nave(pg.sprite.Sprite):
    def __init__(self, screen, speed, cooldownTime, lives):
        # init values
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.cooldownTime = cooldownTime
        self.cooldownCounter = 0
        self.lives = lives

        self.image = pg.image.load("images/nave11.png")#cargar imagen nave
        self.rect = self.image.get_rect()#coger el rectangulo de la imagen

        # Posicion Inicial De La Nave
        self.rect.center = WIDTH//2, HEIGHT*0.8

        self.bullets = []
    
    def draw(self):
        self.screen.blit(self.image, (self.rect.topleft))

    def createBullet(self):
        x, y = self.rect.center
        speed = 10

        return Bullet(self.screen, [x, y], speed)

    def shoot(self):
        if self.cooldownCounter > self.cooldownTime:
            self.bullets.append(self.createBullet())
            self.cooldownCounter = 0

    def borders(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    #funcion para los controles de la nave (derecha/izquierda/disparar)
    def controls(self):
        keys = pg.key.get_pressed() #coger todas las teclas

        #condiciones para moverse en el plano x
        #Izquierda: a / Left
        #Derecha: d / Right
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += self.speed
        
        #Disparar: Espacio / Up
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            self.shoot()

    def update(self):
        self.cooldownCounter += 1

        self.controls()
        self.borders()
        self.draw()
 


class Meter(pg.sprite.Sprite): #clase meteorito
    def __init__(self, screen, image, pos, speed):
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.speed = speed
        self.image = image

        self.rect = self.image.get_rect() #variable para posicionarnuestro sprite
    
    def onScreen(self):
        return self.rect.top < HEIGHT

    def updateRect(self):
        self.rect.topleft = self.pos[0], self.pos[1]

    def movement(self):
        self.pos[1] += self.speed

    def draw(self):
        self.screen.blit(self.image, self.pos)

    def update(self):   #funcion update para  
        self.movement()
        self.updateRect()
        self.draw()     



#classe disparo
class Bullet(pg.sprite.Sprite):
    def __init__(self, screen, pos, speed):
        # init values
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.speed = speed

        self.image = pg.image.load("images/laser.png")
        self.rect = self.image.get_rect()

        # para centrar el disparo
        self.pos[0] -= self.image.get_width()/2

    def updateRect(self):
        self.rect.center = self.pos[0], self.pos[1]

    def onScreen(self):
        return self.rect.bottom > 0
    
    def draw(self):
        self.screen.blit(self.image, (self.pos[0], self.pos[1]))
    
    def movement(self):
        self.pos[1] -= self.speed
    
    def update(self):
        self.movement()
        self.updateRect()
        self.draw()







