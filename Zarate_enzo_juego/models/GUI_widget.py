import pygame as pg

#clase generica
class Widget:
    def __init__(self,master_surface,x,y,w,h,background_color,border_color) -> None:
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self.border_color = border_color
        


    def render(self):
        pass

    def update(self):
        pass

    def draw(self):
        self.master_surface.blit(self.slave_surface, self.slave_rect)