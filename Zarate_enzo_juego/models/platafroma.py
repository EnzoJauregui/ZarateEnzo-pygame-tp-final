import pygame as pg
from models.constantes import DEBUG, HEIGHT_RECT
from models.auxiliar import SurfaceManager as sf

class Plataform:
    def __init__(self, x, y, w, h,numb):
        self.__image = pg.image.load(r'Zarate_enzo_juego\recursos\plataforms\dos\{0}.png'.format(numb)).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (w, h))
        self.__rect = self.__image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__rect_ground_colition = pg.Rect(self.__rect.x, self.__rect.y, self.__rect.w, HEIGHT_RECT)
        self.__rect_top_colition = pg.Rect(self.__rect.x, self.__rect.y+ self.__rect.h, self.__rect.w, HEIGHT_RECT)
    
    @property
    def get_rect_ground_colition(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__rect_ground_colition'
        
        DEVUELVE:
        self.__rect_ground_colition (int): valor del dicho atributo.
        """
        return self.__rect_ground_colition
    
    @property
    def get_rect_top_colition(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__rect_top_colition'
        
        DEVUELVE:
        self.__rect_top_colition (int): valor del dicho atributo.
        """
        return self.__rect_top_colition
    
    def draw(self, screen):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        screen.blit(self.__image, self.__rect)
        pg.draw.rect(screen, "Green", self.__rect_ground_colition)
        pg.draw.rect(screen, "Green", self.__rect_top_colition)