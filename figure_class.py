from utils.__init__ import *
import pygame as pg

# BALA
class Bullet(pg.sprite.Sprite):
    def __init__(self, screen, pos, speed):
        # init values
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.speed = speed

        # cargar la imagen y coger sus medidas
        self.image = pg.image.load("images/laser.png")
        self.rect = self.image.get_rect()

        # para centrar el disparo
        self.pos[0] -= self.image.get_width()/2

    def updateRect(self):
        # actualizar la posicion del rectangulo
        self.rect.center = self.pos[0], self.pos[1]

    def onScreen(self):
        # Si el objeto aún es visible
        return self.rect.bottom > 0
    
    def draw(self):
        # Dibjuar el objeto a la posicion necessaria
        self.screen.blit(self.image, (self.pos[0], self.pos[1]))
    
    def movement(self):
        # Actualizar la posicion de la bala por su velocidad
        self.pos[1] -= self.speed
    
    def update(self):
        self.movement()
        self.updateRect()
        self.draw()

# EXPLOSION
class Explosion(pg.sprite.Sprite):
    def __init__(self, screen, pos, size, images, animationSpeed):
        # init values
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.animationSpeed = animationSpeed
        self.imageIndex = 0
        self.nImagesInSpriteSheet = 3

        # Preparar todas las imagenes necesarias por la explosion y hacerlas a medida
        self.animationImages = images
        for image in self.animationImages:
            self.animationImages[self.animationImages.index(image)] = pg.transform.scale(image, size)

        # Centrar la explosion
        self.pos[0] -= self.animationImages[0].get_width()/2
        
    def animation(self):
        # Incrementar el valor que indica la imagen adequada por la animacion
        self.imageIndex += self.animationSpeed
    
    def draw(self):
        # Dibujar la explosion a la posicion querida
        self.screen.blit(self.animationImages[int(self.imageIndex)], self.pos)
    
    def update(self):
        self.animation()
        self.draw()
    
# METEORO
class Meter(pg.sprite.Sprite): #clase meteorito
    def __init__(self, screen, image, pos, speed):
        # init values
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect() #variable para posicionarnuestro sprite
    
    def onScreen(self):
        # Decir si el meteoro es visible
        return self.rect.top < HEIGHT

    def updateRect(self):
        # Actualizar la posicion del recangulo
        self.rect.topleft = self.pos[0], self.pos[1]

    def movement(self):
        # Actualizar la posicion del meteoro dado su velocidad
        self.pos[1] += self.speed

    def draw(self):
        # Dibujar el meteoro en la pantalla
        self.screen.blit(self.image, self.pos)

    def update(self):
        self.movement()
        self.updateRect()
        self.draw()
    
# NAVE DEL JUGADOR
class Nave(pg.sprite.Sprite):
    def __init__(self, screen, speed, cooldownTime, lives):
        # init values
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.cooldownTime = cooldownTime
        self.cooldownCounter = 0
        self.lives = lives
        self.turnSpeed = 4
        self.angle = 0

        self.image = pg.image.load("images/nave11.png")#cargar imagen nave
        self.blitImage = pg.image.load("images/nave11.png")#cargar la imagen que se pondra en la pantalla
        self.rect = self.image.get_rect()#coger el rectangulo de la imagen

        # Posicion Inicial De La Nave
        self.rect.center = WIDTH//2, HEIGHT*0.8

        # Inicializar la lista de balas
        self.bullets = []
    
    def draw(self):
        # Dibjuar la nave en la pantalla
        self.screen.blit(self.blitImage, (self.rect.topleft))

    def createBullet(self):
        # Cojer las coordenadas por donde comienza la bala
        x, y = self.rect.center
        speed = 10 # velocidad de la bala

        return Bullet(self.screen, [x, y], speed)

    def shoot(self):
        # si ha passado el tiempo "cooldown" para disparar
        if self.cooldownCounter > self.cooldownTime:
            # crea una bala y la pone en la lista
            self.bullets.append(self.createBullet())
            self.cooldownCounter = 0 # Reinicia el "cooldown"

    def borders(self):
        # Si la nave se pone en uno de los dos extremos de la pantalla, se quedara alli
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

    def turnTill180(self):
        # Si no ha llegado a los 180 grados, seguira girando
        if self.angle < 180:
            self.angle += self.turnSpeed

            # Tienes que girar la imagen principal, sino se distorcionara
            self.blitImage = pg.transform.rotate(self.image, self.angle)

            # Para girar de centro, tienes que actualizar el centro de la imagen
            center = (self.rect.centerx, self.rect.centery)
            self.rect = self.blitImage.get_rect(center=center)

    def update(self):
        self.cooldownCounter += 1

        self.controls()
        self.borders()
        self.draw()

# PLANETA 
class Planet(pg.sprite.Sprite):
    def __init__(self, screen, images, inGame=True):
        # init values
        self.screen = screen
        self.images = images
        self.inGame = inGame
        self.imageSize = self.images[0].get_width()
        self.animationIndex = 0

        # Si esta en juego tendra diferentes coordenadas que en el menu
        if inGame:
            x, y = WIDTH//2-self.imageSize//2, -self.imageSize
        else:
            x, y = WIDTH//2-self.imageSize//2, -self.imageSize*0.7

        self.rect = pg.rect.Rect(x, y, self.imageSize, self.imageSize)
    
    def movement(self):
        # Si llega a la posicion deseada
        if self.rect.bottom < self.imageSize/2.5:
            self.rect.y += 1 # Mover abajo
        
    def animation(self):
        self.animationIndex += 0.075 # Incrementar el index para canviar de imagen

        # Si llega al fin de la lista de imagenes, que comienze otra vez
        if int(self.animationIndex) >= len(self.images)-1:
            self.animationIndex = 0

    def draw(self):
        # Dibujar el planeta en la pantalla
        self.screen.blit(self.images[int(self.animationIndex)], self.rect)
        
    def update(self):
        if self.inGame:
            self.movement()
        self.animation()
        self.draw()