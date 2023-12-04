from typing import Any
import pygame as pg
from models.auxiliar import SurfaceManager as sf
from auxiliar.constantes import ANCHO_VENTANA
import random

class Fruit(pg.sprite.Sprite):
    def __init__(self,x, y, w, h, increase_life, increase_points,numb, frame_rate = 60):
        super().__init__()
        self.__actual_animation = sf.get_surface_from_spritesheet(f'./Zarate_enzo_juego/recursos/Fruits/{numb}.png',17, 1,(w,h))
        self.__frame_rate = frame_rate
        self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = x
        self.__rect.y = y
        self.__increase_life = increase_life
        self.increase_points = increase_points

        self.update_time = pg.time.get_ticks()

        self.__sound = pg.mixer.Sound("./Zarate_enzo_juego/recursos/Sounds/coin.wav")
        
    @property
    def get_rect(self):
        """
        Obtiene el rectángulo asociado a la fruta.

        DEVUELVE:
        pg.Rect: Rectángulo de la fruta.
        """
        return self.__rect

    @property
    def get_increase(self):
        """
        Obtiene la cantidad de puntos de vida a incrementar.

        DEVUELVE:
        int: Cantidad de puntos de vida a incrementar.
        """
        return self.__increase_life
    
    def increase_life(self, player):
        """
        Incrementa los puntos de vida y puntos del jugador si hay colisión con la fruta.

        RECIBE:
        player (Jugador): Objeto del jugador.

        DEVUELVE:
        bool: True si hay colisión y se incrementa la vida, False de lo contrario.
        """
        if self.__rect.colliderect(player.get_rect):
            self.__sound.play()
            player.increase_life_points(self.__increase_life)
            player.increase_points(self.increase_points)
            print(f"Puntos de vida incrementados: {player.get_life_points}")
            print(f"Puntos incrementados: {player.get_points}")
            return True
        
    def do_animation(self):
        """
        Realiza la animación de la fruta.
        """
        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            
            self.update_time = pg.time.get_ticks()
        
    
    def update(self,player):
        """
        Actualiza el estado de la fruta.

        Args:
            player (Jugador): Objeto del jugador.
        """
        self.increase_life(player)
        self.do_animation()
        

    def draw(self,screen:pg.Surface):
        """
        Dibuja la fruta en la pantalla.

        RECIBE:
        screen (pg.Surface): Superficie de la pantalla.
        """
        screen.blit(self.__actual_img_animation, self.__rect)
    
    @staticmethod
    def generate_fruits(num_fruits: int, min_life: int, max_life: int, min_points: int, max_points: int, ground_level):
        """
        Genera una lista de frutas de forma aleatoria.

        RECIBE:
        num_fruits (int): Número de frutas a generar.

        DEVUELVE:
        list: Lista de objetos Fruit generados.
        """
        fruits = []
        for _ in range(num_fruits):
            x = random.randint(50, ANCHO_VENTANA - 50)
            y = random.randint(150, ground_level)
            increase_life = random.randint(min_life, max_life)  
            increase_points = random.randint(min_points, max_points)
            numb = random.randint(1, 8) 
            
            fruit = Fruit(x, y, 50, 50, increase_life, increase_points, numb)
            fruits.append(fruit)

        return fruits


