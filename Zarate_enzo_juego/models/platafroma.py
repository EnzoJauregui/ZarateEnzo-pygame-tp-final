import pygame as pg
from models.constantes import DEBUG
from models.auxiliar import SurfaceManager as sf

class Plataform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h,numb):
        super().__init__()

        self.__image = pg.image.load(r'recursos\plataforms\dos\{0}.png'.format(numb)).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (w, h))
        self.__rect = self.__image.get_rect()
        self.__rect.x = x
        self.__rect.y = y
    
    @property
    def get_rect(self):
        return self.__rect
    
    def draw(self, screen):
        
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        screen.blit(self.__image, self.__rect)