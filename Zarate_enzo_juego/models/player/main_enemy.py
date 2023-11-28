import pygame as pg
import random
from models.platafroma import Plataform
from auxiliar.constantes import GROUND_LEVEL, ANCHO_VENTANA, PUSH, DEBUG, open_config
from models.bullet import Bullet
from models.auxiliar import SurfaceManager as sf

class Enemigo(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y,w,h,damage, speed_walk,frame_rate=100):
        super().__init__()

        self.__config = open_config().get("enemy")

        self.__walk_r = sf.get_surface_from_spritesheet(self.__config["path_walk"], 3, 1,(w,h))
        self.__walk_l = sf.get_surface_from_spritesheet(self.__config["path_walk"], 3, 1,(w,h), flip=True)
        self.__fall_r = sf.get_surface_from_spritesheet(self.__config["path_fall"], 1, 1,(w,h))
        self.__fall_l = sf.get_surface_from_spritesheet(self.__config["path_fall"], 1, 1,(w,h), flip=True)

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
        Devuelve el rectángulo asociado al enemigo.

        DEVUELVE:
        pg.Rect: Rectángulo del enemigo.
        """
        return self.__rect

    @property
    def get_damage(self) -> int:
        """
        Devuelve la cantidad de daño infligido por el enemigo.

        DEVUELVE:
        int: Daño infligido por el enemigo.
        """
        return self.__damage

    @property
    def get_push(self) -> int:
        """
        Devuelve la cantidad de fuerza de empuje del enemigo.

        DEVUELVE:
        int: Fuerza de empuje del enemigo.
        """
        return self.__push
    
    @property
    def get_points(self) -> int:
        """
        Devuelve la cantidad de puntos otorgados al derrotar al enemigo.

        DEVUELVE:
        int: Puntos otorgados al derrotar al enemigo.
        """
        return self.__points
    
    @property
    def get_bullets(self) -> list[Bullet]:
        """
        Devuelve la lista de balas disparadas por el enemigo.

        DEVUELVE:
        list[Bullet]: Lista de balas disparadas por el enemigo.
        """
        return self.__bullet_group

    @property
    def dead(self) -> bool:
        """
        Indica si el enemigo ha sido derrotado.

        DEVUELVE:
        bool: True si el enemigo ha sido derrotado, False de lo contrario.
        """
        return self.__dead
    
    def bullet_shoot(self):
        """
        Realiza el disparo de una bala por parte del enemigo.
        """
        if self.__is_on_ground or self.__plataform_colition:
            if self.__bullet_ready:
                print('Enemigo dispara')
                self.__bullet_group.add(self.create_bullet())
                self.__bullet_ready = False
                self.__bullet_time = pg.time.get_ticks()

    def create_bullet(self):
        """
        Crea una instancia de la clase Bullet, representando una bala disparada por el enemigo.

        DEVUEVE:
        Bullet: Instancia de la clase Bullet.
        """
        return Bullet(self.__rect.centerx, self.__rect.centery, not self.__is_looking_right, True)

    def recharge(self):
        """
        Recarga el tiempo de espera entre disparos del enemigo.
        """
        if not self.__bullet_ready:
            current_time = pg.time.get_ticks()
            if current_time - self.__bullet_time >= self.__bullet_cooldown:
                self.__bullet_ready = True
    
    def check_bullet_collision(self, bullets: pg.sprite.Group):
        """
        Verifica si el enemigo ha colisionado con alguna bala disparada por el jugador.

        RECIBE:
        bullets (pg.sprite.Group): Grupo de balas disparadas por el jugador.
        """
        for bullet in bullets:
            if self.__rect.colliderect(bullet.rect):
                print("le di")
                self.__dead = True
                bullet.kill()
                break

    def set_x_animations(self, move_x: int, animation: list, look_r:bool):
        """
        Establece la animación y dirección del enemigo al moverse horizontalmente.

        RECIBE:
        move_x (int): Desplazamiento horizontal del enemigo.
        animation (list): Lista de imágenes que representan la animación del enemigo.
        look_r (bool): True si el enemigo mira a la derecha, False de lo contrario.
        """
        self.__move_x += move_x
        self.__actual_animation = animation
        self.__is_looking_right = look_r

    def applty_gravity(self):
        """
        Aplica la gravedad al enemigo si no está en el suelo o en una plataforma.
        """
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
        """
        Verifica la colisión del enemigo con las plataformas.

        RECIBE:
        plataforms (list[Plataform]): Lista de plataformas en el juego.
        """
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
        """
        Limita el patrullaje del enemigo dentro de ciertos límites horizontales.

        RECIBE:
        limit_l (int): Límite izquierdo del patrullaje.
        limit_r (int): Límite derecho del patrullaje.
        """
        if self.__rect.x <= limit_l:
            self.__rect.x = limit_l  # Ajusta la posición al límite izquierdo
            self.__is_patrolling_right = True
            
        elif self.__rect.x >= limit_r:
            self.__rect.x = limit_r  # Ajusta la posición al límite derecho
            self.__is_patrolling_right = False
            
    def auto_move(self):
        """
        Realiza el movimiento automático del enemigo en el juego.
        """
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
        """
        Realiza el movimiento del enemigo y verifica colisiones con plataformas.

        RECIBE:
        plataforms (list[Plataform]): Lista de plataformas en el juego.
        """
        self.__rect.x = self.__move_x
        self.__rect.y = self.__move_y
        self.applty_gravity()
        self.collition_plataform(plataforms)
        self.auto_move()

    def do_animation(self):
        """
        Realiza la animación del enemigo.
        """
        if not self.__is_on_ground and not self.__plataform_colition:
            self.__actual_img_animation = self.__fall_r[0] if self.__is_looking_right else self.__fall_l[0]
        else:
            if self.__actual_animation and pg.time.get_ticks() - self.update_time >= self.__frame_rate:
                self.__initial_frame += 1
                if self.__initial_frame >= len(self.__actual_animation):
                    self.__initial_frame = 0
                self.update_time = pg.time.get_ticks()
                self.__actual_img_animation = self.__actual_animation[self.__initial_frame]


    def update(self,plataforms: list[Plataform]):
        """
        Actualiza el estado del enemigo.

        RECIBE:
        plataforms (list[Plataform]): Lista de plataformas en el juego.
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
    def generate_enemies(num_enemies, max_damage, max_speed):
        """
        Genera una lista de enemigos de forma aleatoria.

        RECIBE:
        num_enemies (int): Número de enemigos a generar.

        DEVUELVE:
        list: Lista de objetos Enemigo generados.
        """
        enemies = []

        for _ in range(num_enemies):
            x = random.randint(100, ANCHO_VENTANA-40)
            y = 0
            damage = random.randint(1, max_damage)
            speed = random.uniform(1, max_speed)

            enemy = Enemigo(x, y, 40, 40,damage,speed)
            enemies.append(enemy)

        return enemies