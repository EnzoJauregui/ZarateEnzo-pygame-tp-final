import pygame as pg
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS, CANTIDAD
from models.player.main_enemy import Enemigo
from models.platafroma import Plataform
from models.tramps import Tramp
from models.Fruits import Fruit
from models.game import Game

pg.init()

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))


back_img = pg.image.load(r'Zarate_enzo_juego\recursos\fondo.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

# Creación de plataformas
list_plataforms = []
list_plataforms.append(Plataform(350, 580, 150, 30, 3))
list_plataforms.append(Plataform(450, 400, 150, 30, 5))
list_plataforms.append(Plataform(250, 500, 150, 30, 3))
list_plataforms.append(Plataform(650, 380, 150, 30, 5))
list_plataforms.append(Plataform(0, 300, 150, 30, 5))
list_plataforms.append(Plataform(ANCHO_VENTANA - 150, 300, 150, 30, 5))

list_enemies = []
num_enemies_to_generate = CANTIDAD
nuevos_enemigos = Enemigo.generate_enemies(num_enemies_to_generate)
list_enemies.extend(nuevos_enemigos)

list_tramps = []
num_tramps_to_generate = CANTIDAD
nuevas_trampas = Tramp.generate_tramps(num_tramps_to_generate)
list_tramps.extend(nuevas_trampas)

list_fruits = []

num_fruits_to_generate = CANTIDAD
nuevas_frutas = Fruit.generate_fruits(num_fruits_to_generate)
list_fruits.extend(nuevas_frutas)

game = Game(screen, list_plataforms, list_enemies, list_tramps, list_fruits, back_img)

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