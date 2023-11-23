from typing import Any
import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, GROUND_LEVEL
import random

class Fruit(pg.sprite.Sprite):
    def __init__(self,x, y, w, h, increase_life, increase_points, frame_rate = 60):
        super().__init__()
        self.__actual_animation = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego/recursos/Fruits/Apple.png',17, 1,(w,h))
        self.__frame_rate = frame_rate
        self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__increase_life = increase_life
        self.increase_points = increase_points
        self.__points = False
        self.update_time = pg.time.get_ticks()
        

    @property
    def get_rect(self):
        return self.__rect

    @property
    def get_increase(self):
        return self.__increase_life
    
    def increase_life(self, player):
        if self.__rect.colliderect(player.get_rect):
            player.increase_life_points(self.__increase_life)
            player.increase_points(self.increase_points)
            print(f"Puntos de vida incrementados: {player.get_life_points}")
            print(f"Puntos incrementados: {player.get_points}")
            return True
        
    def do_animation(self):
        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            
            self.update_time = pg.time.get_ticks()
        
    
    def update(self,player, *args: Any, **kwargs: Any) -> None:
        self.increase_life(player)
        self.do_animation()
        return super().update(*args, **kwargs)

    def draw(self,screen:pg.Surface):
        screen.blit(self.__actual_img_animation, self.__rect)
    
    @staticmethod
    def generate_fruits(num_fruits):
        fruits = []
        for _ in range(num_fruits):
            x = random.randint(50, ANCHO_VENTANA - 50)
            y = random.randint(150, GROUND_LEVEL)
            increase_life = random.randint(5, 15)  
            increase_points = random.randint(10, 70) 
            fruit = Fruit(x, y, 50, 50, increase_life, increase_points)
            fruits.append(fruit)
        return fruits


