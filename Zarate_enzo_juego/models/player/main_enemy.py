import pygame as pg
from random import randint
from models.constantes import GROUND_LEVEL
from models.auxiliar import SurfaceManager as sf

class Enemigo():
    def __init__(self, coord_x, coord_y,w,h, frame_rate=100, speed_walk=6,speed_run = 7):
        
        self.__up_r = sf.get_surface_from_spritesheet(r'recursos\enemy\up.png', 1, 1,(w,h))
        self.__up_l = sf.get_surface_from_spritesheet(r'recursos\enemy\up.png', 1, 1,(w,h), flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet(r'recursos\enemy\walk.png', 3, 1,(w,h))
        self.__walk_l = sf.get_surface_from_spritesheet(r'recursos\enemy\walk.png', 3, 1,(w,h), flip=True)
        self.__die_r = sf.get_surface_from_spritesheet(r'recursos\enemy\die.png', 9, 1,(w,h))
        self.__die_l = sf.get_surface_from_spritesheet(r'recursos\enemy\die.png', 9, 1,(w,h), flip=True)
        self.__attack_r = sf.get_surface_from_spritesheet(r'recursos\enemy\atak.png', 3, 1,(w,h))
        self.__attack_l = sf.get_surface_from_spritesheet(r'recursos\enemy\atak.png', 3, 1,(w,h), flip=True)
        self.__fall_r = sf.get_surface_from_spritesheet(r'recursos\enemy\fall.png', 1, 1,(w,h))
        self.__fall_l = sf.get_surface_from_spritesheet(r'recursos\enemy\fall.png', 1, 1,(w,h), flip=True)
        
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__is_looking_right = True

        self.__gravity = -1
        self.__jump = 15
        self.__is_jumping = False
        self.__star_jump = False

        self.__frame_rate = frame_rate
        self.update_time = pg.time.get_ticks()
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_l
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()



    def move_and_fall(self):
        """
        Simula el movimiento automático y la caída del enemigo.
        """
        # Configura la animación de caminar hacia la izquierda
        self.__actual_animation = self.__walk_l
        self.__is_looking_right = False

        # Mueve al enemigo hacia abajo automáticamente (en el eje y)
        self.__move_y += self.__gravity
        self.__gravity += 1

        # Actualiza la posición del rectángulo del enemigo
        self.__rect.x = self.__move_x
        self.__rect.y = self.__move_y

        # Aplica la gravedad si el enemigo está en el aire o saltando
        if self.__move_y < GROUND_LEVEL:
            self.__actual_animation = self.__fall_l
        else:
            # Si el enemigo toca el suelo, reinicia la gravedad y la animación
            self.__gravity = -1
            self.__actual_animation = self.__walk_l

        # Actualiza la animación según el tiempo transcurrido
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            self.update_time = pg.time.get_ticks()

        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

    def update(self):
        """
        Actualiza el estado del enemigo.
        """
        self.move_and_fall()

    def draw(self, screen: pg.surface.Surface):
        """
        Dibuja al enemigo en la pantalla.

        Args:
            screen (pg.surface.Surface): Superficie de la pantalla.
        """
        screen.blit(self.__actual_animation[self.__initial_frame], self.__rect)