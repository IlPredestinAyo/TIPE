import pygame
import numpy as np
import time
import F1

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

ship_image = pygame.image.load("./cars/fefe.png") 
ship_image = pygame.transform.scale(ship_image, (24, 48))

ferrari = F1.F1()

# Initialisation du chronomètres
start_time = time.time()

i = 0
going = True
clock = pygame.time.Clock()
while going:
	screen.blit(background_image, (0, 0))  # img de fond
	going = ferrari.detecteur()

	# Gestion des événements
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			going = False

	ferrari.mouvement()
	
	xf = ferrari.x
	yf = ferrari.y
	
	ferrari.x -= np.sin(ferrari.angle) * ferrari.vitesse
	ferrari.y -= np.cos(ferrari.angle) * ferrari.vitesse

	#coloration
	i+=.01
	pygame.draw.line(screen2, (127+int(127*np.cos(i+1)), 127+int(127*np.cos(i+1 + .66*np.pi)), 127+int(127*np.cos(i+1 + 1.33 * np.pi)), 255), (int(ferrari.x), int(ferrari.y)), (xf, yf), 5)
	
	ferrari.x %= WIDTH
	ferrari.y %= HEIGHT
	
	# Rotation de l'image du vaisseau
	rotated_ship = pygame.transform.rotate(ship_image, ferrari.angle*(180/np.pi))
	rect = rotated_ship.get_rect(center=(ferrari.x, ferrari.y))
	
	# Affichage du vaisseau
	screen.blit(rotated_ship, rect.topleft)

	screen.blit(screen2, (0, 0))

	# Création du texte du score
	score_text = pygame.font.Font(None, 30).render(
	    f"vitesse: {(ferrari.vitesse//.1)/10} \nangle: {((ferrari.angle%6.28)*180/np.pi)//1}", 
	    True, 
	    (255, 255, 255)
	)

	# Position du texte
	screen.blit(score_text, (20, 20))

	if int(ferrari.x) == 430 and int(ferrari.y) == 600:  # trouver une meilleure condition pour le tour
		lap_time = time.time() - start_time
		print(f"Durée du tour: {lap_time:.2f} secondes")
		start_time = time.time()  # Réinitialisation du temps de départ pour le prochain tour

	pygame.display.flip()
	clock.tick(60)

pygame.quit()