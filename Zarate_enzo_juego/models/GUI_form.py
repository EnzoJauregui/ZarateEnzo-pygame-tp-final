import pygame as pg


class Form():
    def __init__(self, master_surface, x, y, w, h, background_color="Black", border_color="Red", active=False) -> None:
        self.maste_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_color = background_color
        self. border_color = border_color


        self.slave_surface = pg.Surface((w,h))
        self.slave_rect = self.slave_surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active

        if self.background_color != None:
            self.slave_surface.fill(self.background_color)

        

    def render(self):
        pass

    def update(self,list_events):
        pass