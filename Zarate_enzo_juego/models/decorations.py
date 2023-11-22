import pygame as pg
class Decorations:
    def __init__(self, x,y,w,h) -> None:
        self.__img = pg.image.load(r'Zarate_enzo_juego\recursos\0.png')
        self.__img =pg.transform.scale(self.img, (w,h))
        self.__rect = self.__img.get_rect()
        self.__rect.x = x
        self.__rect.y = y

    

    

    def draw(self,screen):
        screen.blit(self.__img, self.__rect)