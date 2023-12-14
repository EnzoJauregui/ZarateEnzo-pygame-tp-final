import pygame as pg
from auxiliar.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.text import Text
from models.game import Game

pg.init()
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

game = Game(screen)
text = Text(screen)

clock = pg.time.Clock()

players_score = []

max_time_sec = 120
start_game = True
start_time = pg.time.get_ticks()

while start_game:
    
    elapsed_time = (pg.time.get_ticks() - start_time) // 1000  
    remaining_time = max_time_sec - elapsed_time
    remaining_time = 0 if remaining_time < 0 else remaining_time

    list_events = pg.event.get()

    for event in list_events:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            start_game = False 

    delta_ms = clock.tick(FPS)
    game.update(delta_ms)

    if remaining_time <= 0 or game.get_player.get_is_dead:
        text.game_over()
    else:
        game.read_keys()

    text.update(remaining_time,game.get_player.get_points,game.get_player.get_lives)
    
    pg.display.update()
pg.quit()
