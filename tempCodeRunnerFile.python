import pygame
import math
from math import cos,sin

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1024, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Déplacement du Vaisseau")

# Chargement du vaisseau
background_image = pygame.image.load("idurla.jpg")
screen.blit(background_image, (0,0))
ship_image = pygame.image.load("fefe.png")  # Assurez-vous d'avoir une image nommée 'vaisseau.png'
ship_image = pygame.transform.scale(ship_image, (20, 40))

class F1 :
    def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
    
    def capteur_avant(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = int(self.x) + int(i*15*cos(self.angle + 1.57))
            y = int(self.y) - int(i*15*sin(self.angle + 1.57))
            r = screen.get_at(( x, y))
            t += sum(r)/(3*255)
        return t/7

    def capteur_gauche(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = int(self.x) + int(i*10*cos(self.angle + 3.14))
            y = int(self.y) - int(i*10*sin(self.angle + 3.14))
            r = screen.get_at(( x, y))
            t += i*sum(r)/(3*255)
        return (21-t)/21

    def capteur_droit(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = int(self.x) + int(i*10*cos(self.angle))
            y = int(self.y) - int(i*10*sin(self.angle))
            r = screen.get_at(( x, y))
            t += i*sum(r)/(3*255)
        return (21-t)/21

    def mouvement(self) :
        self.vitesse += (self.capteur_avant() -.7)*.1
        self.angle -=(.8 - self.capteur_avant())*(self.capteur_gauche()-self.capteur_droit())*.2
        screen.set_at((int(self.x), int(self.y)), 255**2)

rb = F1()

# Boucle principale
going = True
clock = pygame.time.Clock()
while going:
    screen.blit(background_image, (0, 0))  # img de fond
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
    
    # Contrôles du vaisseau
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rb.angle += .1  # Rotation à gauche
    if keys[pygame.K_RIGHT]:
        rb.angle -= .1  # Rotation à droite
    if keys[pygame.K_UP]:
        rb.vitesse += 0.1  # Accélération
    if keys[pygame.K_DOWN]:
        rb.vitesse -= 0.2  # Décélération

    rb.mouvement()
    
    # Calcul du déplacement
    rb.x -= math.sin(rb.angle) * rb.vitesse
    rb.y -= math.cos(rb.angle) * rb.vitesse
    
    # Gestion des limites de l'écran (téléportation aux bords)
    rb.x %= WIDTH
    rb.y %= HEIGHT
    
    # Rotation de l'image du vaisseau
    rotated_ship = pygame.transform.rotate(ship_image, rb.angle*(180/3.14))
    rect = rotated_ship.get_rect(center=(rb.x, rb.y))
    
    # Affichage du vaisseau
    screen.blit(rotated_ship, rect.topleft)

    # Création du texte du score
    score_text = pygame.font.Font(None, 30).render(f" vitesse: {(rb.vitesse//.1)/10} \n angle: {((rb.angle%6.28)*180/3.14)//1}  ", True, (255, 255, 255))

    # Position du texte
    screen.blit(score_text, (20, 20))
    
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()