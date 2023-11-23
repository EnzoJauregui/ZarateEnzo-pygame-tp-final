import pygame as pg
from models.constantes import DEBUG, ANCHO_VENTANA

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, img_path = False):
        super().__init__()
        self.__load_img(img_path)
        
        self.__rect = self.image.get_rect(center=(x, y))
        self.__direction = direction
        self.__speed = 5
        self.__alive = True
        self.__damage = 2

    @property
    def rect(self):
        return self.__rect
    
    @property
    def is_alive(self):
        return self.__alive
    
    def __load_img(self, img_path: bool):
        if img_path:
            self.image = pg.image.load(r'Zarate_enzo_juego\recursos\bullet\1.png')
        else: 
            self.image = pg.Surface((4, 20))
            self.image.fill('Black')
    
    def check_collision(self, target: object):
        """
        Verifica si la bala ha colisionado con el objetivo.

        RECIBE:
        target: Objeto (Jugador o Enemigo) con el que se verifica la colisión.
        """
        return self.rect.colliderect(target.get_rect)

    def update(self):
        self.__rect.x += self.__speed if self.__direction else -self.__speed

        if 0 >= self.__rect.x <= ANCHO_VENTANA:
            self.kill()

       