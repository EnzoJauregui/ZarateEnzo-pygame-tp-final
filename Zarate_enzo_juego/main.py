import pygame as pg
from auxiliar.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS

from models.platafroma import Plataform
from models.game import Game

pg.init()

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Creación de plataformas
list_plataforms = []
list_plataforms.append(Plataform(350, 580, 150, 30, 3))
list_plataforms.append(Plataform(450, 400, 150, 30, 5))
list_plataforms.append(Plataform(250, 500, 150, 30, 3))
list_plataforms.append(Plataform(650, 380, 150, 30, 5))
list_plataforms.append(Plataform(0, 300, 150, 30, 5))
list_plataforms.append(Plataform(ANCHO_VENTANA - 150, 300, 150, 30, 5))

game = Game(screen, list_plataforms, "stage_uno")
game = Game(screen, list_plataforms, "stage_dos")
game = Game(screen, list_plataforms, "stage_tres")

max_time_seg = 60

# Reloj para controlar el FPS
clock = pg.time.Clock()
# Bucle principal
juego_ejecutandose = True
inicio_tiempo = pg.time.get_ticks()

while juego_ejecutandose:
    # Obtengo el tiempo transcurrido en milisegundos
    tiempo_transcurrido = (pg.time.get_ticks() - inicio_tiempo) // 1000  # Convierte a segundos
    tiempo_restante = max_time_seg - tiempo_transcurrido
    tiempo_restante = 0 if tiempo_restante < 0 else tiempo_restante

    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            juego_ejecutandose = False 

    if tiempo_restante <= 0:
        juego_ejecutandose = False

    game.update()

    #Texto mostrado en pantalla
    font = pg.font.Font(None, 36)
    tiempo_texto = font.render(f'Tiempo: {tiempo_restante} segundos', True, "Black")
    screen.blit(tiempo_texto, (10, 10))
    font = pg.font.Font(None, 36)
    puntos_texto = font.render(f'Puntos: {game.get_player.get_points}', True, "Black")
    screen.blit(puntos_texto, (ANCHO_VENTANA - 200, 10))

    # Actualizar pantalla
    pg.display.update()

    delta_ms = clock.tick(FPS)
pg.quit()