import pygame as pg
from random import randint
from main_player import Jugador
from auxiliar import SurfaceManager as sf

class Enemigo(Jugador):
    def __init__(self, coord_x, coord_y, frame_rate, speed_walk):
        super().__init__(coord_x, coord_y, frame_rate, speed_walk)
        self.__iddle_r = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\iddle\player_idle.png', 5, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\iddle\player_idle.png', 5, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet(r'Pygame\assets\img/player\walk/player_walk.png', 6, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\walk/player_walk.png', 6, 1, flip=True)
        self.__run_r = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\run/player_run.png', 2, 1)
        self.__run_l = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\run/player_run.png', 2, 1, flip=True)
        self.__attack_r = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\jump/player_jump.png', 6, 1)
        self.__attack_l = sf.get_surface_from_spritesheet(r'Pygame\assets\img\player\jump/player_jump.png', 6, 1, flip=True)
    
        
