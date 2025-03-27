import pygame
import math
from math import cos,sin,pi

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1024, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Déplacement du Vaisseau")

# Chargement du vaisseau
background_image = pygame.image.load("idurla.jpg")
screen.blit(background_image, (0,0))
ship_image = pygame.image.load("rb.png")  # Assurez-vous d'avoir une image nommée 'vaisseau.png'
ship_image = pygame.transform.scale(ship_image, (24, 48))


ship_image2 = pygame.image.load("fefe.png")  # Assurez-vous d'avoir une image nommée 'vaisseau.png'
ship_image2 = pygame.transform.scale(ship_image2, (24, 48))

# PARA CAPTEUR
taille_zone = 5
taille_zone_avant = 15
nombre_capteur = 7

#PARA MOUVEMENT
coef_accel = .2
coef_angle = .6

class F1 :
    def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0, coef_accel = coef_accel):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
        self.coef_accel = coef_accel
    
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
        self.vitesse += (self.capteur_avant() -.7)*self.coef_accel
        self.angle +=(.8 - self.capteur_avant())*(self.capteur_droit()-self.capteur_gauche())*coef_angle
        screen.set_at((int(self.x), int(self.y)), 255**2)

rb = F1(coef_accel=.3)
ferrari = F1(y=650)

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
        ferrari.vitesse += 0  # Accélération
    if keys[pygame.K_DOWN]:
        rb.vitesse -= 0.2  # Décélération

    rb.mouvement()
    ferrari.mouvement()
    
    # Calcul du déplacement
    rb.x -= math.sin(rb.angle) * rb.vitesse
    rb.y -= math.cos(rb.angle) * rb.vitesse
    
    ferrari.x -= math.sin(ferrari.angle) * ferrari.vitesse
    ferrari.y -= math.cos(ferrari.angle) * ferrari.vitesse
    
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
    
    # Affichage du vaisseau
    screen.blit(rotated_ship, rect.topleft)



    

    # Création du texte du score
    score_text = pygame.font.Font(None, 30).render(f" vitesse: {(rb.vitesse//.1)/10} \n angle: {((rb.angle%6.28)*180/3.14)//1}  ", True, (255, 255, 255))

    # Position du texte
    screen.blit(score_text, (20, 20))
    
    pygame.display.flip()
    clock.tick(50)  # 30 FPS

pygame.quit()