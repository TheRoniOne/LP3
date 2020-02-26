import pygame,random,sys

class Bloque(pygame.sprite.Sprite):
    def __init__(self,x,y,hp,color):
        pygame.sprite.Sprite.__init__(self) #llamada al constructor de la clase padre
        self.image = pygame.Surface((80,30)) #creacion del sprite
        self.image.fill(color) #da color
        self.rect = self.image.get_rect() #se le da hitbox
        self.rect.x = x #posicionamiento
        self.rect.y = y #posicionamiento
        self.hp = hp #numero de vidas del bloque
        
    def colorear(self,pelota):
        self.hp -=1
        if (self.hp == 1):
            self.image.fill((0,255,0))
        elif (self.hp == 0):
            self.image.fill((255,0,0))
        else:
            pygame.sprite.Sprite.kill(self) #si ya se acabaron las vidas del bloque, se destruye
            pelota.puntaje += 1

class Almacen(Bloque):
    def __init__(self):
        pass
    
    def generar(self,bloques): #generacion de bloques y coloreado inicial
        for j in range(3):
            for i in range(10):
                rnd = random.randint(0,2)
                if (rnd == 2):
                    color = (0,0,255) 
                elif (rnd == 1):
                    color = (0,255,0)
                elif (rnd == 0):
                    color = (255,0,0)
                bloque = Bloque(i*80,j*30,rnd,color)
                bloques.add(bloque)

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #llamada al constructor de la clase padre
        self.image = pygame.Surface((27,27)) #creacion del sprite
        self.rect = self.image.get_rect() #se recrea su hitbox
        self.velocidad = [7,-7] #velocidad de la pelota
        self.vidas = 3 #vidas del jugador al iniciar el juego
        self.ejecutando = True
        self.puntaje = 0
        
    def posicionar(self):
        self.rect.x = 400-self.rect.width+15 #posicionamiento en x
        self.rect.y = 600-self.rect.height-20 #posicionamiento en y
        
    def mover(self,barraRect): #movimiento de la pelota
        self.rect.x += self.velocidad[0]
        self.rect.y += self.velocidad[1]
        
        if (self.rect.y + self.rect.height >= 581): #logica de cambio de direccion si choca con barra
            if (self.rect.colliderect(barraRect)):
                self.velocidad[1] = -1*self.velocidad[1]
            else:
                self.ejecutando = False #si no ha chocado con la barra es porque ya se le fue la bola y ha perdido
                self.vidas -= 1
        
        if ((self.rect.x >= (800 - self.rect.width)) or (self.rect.x <= 0)): #si la pelota se trata de salir por un costado, se le cambia la direccion de movimiento
            self.velocidad[0] = -1*self.velocidad[0]
            self.rect.x = 800 - self.rect.width
        if (self.rect.y < 0):
            self.velocidad[1] = -1*self.velocidad[1]
            self.velocidad[1] = 0
        
    def chocar(self,colisiones): #efecto de cuando la pelota golpea un bloque
            rnd = random.randint(0,1)
            if (rnd ==0):
                self.velocidad[0] = -1*self.velocidad[0]
            self.velocidad[1] = -1*self.velocidad[1]
            colisiones[0].colorear(self)
            if (self.puntaje == 30):
                self.ejecutando = False

class Barra(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #llamada al constructor de la clase padre
        self.img = pygame.Surface((100,20)) #creacion del sprite
        self.img.fill((100,100,100)) #da color
        self.rect = self.img.get_rect() #se le da hitbox
        
    def posicionar(self):
        self.rect.x = 400-self.rect.width +50 #posicionamiento en x
        self.rect.y = 600-self.rect.height #posicionamiento en y
    
    def mover(self,direc):
        if (not (self.rect.x > (800-self.rect.width) and (direc == 10))) and (not((self.rect.x < 0) and (direc ==-10))):
            self.rect.x = self.rect.x + direc #mover la barra
            
    def moverConPelota(self,direc,pelota):
        if (not (self.rect.x > (800-self.rect.width) and (direc == 10))) and (not((self.rect.x < 0) and (direc ==-10))):
            self.rect.x = self.rect.x + direc #mover la barra
            pelota.rect.x = pelota.rect.x + direc #mover la pelota junto a la barra
            
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    reloj = pygame.time.Clock()
    
    bloques = pygame.sprite.Group() #crea un grupo de Sprites para los bloques
    
    almacen = Almacen()
    almacen.generar(bloques)
    barra = Barra()
    pelota = Pelota()
    fuente = pygame.font.SysFont('Showcard Gothic', 100)
    fuente1 = pygame.font.SysFont('Showcard Gothic', 50)
    fuente2 = pygame.font.SysFont('Showcard Gothic', 45)
    
    while (pelota.vidas >= 1) and (pelota.puntaje != 30):
        
        pelota.posicionar() #iniciar la posicion de la pelota
        barra.posicionar() #iniciar la posicion de la barra
        cond = False
        pelota.ejecutando = True
        
        while pelota.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if (evento.key == pygame.K_SPACE):
                        cond = True
            
            if (cond): #si ya presiono space, se inicia el movimiento de la pelota
                pelota.mover(barra.rect) #movimiento normal de la pelota
                texto = fuente1.render("",False,(0,0,0))
                texto1 = fuente1.render("",False,(0,0,0))
                texto2 = fuente2.render("",False,(0,0,0))
            else:
                if (pelota.vidas == 3): #genera texto a mostrar segun las condiciones
                    texto = fuente1.render("Presione SPACE para iniciar",False,(0,0,0))
                    texto1 = fuente1.render("",False,(0,0,0))
                    texto2 = fuente2.render("",False,(0,0,0))
                else:
                    texto = fuente1.render("",False,(0,0,0))
                    texto1 = fuente1.render("Le quedan " + str(pelota.vidas) + " vidas.", False, (0,0,0))
                    texto2 = fuente2.render("Presione space para continuar", False, (0,0,0))
                    
            colisiones = pygame.sprite.spritecollide(pelota, bloques, False) #devuelve una lista de colisiones entre la pelota y los bloques
                
            if (len(colisiones) >= 1): #si la lista no esta vacia es porq la pelota ha chocado con un bloque
                pelota.chocar(colisiones)
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]: #si se presiona la tecla derecha o izquierda se mueve la barra
                if not (cond):
                    barra.moverConPelota(-10,pelota)
                else:
                    barra.mover(-10)
                    
            if keys[pygame.K_RIGHT]:
                if not (cond):
                    barra.moverConPelota(10,pelota)
                else:
                    barra.mover(10)
            
            pantalla.fill((70, 242, 216))
            pantalla.blit(barra.img,barra.rect)
            pygame.draw.circle(pantalla,(100,100,100),(int(pelota.rect.x + pelota.rect.width/2), int(pelota.rect.y + pelota.rect.height/2)), 15)
            bloques.draw(pantalla)
            pantalla.blit(texto, (40,250))
            pantalla.blit(texto1, (180,250))
            pantalla.blit(texto2, (40,310))
            pygame.display.flip()
            reloj.tick(60)
            
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if pelota.vidas >=1:
            texto = fuente.render("YOU WIN!",False, (0,0,0))
            pantalla.blit(texto, (150,250))
        else:
            texto = fuente.render("GAME OVER!",False, (0,0,0))
            pantalla.blit(texto, (100,250))
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
