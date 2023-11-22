import pygame as pg
import random
from models.platafroma import Plataform
from models.constantes import GROUND_LEVEL, ANCHO_VENTANA, PUSH
from models.auxiliar import SurfaceManager as sf

class Enemigo():
    def __init__(self, coord_x, coord_y,w,h, speed_walk,damage, frame_rate=100):
        
        self.__up_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\up.png', 1, 1,(w,h))
        self.__up_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\up.png', 1, 1,(w,h), flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\walk.png', 3, 1,(w,h))
        self.__walk_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\walk.png', 3, 1,(w,h), flip=True)
        self.__die_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\die.png', 9, 1,(w,h))
        self.__die_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\die.png', 9, 1,(w,h), flip=True)
        self.__attack_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\atak.png', 3, 1,(w,h))
        self.__attack_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\atak.png', 3, 1,(w,h), flip=True)
        self.__fall_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\fall.png', 1, 1,(w,h))
        self.__fall_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\fall.png', 1, 1,(w,h), flip=True)
        
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_atak = self.__speed_walk*1.5
        self.__is_looking_right = True
        self.__plataform_colition = False
        self.__gravity = -1
        self.__is_on_ground = False
        self.__damage = damage
        self.__push = PUSH

        self.__collite_top = False        
        self.__frame_rate = frame_rate
        self.update_time = pg.time.get_ticks()

        self.__initial_frame = 0
        self.__actual_animation = self.__walk_l
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_patrolling_right = False
        
        
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
    
    def set_x_animations(self, move_x: int, animation: list, look_r:bool):
        self.__move_x += move_x
        self.__actual_animation = animation
        self.__is_looking_right = look_r

    def collition_plataform(self, plataforms:list[Plataform]):
        for plataform in plataforms:
            if self.__rect.colliderect(plataform.get_rect):
                if self.__rect.bottom >= plataform.get_rect.top:
                    self.__rect.bottom = plataform.get_rect.top
                    self.__plataform_colition = True
                    print(self.__plataform_colition)
                    self.__gravity = 0
            else:
                self.__plataform_colition = False

    def auto_move(self):
        if self.__is_on_ground or self.__plataform_colition:
            if self.__is_patrolling_right:
                look_r = False
                self.set_x_animations(self.__speed_walk, self.__walk_l, look_r)
            else:
                look_r = True
                self.set_x_animations(-self.__speed_walk, self.__walk_r, look_r)

            # Cambia de dirección para que no se pase de la pantalla
            if self.__move_x <= 0 or self.__move_x >= ANCHO_VENTANA - self.__rect.width:
                self.__is_patrolling_right = not self.__is_patrolling_right

    def death(self):
        if self.__collite_top:
            pass

    def applty_gravity(self):
        if (self.__move_y < GROUND_LEVEL) and not self.__plataform_colition:
            self.__move_y += self.__gravity 
            self.__gravity += 1
            self.__actual_animation = self.__fall_r if self.__is_looking_right else self.__fall_l

            if self.__move_y >= GROUND_LEVEL:
                self.__is_on_ground = True
                self.__move_y = GROUND_LEVEL
                self.__gravity = 0
                self.__is_patrolling_right = True
            
    def do_movement(self):
        self.applty_gravity()
        self.auto_move()
        self.__rect.x = self.__move_x
        self.__rect.y = self.__move_y

    def do_animation(self):
        if not self.__is_on_ground:
            self.__actual_img_animation = self.__fall_r if self.__is_looking_right else self.__fall_l
        else:
            self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
            if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
                self.__initial_frame += 1
                if self.__initial_frame >= len(self.__actual_animation):
                    self.__initial_frame = 0
                self.update_time = pg.time.get_ticks()

    def update(self):
        """
        Actualiza el estado del enemigo.
        """
        self.do_movement()
        self.do_animation()

    def draw(self, screen: pg.surface.Surface):
        """
        Dibuja al enemigo en la pantalla.

        Args:
            screen (pg.surface.Surface): Superficie de la pantalla.
        """
        screen.blit(self.__actual_animation[self.__initial_frame], self.__rect)
    
    @staticmethod
    def generate_enemies(num_enemies):
        enemies = []
        for _ in range(num_enemies):
            x = random.randint(50, ANCHO_VENTANA-40)
            y = 0
            speed_walk = random.uniform(1, 5)
            damage = random.randint(1, 3)
            enemy = Enemigo(x, y, 40, 40, speed_walk, damage)
            enemies.append(enemy)
        return enemies