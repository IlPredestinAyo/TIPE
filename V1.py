from PIL import Image, ImageFilter
from math import cos, sin

# Lire l'image
img = Image.open( 'monoco.jpg' )


class F1 :
    def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
    
    def capteur_avant(self): #dessine les cercles du serpent
        x = self.x + int((20*sin(self.angle))//1)
        y = self.y - int((20*cos(self.angle))//1)
        img.putpixel((x+i,y+j), ( 255, 255, 0))
        r = img.getpixel((x,y))
        return sum(r) < 500

    def capteur_gauche(self): #dessine les cercles du serpent
        x = self.x + int((40*sin(- self.angle - 1.57))//1)
        y = self.y + int((40*cos(- self.angle - 1.57))//1)
        img.putpixel((x+i,y+j), ( 255, 0, 0))
        r = img.getpixel((x,y))
        return sum(r) > 500

    def capteur_droit(self): #dessine les cercles du serpent
        x = self.x + int((40*sin(- self.angle + 1.57))//1)
        y = self.y + int((40*cos(- self.angle + 1.57))//1)
        img.putpixel((x+i,y+j), ( 0, 0, 255))
        r = img.getpixel((x,y))
        return sum(r) > 500

    def deplacement(self):
        self.capteur_gauche()
        self.capteur_droit()
        self.capteur_avant()
        if not(self.capteur_avant()) :
            self.x += int((5*sin(self.angle))//1)
            self.y -= int((5*cos(self.angle))//1)
        else :
            if not(self.capteur_droit()) :
                self.angle -= 0.3
            if not(self.capteur_gauche()) :
                self.angle += 0.3

        for i in range(5) :
            for j in range(5):
                img.putpixel((ferrari.x+i,ferrari.y+j), ( 0, 255, 0))

ferrari = F1()

for i in range(5):
    for j in range(5):
        img.putpixel((ferrari.x+i,ferrari.y+j), ( 0, 255, 0)) 

for _ in range(2000):
    ferrari.deplacement()
    print(ferrari.x,ferrari.y,ferrari.angle)
    
img.show()  



print(ferrari.capteur_gauche())
print(ferrari.capteur_droit())
print(ferrari.capteur_avant())