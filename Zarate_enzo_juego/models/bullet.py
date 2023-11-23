import pygame as pg
from models.constantes import DEBUG, ANCHO_VENTANA
from models.player.main_enemy import Enemigo


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, img_path = False):
        super().__init__()
        self.__load_img(img_path)
        
        self.__rect = self.image.get_rect(center=(x, y))
        self.__direction = direction
        self.__speed = 2
        self.__alive = True
        self.__damage = 2

    @property
    def rect(self):
        return self.__rect
    
    @property
    def is_alive(self):
        return self.__alive
    
    def __load_img(self, img_path: bool):
        if img_path:
            self.image = pg.image.load(r'Zarate_enzo_juego\recursos\bullet\1.png')
        else: 
            self.image = pg.Surface((4, 20))
            self.image.fill('Black')

    def handle_collision(self, player, enemies: Enemigo):
        # Verificar colisión con el jugador
        if self.__rect.colliderect(player.get_rect):
            # Realizar acciones cuando hay colisión con el jugador
            player.reduce_life_points(self.__damage)
            self.__alive = False

        # Verificar colisión con los enemigos
        for enemy in enemies:
            if self.__rect.colliderect(enemy.get_rect):
                # Realizar acciones cuando hay colisión con un enemigo
                enemy.kill()
                self.__alive = False
                break

    def update(self):
        self.__rect.x += self.__speed if self.__direction else -self.__speed

        if 0 >= self.__rect.x <= ANCHO_VENTANA:
            self.kill()
