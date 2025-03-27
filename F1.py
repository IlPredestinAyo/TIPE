import numpy as np
import time

class F1():
	def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
		self.x = x
		self.y = y
		self.angle = angle
		self.vitesse = vitesse
		self.coef_accel = .4
		self.coef_angle = .2
		self.coef_frein = 3
		self.evo_frein = 2
		self.last_lap_time = time.time()

	def is_on_track(self, screen):
		return screen.get_at((int(self.x), int(self.y))) != (1, 1, 1)

	# Taux à valeur dans [0;1], fonctions appelées en sortie du modèle
	def accelerer(self, taux):
		self.vitesse += taux * self.coef_accel
	
	def freiner(self, taux):
		self.vitesse -= (self.vitesse**self.evo_frein/1000)*self.coef_frein

	def tourner_gauche(self, taux):
		self.angle += (1/self.vitesse + 10)*self.coef_angle*taux

	def tourner_droite(self, taux):
		self.angle -= (1/self.vitesse + 10)*self.coef_angle*taux

	def move(self, WIDTH, HEIGHT):
		self.x -= np.sin(self.angle) * self.vitesse
		self.y -= np.cos(self.angle) * self.vitesse
		self.x %= WIDTH
		self.y %= HEIGHT


	

	
