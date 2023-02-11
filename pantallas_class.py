import pygame as pg
from utils.__init__ import *
from planet import Planet





class Game():
    clock = pg.time.Clock() #reloj para controlar fps

    def __init__(self):
        self.display = pg.display
        self.main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla
        self.display.set_caption("THE COLONIZERS by Juan_A Espin")#Nombre del juego en la pantalla




        self.score = 0
        self.meter_list = pg.sprite.Group()#meteoros grupo
        self.all_sprite_list = pg.sprite.Group()
        self.fondo= pg.image.load('images/fondo.png') #imagen fondo mde pantalla

        for i in range(60): #crear meteoros 
            meter = Meter() #llamar clase
            meter.rect.x= random.randrange(800)#para que aparezcan los meteoros aleatoriamente
            meter.rect.y = random.randrange(600)

            self.meter_list.add(meter)#agregar elementos a la lista
            self.all_sprite_list.add(meter)

        self.nave = Nave()
        self.all_sprite_list.add(self.nave)    


    def hand_leevent(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
               return  True

        return False  

    def render(self,main_screen, dt):
        self.main_screen = pg.image.load('images/fondo.png') #imagen fondo mde pantalla   
        #self.main_screen.fill(BLANCO)
        self.all_sprite_list.draw(main_screen)#dibujar lista de todos los sprites en la pantalla
        pg.display.flip() 
        self.display.flip()

    def bucle_principal(self):
        game_over = False

        while game_over == False:
            dt = self.clock.tick(40)

            game_over = self.hand_leevent()

            #main_screen.fill

         





    def correr_logica(self):
        self.all_sprite_list.update()
        self.meter_list_collide = pg.sprite.spritecollide(self.nave, self.meter_list, True)

        for self.meter in self.meter_list_collide:
            self.score +=1
            
'''''
    def marco_visual(self, main_screen):
        main_screen.blit(self.fondo,[0,0])   #posicionamiento imagend e fondo
        

        self.all_sprite_list.draw(main_screen)#dibujar lista de todos los sprites en la pantalla
        pg.display.flip() 
'''



class MenuInicial:
    def __init__(self, screen, clock, font) -> None:
        self.screen = screen
        self.clock = clock
        self.font = font

        self.fondoMenuPrincipal = pg.image.load("images/menuBackground.png")

        self.menuPrincipal = pg.image.load("images/menuPrincipal.png")
        self.menuPrincipal = pg.transform.scale(self.menuPrincipal, (WIDTH, HEIGHT))


        self.planetImages = self.getListOfAnimationImages("images/earthSpriteSheet.png", 50)
        for i in range(len(self.planetImages)):
            image = self.planetImages[i]
            image = pg.transform.scale(image, (HEIGHT//1.5, HEIGHT//1.5))
            image.set_colorkey((0, 0, 0))
            self.planetImages[i] = image

        self.planeta = Planet(self.screen, self.planetImages, inGame=False)

        self.continueToGame = False

    def getListOfAnimationImages(self, spriteSheet, numOfImages):
        images = []
        spriteSheet = pg.image.load(spriteSheet).convert()
        spriteWidth = spriteSheet.get_width() // numOfImages
        for i in range(numOfImages):
            image = spriteSheet.subsurface(pg.Rect(i * spriteWidth, 0, spriteWidth, spriteSheet.get_height()))
            images.append(image)

        return images

    def events(self):
        # eventos
        for event in pg.event.get():
            #si se cancela la pantalla que se pare el "while" del gameloop
            if event.type == pg.QUIT:
                pg.quit()
    
    def checkForContinue(self):
        keys = pg.key.get_pressed()
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
        while not self.continueToGame:
            self.update()










def main():
    pg.init()
    main_screen = pg.display.set_mode((WIDTH,HEIGHT))#tamaño pantalla
    done = False
    clock = pg.time.Clock() #reloj para controlar fps

    game =Game()
    while not done:
        done = game.hand_leevent()
        game.correr_logica()
        clock.tick(40)
    pg.quit()    
    sys.exit()


    

if __name__=="__main__":   
    main()        