import pygame
import numpy as np
import time

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

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
ship_image = pygame.image.load("./cars/rb.png")
ship_image = pygame.transform.scale(ship_image, (24, 48))

ship_image2 = pygame.image.load("./cars/fefe.png") 
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
		return screen.get_at((int(self.x), int(self.y))) != (1, 1, 1)
	
	def capteur(self, taille, nombre, angle): 
		t = 0
		for i in range(1,nombre):
			x = int(self.x + i*taille_zone_avant*np.cos(self.angle + angle))
			y = int(self.y - i*taille_zone_avant*np.sin(self.angle + angle))
			r = screen.get_at(( x % WIDTH, y % HEIGHT))
			t += sum(r)/(3*255)
		return t/nombre
	
	def capteur_avant(self) :
		return self.capteur(taille_zone_avant, nombre_capteur, np.pi/2)

	def capteur_gauche(self): 
		return 1 - self.capteur(taille_zone_avant, nombre_capteur, np.pi)

	def capteur_droit(self): 
		return 1 - self.capteur(taille_zone_avant, nombre_capteur, 0)

	# Taux à valeur dans [0;1], fonctions appelées en sortie du modèle
	def accelerer(self, taux):
		self.vitesse += taux * self.coef_accel
	
	def freiner(self, taux):
		self.vitesse -= (self.vitesse**self.evo_frein/1000)*self.coef_frein

	def tourner_gauche(self, taux):
		self.angle += (1/self.vitesse + 10)*self.coef_angle*taux

	def tourner_droite(self, taux):
		self.angle -= (1/self.vitesse + 10)*self.coef_angle*taux
    


rb = F1()
ferrari = F1(y=650)
ferrari.coef_frein -= .2
ferrari.angle -= .5

# Initialisation des chronomètres
start_time = time.time()

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
	rb.x -= np.sin(rb.angle) * rb.vitesse
	rb.y -= np.cos(rb.angle) * rb.vitesse
	
	ferrari.x -= np.sin(ferrari.angle) * ferrari.vitesse
	ferrari.y -= np.cos(ferrari.angle) * ferrari.vitesse

	#coloration
	i+=.01
	pygame.draw.line(screen2, (127+int(127*np.cos(i)), 127+int(127*np.cos(i + .66*np.pi)), 127+int(127*np.cos(i + 1.33 * np.pi)), 255), (int(rb.x), int(rb.y)), (x, y), 5)
	pygame.draw.line(screen2, (127+int(127*np.cos(i+1)), 127+int(127*np.cos(i+1 + .66*np.pi)), 127+int(127*np.cos(i+1 + 1.33 * np.pi)), 255), (int(ferrari.x), int(ferrari.y)), (xf, yf), 5)

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
	
	if int(rb.x) == 430 and int(rb.y) == 600: # trouver une meilleure condition pour le tour
		lap_time = time.time() - start_time
		print(f"Durée du tour: {lap_time:.2f} secondes")
		start_time = time.time()  # Réinitialisation du temps de départ pour le prochain tour

	pygame.display.flip()
	clock.tick(60)

pygame.quit()