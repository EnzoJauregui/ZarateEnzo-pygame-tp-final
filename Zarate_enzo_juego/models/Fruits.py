from typing import Any
import pygame as pg
from models.auxiliar import SurfaceManager as sf
import random

class Fruit(pg.sprite.Sprite):
    def __init__(self,x, y, w, h, increase, frame_rate = 60):
        super().__init__()
        self.__actual_animation = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego/recursos/Fruits/Apple.png',17, 1,(w,h))
        self.__frame_rate = frame_rate
        self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__increase = increase
        self.update_time = pg.time.get_ticks()
        

    @property
    def get_rect(self):
        return self.__rect

    @property
    def get_increase(self):
        return self.__increase
    
    def do_animation(self):
        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            self.update_time = pg.time.get_ticks()
            
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        
        self.do_animation()
        return super().update(*args, **kwargs)

    
    def draw(self,screen:pg.Surface):
        screen.blit(self.__actual_img_animation, self.__rect)
    



