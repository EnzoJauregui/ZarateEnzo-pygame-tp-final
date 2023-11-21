import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA

class Tramp:
    def __init__(self, coord_x, coord_y, w, h,empuje, speed=5, damage=10):
        self.__trap_image = pg.image.load(r'Zarate_enzo_juego\recursos\tramps\0.png')
        self.__trap_image = pg.transform.scale(self.__trap_image,(w, h))
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed = speed
        self.__rect = self.__trap_image.get_rect()
        self.__damage = damage
        self.__empuje = empuje

    @property
    def get_rect(self):
        """
        Devuelve el valor del atributo privado 'self.__rect'
        
        DEVUELVE:
        self.__rect (int): valor del dicho atributo.
        """
        return self.__rect

    @property
    def get_damage(self):
        """
        Devuelve el valor del atributo privado 'self.__damage'
        
        DEVUELVE:
        self.__damage (int): valor del dicho atributo.
        """
        return self.__damage
    @property
    def get_empuje(self):
        """
        Devuelve el valor del atributo privado 'self.__empuje'
        
        DEVUELVE:
        self.__empuje (int): valor del dicho atributo.
        """
        return self.__empuje

    def move(self):
        self.__move_x -= self.__speed
        if self.__move_x + self.__rect.width < 0:
            self.__move_x = ANCHO_VENTANA

    def update(self):
        self.move()

    def draw(self, screen):
        screen.blit(self.__trap_image, (self.__move_x, self.__move_y))
