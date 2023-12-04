import pygame as pg
from auxiliar.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS, exportar_a_sql
from models.text import Text
from models.platafroma import Plataform
from models.game import Game

class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.start_game = False
        self.font = pg.font.Font(None, 36)
        self.input_rect = pg.Rect(ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2 - 20, 200, 40)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.active = False
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

    def handle_events(self, event):
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            pg.quit()
            quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.start_game = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_surface = self.font.render(self.text, True, self.color)
                self.text_rect.w = max(200, self.text_surface.get_width() + 10)

    def run(self):
        while not self.start_game:
            for event in pg.event.get():
                self.handle_events(event)

            self.screen.fill((30, 30, 30))
            width = max(200, self.text_surface.get_width()+10)
            self.input_rect.w = width
            self.screen.blit(self.text_surface, (self.input_rect.x+5, self.input_rect.y+5))
            pg.draw.rect(self.screen, self.color, self.input_rect, 2)
            pg.display.flip()
            self.clock.tick(FPS)

        name_player = self.text
        pg.quit()
        return name_player