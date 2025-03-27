import pygame
import math
from math import cos,sin,pi

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1024, 1024
FPS = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
relevé = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
relevé.fill((255, 0, 0, 0))
pygame.display.set_caption("F1")

# Chargement du circuit
circuit = ["idurla","Suzuki","monoco"]
background_image = pygame.image.load(circuit[0]+".jpg")
screen.blit(background_image, (0,0))

# PARA CAPTEUR
taille_zone = 5
taille_zone_avant = 10
nombre_capteur = 7

class F1 :
    def __init__(self, sprite, x = 430, y = 600, angle = 0):
        self.sprite = sprite
        # position
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = 0
        # variables
        self.coef_accel = .4
        self.coef_angle = .2
        self.coef_frein = 3
        self.evo_frein = 2
        # image
        self.image = pygame.image.load(self.sprite + ".png")
        self.image = pygame.transform.scale(self.image, (24, 48))

    def detecteur(self):
        return sum(screen.get_at(( int(self.x), int(self.y))))>300
    
    def capteur(self, taille, nombre, angle): 
        t = 0
        for i in range(1,nombre):
            x = int(self.x + i*taille_zone_avant*cos(self.angle + angle))
            y = int(self.y - i*taille_zone_avant*sin(self.angle + angle))
            r = screen.get_at(( x % WIDTH, y % HEIGHT))
            t += sum(r)/(3*255)
        return t/nombre
    
    def capteur_avant(self) :
        return self.capteur(taille_zone_avant, nombre_capteur, pi/2)

    def capteur_gauche(self): 
        return 1 - self.capteur(taille_zone_avant, nombre_capteur, pi)

    def capteur_droit(self): 
        return 1 - self.capteur(taille_zone_avant, nombre_capteur, 0)

    def mouvement(self) :
        if (self.capteur_avant() -.7)>0 :
            self.vitesse += (self.capteur_avant() -.7)*self.coef_accel
        else : 
            self.vitesse -= (self.vitesse**self.evo_frein/1000)*self.coef_frein
        self.angle +=(1/self.capteur_avant())*(self.capteur_droit()-self.capteur_gauche())*self.coef_angle
        screen.set_at((int(self.x), int(self.y)), 255**2)
    
    def animer(self) :
    # Calcul du déplacement
        x, y = self.x, self.y
        self.x -= math.sin(self.angle) * self.vitesse
        self.y -= math.cos(self.angle) * self.vitesse

        # Gestion des limites de l'écran (téléportation aux bords)
        self.x %= WIDTH
        self.y %= HEIGHT

        # Rotation de l'image du vaisseau
        rotated_ship = pygame.transform.rotate(self.image, self.angle*(180/3.14))
        rect = rotated_ship.get_rect(center=(self.x, self.y))
        
        pygame.draw.line(relevé, (127+int(127*cos(self.vitesse/10)), 127+int(127*cos(self.vitesse/10 + .66*pi)), 127+int(127*cos(self.vitesse/10 + 1.33 * pi)), 255), (int(self.x), int(self.y)), (x, y), 2)
        screen.blit(relevé, (0, 0))

        # Affichage du vaisseau
        screen.blit(rotated_ship, rect.topleft)
        
rb = F1("rb")
ferrari = F1("fefe",y=620)
maclaren = F1("mc",y=640)
mercedes = F1("merco",y=660)

Grille = [rb, ferrari, maclaren, mercedes]

# Boucle principale
i = 0
going = True
clock = pygame.time.Clock()
while going:

    screen.blit(background_image, (0, 0))  # img de fond
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
    
    for voiture in Grille :
        voiture.mouvement()
        voiture.animer()
    
    # Création du texte du score
    score_text = pygame.font.Font(None, 30).render(f" vitesse: {(rb.vitesse//.1)/10} \n angle: {((rb.angle%6.28)*180/3.14)//1}  ", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    
    pygame.display.flip()
    clock.tick(FPS)  # 30 FPS

pygame.quit()