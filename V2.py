from PIL import Image, ImageFilter
from math import cos, sin

# Lire l'image
img = Image.open( 'Suzuki.jpg' )


class F1 :
    def __init__(self, x = 430, y = 600, angle = 0, vitesse = 0):
        self.x = x
        self.y = y
        self.angle = angle
        self.vitesse = vitesse
    
    def capteur_avant(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = self.x + int((i*25*sin(self.angle))//1)
            y = self.y - int((i*25*cos(self.angle))//1)
            r = img.getpixel((x,y))
            t += sum(r)/(3*255)
        return t/7

    def capteur_gauche(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = self.x + int((i*15*sin(self.angle - 1.57))//1)
            y = self.y - int((i*15*cos(self.angle - 1.57))//1)
            r = img.getpixel((x,y))
            t += i*sum(r)/(3*255)
        return (21-t)/21

    def capteur_droit(self): #dessine les cercles du serpent
        t = 0
        for i in range(1,7):
            x = self.x + int((i*15*sin(self.angle + 1.57))//1)
            y = self.y - int((i*15*cos(self.angle + 1.57))//1)
            r = img.getpixel((x,y))
            t += i*sum(r)/(3*255)
        return (21-t)/21

    def deplacement(self):
        self.x += int((self.capteur_avant()**.25)*(25*sin(self.angle))//1)
        self.y -= int((self.capteur_avant()**.25)*(25*cos(self.angle))//1)
        self.angle -= (1-self.capteur_avant())**3*(self.capteur_droit())*1
        self.angle += (1-self.capteur_avant())**3*(self.capteur_gauche())*1

        for i in range(5) :
            for j in range(5):
                img.putpixel((ferrari.x+i,ferrari.y+j), ( 0, 255, 0))


ferrari = F1()

for _ in range(115):
    ferrari.deplacement()
#    print(ferrari.x,ferrari.y,ferrari.angle)
    
img.show()  


#print(ferrari.capteur_gauche())
#print(ferrari.capteur_droit())
#print(ferrari.capteur_avant())