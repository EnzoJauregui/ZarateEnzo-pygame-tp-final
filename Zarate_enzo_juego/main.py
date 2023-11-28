import pygame as pg
from auxiliar.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS, exportar_a_sql
from models.text import Text
from models.platafroma import Plataform
from models.game import Game

name_player = input("Ingrese su nombre: ")

pg.init()

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Creación de plataformas
list_plataforms = []
list_plataforms.append(Plataform(350, 580, 150, 30, 5))
list_plataforms.append(Plataform(450, 400, 150, 30, 5))
list_plataforms.append(Plataform(250, 500, 150, 30, 5))
list_plataforms.append(Plataform(650, 380, 150, 30, 5))
list_plataforms.append(Plataform(0, 300, 150, 30, 5))
list_plataforms.append(Plataform(ANCHO_VENTANA - 150, 300, 150, 30, 5))

game = Game(screen, list_plataforms)

max_time_sec = 60

text = Text(screen)

# Reloj para controlar el FPS
clock = pg.time.Clock()

players_score = []

# Bucle principal
start_game = True

start_time = pg.time.get_ticks()

while start_game:
    # Obtengo el tiempo transcurrido en milisegundos
    elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # Convert to seconds
    remaining_time = max_time_sec - elapsed_time
    remaining_time = 0 if remaining_time < 0 else remaining_time

    lista_eventos = pg.event.get()

    for event in lista_eventos:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            start_game = False 

    game.update()

    if remaining_time <= 0:
        text.game_over()
    else:
        game.read_keys()

    text.show_points(game.get_player.get_points)
    text.show_time(remaining_time)

    # Actualizar pantalla
    pg.display.update()

    delta_ms = clock.tick(FPS)

pg.quit()

players_score.append((name_player, game.get_player.get_points))

exportar_a_sql(players_score)