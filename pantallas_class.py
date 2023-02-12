import pygame as pg
import os, random
from utils.__init__ import *
from figure_class import *
import sys 



class MenuInicial:
    # Constructor de la clase
    def __init__(self, screen, clock, font) -> None:
        # Inicializa la pantalla
        self.screen = screen
        # Inicializa el reloj
        self.clock = clock
        # Inicializa la fuente
        self.font = font

        # Carga la imagen de fondo para el menú principal
        self.fondoMenuPrincipal = pg.image.load("images/menuBackground.png")

        # Carga la imagen del menú principal y la escala a las dimensiones de la pantalla
        self.menuPrincipal = pg.image.load("images/menuPrincipal.png")
        self.menuPrincipal = pg.transform.scale(self.menuPrincipal, (WIDTH, HEIGHT))

        # Obtiene una lista de imágenes animadas del sprite sheet y las escala a un tamaño adecuado
        self.planetImages = self.getListOfAnimationImages("images/earthSpriteSheet.png", 50)
        for i in range(len(self.planetImages)):
            image = self.planetImages[i]
            image = pg.transform.scale(image, (HEIGHT//1.5, HEIGHT//1.5))
            image.set_colorkey((0, 0, 0))
            self.planetImages[i] = image

        # Crea una instancia de la clase Planet con las imágenes animadas y un indicador de que no se está en juego
        self.planeta = Planet(self.screen, self.planetImages, inGame=False)

        # Indicador de si se debe continuar al juego
        self.continueToGame = False

    # Función que obtiene una lista de imágenes de un sprite sheet
    def getListOfAnimationImages(self, spriteSheet, numOfImages):
        images = []
        # Carga la hoja de sprites
        spriteSheet = pg.image.load(spriteSheet).convert()
        # Calcula el ancho de cada imagen
        spriteWidth = spriteSheet.get_width() // numOfImages
        # Recorre cada imagen y la agrega a la lista
        for i in range(numOfImages):
            image = spriteSheet.subsurface(pg.Rect(i * spriteWidth, 0, spriteWidth, spriteSheet.get_height()))
            images.append(image)

        # Devuelve la lista de imágenes
        return images

    # Función que maneja los eventos
    def events(self):
        # Obtiene los eventos
        for event in pg.event.get():
            # Si se recibe un evento de cierre de la pantalla, se cierra pygame
            if event.type == pg.QUIT:
                sys.exit()

    # Función que verifica si se debe continuar al juego
    def checkForContinue(self):
        # Obtiene los botones presionados
        keys = pg.key.get_pressed()
        # Si aprietas espacio continua hacia al juego
        if keys[pg.K_SPACE]:
            self.continueToGame = True

    def update(self):
        self.events()

        self.checkForContinue()
        self.screen.blit(self.fondoMenuPrincipal, (0, 0))
        self.planeta.update()
        
        self.screen.blit(self.menuPrincipal, (0, 0))

        self.clock.tick(FPS)
        pg.display.flip()

    def inicio(self):
        self.__init__(self.screen, self.clock, self.font)
        while not self.continueToGame:
            self.update()

class Game:
    def __init__(self, screen, clock, font) -> None:
        self.screen = screen
        self.clock = clock
        self.font = font

        # Escoger un fondo aleatorio
        self.gameBackground = self.newBackground()

        self.game_over = False
        
        # valores para la nave
        self.velocidadNave = 6
        self.vidas = 3
        self.cooldownDisparo = FPS*0.25#fraccion de un segundo
        self.nave = Nave(self.screen, self.velocidadNave, self.cooldownDisparo, self.vidas)
        self.score = 0
        self.level = 1
        self.scoreLevelStep = 0
        self.scoreTillNextLevel = 20
        self.planetCreated = False

        # valores para los meteoritos
        self.meteorImagesPath = "images/meteoro/"
        self.meteorImages = os.listdir(self.meteorImagesPath)
        self.meteorSpeed = 2

        self.meteoros = []
        self.meteorosEnPantalla = 10 #numero de meteoros que pueden existir a la vez

        self.explosionImages = self.getListOfAnimationImages('images/explosion.jpg', 3)
        for image in self.explosionImages:
            image.set_colorkey((255, 255, 255))

        self.explosions = []
        self.explosionAnimationSpeed = 0.125

        # valores para los planetas
        self.planetImages = self.getListOfAnimationImages("images/earthSpriteSheet.png", 50)
        for i in range(len(self.planetImages)):
            image = self.planetImages[i]
            image = pg.transform.scale(image, (HEIGHT//1.5, HEIGHT//1.5))
            image.set_colorkey((0, 0, 0))
            self.planetImages[i] = image
        self.planets = []

    def newBackground(self):
        return pg.image.load(f'images/fondos/{random.choice(os.listdir("images/fondos"))}')

    def newLevel(self):
        # Incrementar la dificultad para el nuevo nivel
        self.meteorosEnPantalla += 2
        self.meteorSpeed += 1
        self.score += 20

        # Reiniciar el contador para el nuevo nivel
        self.scoreLevelStep = 0
        self.planetCreated = False

        # Reinicia a valores iniciales la nave y los planetas
        self.planets.clear()
        self.nave.__init__(self.screen, self.velocidadNave, self.cooldownDisparo, self.nave.lives)
        self.gameBackground = self.newBackground()

    def getListOfAnimationImages(self, spriteSheet, numOfImages):
        # Crea una lista vacía para almacenar las imágenes extraídas
        images = []
        
        # Carga la imagen del sprite sheet y la convierte en un formato adecuado para ser usado en Pygame
        spriteSheet = pg.image.load(spriteSheet).convert()
        
        # Calcula el ancho de cada imagen individual en el sprite sheet
        spriteWidth = spriteSheet.get_width() // numOfImages
        
        # Itera a través de cada imagen individual en el sprite sheet
        for i in range(numOfImages):
            # Extrae la imagen individual del sprite sheet
            image = spriteSheet.subsurface(pg.Rect(i * spriteWidth, 0, spriteWidth, spriteSheet.get_height()))
            
            # Agrega la imagen extraída a la lista de imágenes
            images.append(image)

        # Devuelve la lista de imágenes extraídas
        return images

        
    def createExplosion(self, pos, size, meteor=True):
        return Explosion(self.screen, pos, size, self.explosionImages, self.explosionAnimationSpeed)

    def explosionManager(self):
        # Actualizar la lista de explosiones
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

        speed = self.meteorSpeed + random.uniform(0, 3)

        return Meter(self.screen, image, [x, y], speed)

    def isPlayerColliding(self, obstacle):
        if self.nave.rect.colliderect(obstacle.rect):
            return True
        return False

    def meteorUpdate(self):
        # Actualizar todos los meteoros
        for meteor in self.meteoros:
            meteor.update()

            # Comprobar si los meteoros estan colisionando con la nave
            if self.isPlayerColliding(meteor):
                self.meteoros.remove(meteor)
                self.nave.lives -= 1
                self.explosions.append(self.createExplosion([self.nave.rect.centerx, self.nave.rect.y], [200, 200], meteor=False))
                continue

            #si el meteoro no esta en pantalla, que desaparezca
            if not meteor.onScreen():
                self.meteoros.remove(meteor)
    
    def meteorManager(self):
        self.meteorUpdate()
        
        # si hay menos meteoros de los especificados (self.meteorosEnPantalla)
        if len(self.meteoros) < self.meteorosEnPantalla and not self.isNextLevel():
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
                    self.explosions.append(self.createExplosion([bullet.rect.centerx, bullet.rect.top], [100, 100]))
                    
                    self.meteoros.remove(meteor)
                    self.nave.bullets.remove(bullet)
    
    def createPlanet(self):
        return Planet(self.screen, self.planetImages)

    def planetManager(self):
        for planet in self.planets:
            planet.update()

    def isNextLevel(self):
        return self.scoreLevelStep/FPS >= self.scoreTillNextLevel

    def levelManager(self):
        # Verifica si es el siguiente nivel
        if self.isNextLevel():
            # Verifica si el planeta aún no ha sido creado
            if not self.planetCreated:
                # Agrega un planeta a la lista de planetas
                self.planets.append(self.createPlanet())
                # Aumenta el nivel
                self.level += 1
                # Marca que el planeta ha sido creado
                self.planetCreated = True

            # Verifica si todos los meteoros han sido destruidos
            if len(self.meteoros) == 0:
                # Si la nave aún no ha aterrizado en el planeta
                if not self.nave.rect.bottom < 0:
                    # Hace que la nave avance hacia el planeta
                    self.nave.rect.y -= 7
                    # Hace que la nave gire hasta 180 grados
                    self.nave.turnTill180()
                else:
                    # Verifica si el usuario ha pulsado la tecla C
                    keys = pg.key.get_pressed()
                    if keys[pg.K_c]:
                        # Inicia el siguiente nivel
                        self.newLevel()
                    else:
                        # Muestra el texto "Pulse C para continuar" en la pantalla
                        continueText = self.font.render("Pulse C para continuar", True, BLANCO)
                        continueRect = continueText.get_rect()
                        self.screen.blit(continueText, (WIDTH//2-continueRect.width//2, HEIGHT//1.5))

    def scoreBoard(self):
        # SCORE TEXT
        score = self.font.render(f'Score: {int(self.score/FPS)}', True, GRIS)  # renderizar el texto

        # Poner el texto arriba a la derecha
        spacer = 10
        scoreRect = score.get_rect()
        scoreRect.topleft = spacer, spacer

        self.screen.blit(score, scoreRect)  # Poner el texto en la pantalla
        #####################

        # LIVES TEXT
        lives = self.font.render(f'Lives: {self.nave.lives}', True, GRIS)  # renderizar el texto

        # Poner el texto arriba a la derecha
        spacer = 10
        livesRect = lives.get_rect()
        livesRect.topleft = spacer, scoreRect.height+spacer

        self.screen.blit(lives, livesRect)  # Poner el texto en la pantalla
        #####################

        # LEVEL TEXT
        level = self.font.render(f'Level {self.level}', True, GRIS)  # renderizar el texto

        # Poner el texto arriba a la derecha
        spacer = 10
        levelRect = level.get_rect()
        levelRect.topleft = WIDTH-levelRect.width-spacer, spacer

        self.screen.blit(level, levelRect)  # Poner el texto en la pantalla
        #####################
        
    def events(self):
        # eventos
        for event in pg.event.get():
            #si se cancela la pantalla que se pare el "while" del gameloop
            if event.type == pg.QUIT:
                sys.exit()

    def gameUpdate(self):
        self.events()
        self.screen.blit(self.gameBackground, (0, 0))

        # Game Elements

        self.levelManager()
        self.planetManager()
        self.bulletUpdate()
        self.nave.update()
        self.meteorManager()
        self.explosionManager()
        self.scoreBoard()

        self.score += 1
        self.scoreLevelStep += 1

        if self.nave.lives <= 0:
            self.game_over = True

        ###############

        self.clock.tick(FPS)
        pg.display.flip()

    def inicio(self):
        self.__init__(self.screen, self.clock, self.font)
        while not self.game_over:
            self.gameUpdate()


class PantallaMuerte:
    def __init__(self, screen, clock) -> None:
        self.screen = screen
        self.clock = clock

        self.backgroundImage = pg.image.load('images/pantallaMuerte.png')
        self.continueToMenu = False
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def checkForContinue(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_c]:
            self.continueToMenu = True

    def update(self):
        self.events()

        self.checkForContinue()
        self.screen.blit(self.backgroundImage, (0, 0))
    
        pg.display.flip()
        self.clock.tick(FPS)
    
    def inicio(self):
        self.__init__(self.screen, self.clock)
        while not self.continueToMenu:
            self.update()