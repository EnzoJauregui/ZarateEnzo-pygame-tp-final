import pygame as pg
from auxiliar.constantes import DEBUG

class Plataform:
    def __init__(self, x, y, w, h,numb):
        
        self.__image = pg.image.load(r'Zarate_enzo_juego\recursos\plataforms\dos\{0}.png'.format(numb)).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (w, h))
        self.__rect = self.__image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
       
    @property
    def get_rect(self):
        """
        Obtiene el rectángulo asociado a la plataforma.

        DEVUELVE:
        pg.Rect: Rectángulo de la plataforma.
        """
        return self.__rect
   
    def draw(self, screen:pg.Surface):
        """
        Dibuja la plataforma en la pantalla.

        RECIBE:
        screen (pg.Surface): Superficie de la pantalla.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            
        screen.blit(self.__image, self.__rect)
       