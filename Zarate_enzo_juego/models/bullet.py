import pygame as pg
from models.constantes import DEBUG


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, direction, speed):
        self.__bullet_image = pg.image.load(r'Zarate_enzo_juego\recursos\bullet\1.png')
        self.__bullet_image = pg.transform.scale(self.__bullet_image,(w, h))
        self.__bullet_collition_image = pg.image.load(r'Zarate_enzo_juego\recursos\bullet\2.png')
        self.__bullet_collition_image = pg.transform.scale(self.__bullet_collition_image,(w, h))
        self.__actual_image = self.__bullet_image
        self.__move_x = x
        self.__move_y = y
        self.__direction = direction
        self.__collide = False

        self.__speed = speed
        self.__rect = self.__actual_image.get_rect()

    def bullet_move(self):
        self.__move_x += self.__speed if self.__direction else -self.__speed
    
    def impact_to(self, person):
        if self.__rect.colliderect(person.get_rect):
            
            self.__actual_image = self.__bullet_collition_image
            del(person)
            self.__collide = True
        else:
            self.__collide = False
        return self.__collide


    
    def do_movement(self):
        self.bullet_move()

    def draw(self, screen):
        if DEBUG:
            pg.draw.rect(screen, "Red", self.__rect)
        
        screen.blit(self.__actual_image, (self.__move_x, self.__move_y))
