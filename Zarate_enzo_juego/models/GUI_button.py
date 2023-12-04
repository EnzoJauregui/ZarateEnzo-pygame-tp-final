import pygame as pg
from models.GUI_widget import Widget

class Button(Widget):
    def __init__(self,master_surface,x,y,w,h,background_color,border_color, on_click, on_click_param,text, font,font_size,font_color) -> None:
        super().__init__(master_surface,x,y,w,h,background_color,border_color)
        pg.font.init()
        self.on_click = on_click
        self.on_click_param = on_click_param
        self.text = text
        self.font_sys = pg.font.SysFont(font, font_size)
        self.font_color = font_color
    


    def render(self):
        image_text = self.font_sys.render(self.text, True, self.font_color, self.background_color)
        self.slave_surface = pg.Surface((self.w, self.h))
        self.slave_surface.fill(self.background_color)
        pg.draw.rect(self.slave_surface, self.border_color, (0, 0, self.w, self.h))
        self.slave_surface.blit(image_text, (10, 10))

    def update(self, list_events):
        #verifico si hicieron click
        for event in list_events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.slave_rect.collidepoint(event.pos):
                    self.on_click(self.on_click_param) 


        self.render()

    