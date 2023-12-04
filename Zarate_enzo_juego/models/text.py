import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA

class Text:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.font_game_over = pg.font.Font(None, 74)

    def show_time(self, remaining_time):
        """
        Muestra el tiempo restante en la pantalla.

        RECIBE:
        - tiempo_restante: El tiempo restante en segundos que se mostrará en la pantalla.
        """
        time_text = self.font.render(f'Tiempo: {remaining_time} segundos', True, "Black")
        self.screen.blit(time_text, (10, 10))

    def show_points(self, points):
        """
        Muestra la cantidad de puntos en la pantalla.

        RECIBE:
        - puntos: La cantidad de puntos que se mostrará en la pantalla.
        """
        points_text = self.font.render(f'Puntos: {points}', True, "Black")
        self.screen.blit(points_text, (ANCHO_VENTANA - 200, 10))

    def show_lives(self, lives):
        """
        Muestra la cantidad de vidas en la pantalla.

        RECIBE:
        - lives: La cantidad de vidas que se mostrará en la pantalla.
        """
        lives_text = self.font.render(f'Vidas: {lives}', True, "Black")
        self.screen.blit(lives_text, (ANCHO_VENTANA - 200, 50))

    def game_over(self):
        
        game_over_text = self.font_game_over.render("Game Over", True, "Red")
        self.screen.blit(game_over_text, (ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2))

