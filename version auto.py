import pygame
import math
from math import cos,sin,pi

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1024, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen2 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
screen2.fill((255, 0, 0, 0))
pygame.display.set_caption("Déplacement du Vaisseau")

# Chargement du vaisseau
background_image = pygame.image.load("./circuits/idurla.jpg")
screen.blit(background_image, (0,0))
ship_image = pygame.image.load("./cars/rb.png")  # Assurez-vous d'avoir une image nommée 'vaisseau.png'
ship_image = pygame.transform.scale(ship_image, (24, 48))

ship_image2 = pygame.image.load("./cars/fefe.png")  # Assurez-vous d'avoir une image nommée 'vaisseau.png'
ship_image2 = pygame.transform.scale(ship_image2, (24, 48))

# PARA CAPTEUR
taille_zone = 5
taille_zone_avant = 10
nombre_capteur = 7

class F1 :
    def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
        self.coef_accel = .4
        self.coef_angle = .2
        self.coef_frein = 3
        self.evo_frein = 2

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


rb = F1()
ferrari = F1(y=650)
ferrari.coef_frein -= .2
ferrari.angle -= .5

# Boucle principale
i = 0
going = True
clock = pygame.time.Clock()
while going:
    screen.blit(background_image, (0, 0))  # img de fond
    going = rb.detecteur()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False

    rb.mouvement()
    ferrari.mouvement()
    
    x = rb.x
    y = rb.y
    
    xf = ferrari.x
    yf = ferrari.y

    # Calcul du déplacement
    rb.x -= math.sin(rb.angle) * rb.vitesse
    rb.y -= math.cos(rb.angle) * rb.vitesse
    
    ferrari.x -= math.sin(ferrari.angle) * ferrari.vitesse
    ferrari.y -= math.cos(ferrari.angle) * ferrari.vitesse

    #coloration
    i+=.01
    pygame.draw.line(screen2, (127+int(127*cos(i)), 127+int(127*cos(i + .66*pi)), 127+int(127*cos(i + 1.33 * pi)), 255), (int(rb.x), int(rb.y)), (x, y), 5)
    pygame.draw.line(screen2, (127+int(127*cos(i+1)), 127+int(127*cos(i+1 + .66*pi)), 127+int(127*cos(i+1 + 1.33 * pi)), 255), (int(ferrari.x), int(ferrari.y)), (xf, yf), 5)

    # Gestion des limites de l'écran (téléportation aux bords)
    rb.x %= WIDTH
    rb.y %= HEIGHT
    
    ferrari.x %= WIDTH
    ferrari.y %= HEIGHT
    
    # Rotation de l'image du vaisseau
    rotated_ship2 = pygame.transform.rotate(ship_image2, ferrari.angle*(180/3.14))
    rect = rotated_ship2.get_rect(center=(ferrari.x, ferrari.y))
    
    # Affichage du vaisseau
    screen.blit(rotated_ship2, rect.topleft)

    # Rotation de l'image du vaisseau
    rotated_ship = pygame.transform.rotate(ship_image, rb.angle*(180/3.14))
    rect = rotated_ship.get_rect(center=(rb.x, rb.y))

    screen.blit(screen2, (0, 0))
    
    # Affichage du vaisseau
    screen.blit(rotated_ship, rect.topleft)

    # Création du texte du score
    score_text = pygame.font.Font(None, 30).render(f" vitesse: {(rb.vitesse//.1)/10} \n angle: {((rb.angle%6.28)*180/3.14)//1}  ", True, (255, 255, 255))

    # Position du texte
    screen.blit(score_text, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)  # 30 FPS

pygame.quit()