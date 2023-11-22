import pygame as pg
import random
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, DEBUG

path = r'Zarate_enzo_juego\recursos\tramps\0.png'
class Tramp:
    def __init__(self, coord_x, coord_y, w, h,push,path=r'Zarate_enzo_juego\recursos\tramps\1.png', speed=5, damage=1, frame_rate = 60):
        self.__tramp_animation = sf.get_surface_from_spritesheet(path,8,1,(w,h),flip=True)
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed = speed
        self.update_time = pg.time.get_ticks()
        self.__frame_rate = frame_rate
        self.__initial_frame = 0
        self.__actual_img_animation = self.__tramp_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__damage = damage
        self.__push = push
        self.update_time = pg.time.get_ticks()
        
        

    @property
    def get_rect(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__rect'
        
        DEVUELVE:
        self.__rect (int): valor del dicho atributo.
        """
        return self.__rect


    @property
    def get_damage(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__damage'
        
        DEVUELVE:
        self.__damage (int): valor del dicho atributo.
        """
        return self.__damage
    
    @property
    def get_push(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__push'
        
        DEVUELVE:
        self.__push (int): valor del dicho atributo.
        """
        return self.__push
    
   
    

    def move(self):
        self.__move_x -= self.__speed
        if self.__move_x + self.__rect.width < 0:
            self.__move_y += 50
            if self.__move_y >= 650:
                self.__move_y = -50  # Cambia a -20 cuando llega al límite en y
            self.__move_x = ANCHO_VENTANA

    def do_animation(self):

        if self.__initial_frame > len(self.__tramp_animation)-1:
            self.__initial_frame = 0

        self.__actual_img_animation = self.__tramp_animation[self.__initial_frame]

        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            self.update_time = pg.time.get_ticks()

    def update(self):
        self.__rect.x = self.__move_x
        self.__rect.y = self.__move_y
        self.move()
        self.do_animation()

    def draw(self, screen:pg.Surface):
        if DEBUG:
            pg.draw.rect(self.__actual_img_animation, "Blue", self.__rect)
            
        screen.blit(self.__actual_img_animation, self.__rect)
