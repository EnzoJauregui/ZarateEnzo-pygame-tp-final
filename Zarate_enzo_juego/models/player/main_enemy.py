import pygame as pg
import random
from models.platafroma import Plataform
from models.constantes import GROUND_LEVEL, ANCHO_VENTANA, PUSH, DEBUG
from models.bullet import Bullet
from models.auxiliar import SurfaceManager as sf

class Enemigo(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y,w,h, speed_walk,damage, frame_rate=100):
        super().__init__()

        self.__walk_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\walk.png', 3, 1,(w,h))
        self.__walk_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\walk.png', 3, 1,(w,h), flip=True)
        self.__fall_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\fall.png', 1, 1,(w,h))
        self.__fall_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\enemy\fall.png', 1, 1,(w,h), flip=True)

        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__is_looking_right = True
        self.__is_patrolling_right = False

        self.__gravity = -1
        self.__plataform_colition = False
        self.__is_on_ground = False

        self.__frame_rate = frame_rate
        self.update_time = pg.time.get_ticks()
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_l
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        
        self.__points = 50
        self.__push = PUSH
        self.__damage = damage
        self.__bullet_group = pg.sprite.Group()
        self.__bullet_ready = True
        self.__bullet_time = 0
        self.__bullet_cooldown = 2000  # Ajusta el tiempo de espera entre disparos
        self.__dead = False

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
    
    @property
    def get_points(self) -> int:
        """
        Devuelve el valor del atributo privado 'self.__points'

        DEVUELVE:
        self.__points (int): valor del dicho atributo.
        """
        return self.__points
    
    @property
    def get_bullets(self) -> list[Bullet]:
        return self.__bullet_group

    @property
    def dead(self) -> bool:
        """
        Devuelve el valor del atributo privado 'self.__dead'

        DEVUELVE:
        self.__dead (int): valor del dicho atributo.
        """
        return self.__dead
    
    def bullet_shoot(self):
        if self.__is_on_ground or self.__plataform_colition:
            if self.__bullet_ready:
                print('Enemigo dispara')
                self.__bullet_group.add(self.create_bullet())
                self.__bullet_ready = False
                self.__bullet_time = pg.time.get_ticks()

    def create_bullet(self):
        return Bullet(self.__rect.centerx, self.__rect.centery, not self.__is_looking_right, True)

    def recharge(self):
        if not self.__bullet_ready:
            current_time = pg.time.get_ticks()
            if current_time - self.__bullet_time >= self.__bullet_cooldown:
                self.__bullet_ready = True
    
    def check_bullet_collision(self, bullets: pg.sprite.Group):
        for bullet in bullets:
            if self.__rect.colliderect(bullet.rect):
                print("le di")
                self.__dead = True
                bullet.kill()
                break

    def set_x_animations(self, move_x: int, animation: list, look_r:bool):
        self.__move_x += move_x
        self.__actual_animation = animation
        self.__is_looking_right = look_r

    def applty_gravity(self):
        if (self.__move_y < GROUND_LEVEL) and not self.__plataform_colition:
            self.__move_y -= self.__gravity
            self.__gravity -= 1
            self.__actual_animation = self.__fall_r if self.__is_looking_right else self.__fall_l

            if self.__move_y >= GROUND_LEVEL:
                self.__is_on_ground = True
                self.__move_y = GROUND_LEVEL
                self.__gravity = 0
                self.__is_patrolling_right = True

    def collition_plataform(self, plataforms:list[Plataform]):
        for plataform in plataforms:
            if self.__rect.colliderect(plataform.get_rect):
                if self.__rect.bottom >= plataform.get_rect.top:
                    self.__rect.bottom = plataform.get_rect.top
                    self.__limit_r = plataform.get_rect.x + plataform.get_rect.w
                    self.__limit_l = plataform.get_rect.x
                    self.__plataform_colition = True
                    break
            else:
                self.__plataform_colition = False

    def limit_patrol(self, limit_l: int, limit_r: int):

        if self.__rect.x <= limit_l:
            self.__rect.x = limit_l  # Ajusta la posición al límite izquierdo
            self.__is_patrolling_right = True
            
        elif self.__rect.x >= limit_r:
            self.__rect.x = limit_r  # Ajusta la posición al límite derecho
            self.__is_patrolling_right = False
            
    def auto_move(self):
        if self.__rect.y >= GROUND_LEVEL or self.__plataform_colition:
            if self.__is_patrolling_right:
                look_r = False
                self.set_x_animations(self.__speed_walk, self.__walk_l, look_r)
            else:
                look_r = True
                self.set_x_animations(-self.__speed_walk, self.__walk_r, look_r)

            if self.__plataform_colition:
                self.limit_patrol(self.__limit_l, self.__limit_r - self.__rect.width)
            else:
                self.limit_patrol(0, ANCHO_VENTANA - self.__rect.width)
            
    def do_movement(self,plataforms: list[Plataform]):
        self.__rect.x = self.__move_x
        self.__rect.y = self.__move_y
        self.applty_gravity()
        self.collition_plataform(plataforms)
        self.auto_move()

    def do_animation(self):
        if not self.__is_on_ground and not self.__plataform_colition:
            self.__actual_img_animation = self.__fall_r if self.__is_looking_right else self.__fall_l
        else:
            if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
                self.__initial_frame += 1
                if self.__initial_frame >= len(self.__actual_animation):
                    self.__initial_frame = 0
                self.update_time = pg.time.get_ticks()
            self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

    def update(self,plataforms: list[Plataform]):
        """
        Actualiza el estado del enemigo.
        """
        self.do_movement(plataforms)
        self.do_animation()
        self.__bullet_group.update()
        self.recharge()

    def draw(self, screen: pg.surface.Surface):
        """
        Dibuja al enemigo en la pantalla.

        Args:
            screen (pg.surface.Surface): Superficie de la pantalla.
        """
        screen.blit(self.__actual_animation[self.__initial_frame], self.__rect)
        self.__bullet_group.draw(screen)

        if DEBUG:
            pg.draw.rect(screen, "Blue", self.__rect)

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