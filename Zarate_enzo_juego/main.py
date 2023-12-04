import pygame as pg
from auxiliar.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS, exportar_a_sql
from models.text import Text
from models.game import Game
from models.GUI_form_menu import FormMenu

#name_player = input("Ingrese su nombre: ")

pg.init()

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

#form_menu = FormMenu(master_surface=screen,x=100,y=100,w=500,h=500,background_color="Red",border_color="Green",active=True)

# Creación de plataformas

game = Game(screen)

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

    list_events = pg.event.get()

    for event in list_events:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            start_game = False 

    delta_ms = clock.tick(FPS)
    # if form_menu.active:
    #     form_menu.update(list_events)
    #     form_menu.draw()
    game.update(delta_ms)

    if remaining_time <= 0:
        text.game_over()
    else:
        game.read_keys()

    text.show_points(game.get_player.get_points)
    text.show_lives(game.get_player.get_lives)
    text.show_time(remaining_time)
    

    # Actualizar pantalla
    pg.display.update()


pg.quit()

# players_score.append((name_player, game.get_player.get_points))

# exportar_a_sql(players_score)