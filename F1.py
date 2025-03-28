import numpy as np
import time

class F1():
	def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
		self.x = x
		self.y = y
		self.previous_y = y
		self.angle = angle
		self.vitesse = vitesse
		self.coef_accel = .4
		self.coef_angle = .2
		self.coef_frein = 3
		self.evo_frein = 2
		self.last_lap_start = time.time()
		self.last_lap_time = None
		self.lap_count = 0

	def is_on_track(self, screen):
		return sum(screen.get_at((int(self.x), int(self.y)))) > 100

	# Taux à valeur dans [0;1], fonctions appelées en sortie du modèle
	def accelerer(self, taux):
		self.vitesse += taux * self.coef_accel
	
	def freiner(self, taux):
		self.vitesse -= (self.vitesse**self.evo_frein/1000)*self.coef_frein*taux

	def tourner_gauche(self, taux):
		self.angle += (1/self.vitesse + 10)*self.coef_angle*taux

	def tourner_droite(self, taux):
		self.angle -= (1/self.vitesse + 10)*self.coef_angle*taux

	def move(self, WIDTH, HEIGHT):
		self.x -= np.sin(self.angle) * self.vitesse
		self.y -= np.cos(self.angle) * self.vitesse
		self.x %= WIDTH
		self.y %= HEIGHT

	# Chronomètre le temps du dernier tour, met à jour le nombre de tours
	def lap(self):
		t = time.time()
		self.last_lap_time = t - self.last_lap_start
		self.last_lap_start = t
		self.lap_count += 1

	def is_gripping(self):
		pass

	def crosses_finish_line(self, x1, x2, yl):
		""" 
		On vérifie, dans l'ordre, si :
			La voiture a son abcisse à l'endroit de la ligne d'arrivée
			La voiture passe par dessus la ligne d'arrivée grâce à son ordonnée précédente
			La voiture est orientée dans le bon sens afin d'empêcher la triche
			La voiture a une vitesse afin de l'empêcher de rester sur la ligne d'arrivée
		"""
		return x1 <= self.x <= x2 and self.previous_y <= yl <= self.y and -np.pi/2 < self.angle % (2*np.pi) < np.pi/2 and self.vitesse != 0
	