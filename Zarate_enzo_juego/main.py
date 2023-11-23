import pygame as pg
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador
from models.player.main_enemy import Enemigo
from models.platafroma import Plataform
from models.tramps import Tramp
from models.Fruits import Fruit
# Inicialización de Pygame
pg.init()

# Creación de la pantalla
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Creación del fondo
back_img = pg.image.load(r'Zarate_enzo_juego\recursos\fondo.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

# Creación del jugador y enemigo
nick = Jugador(0, 0, 30, 30)

# Creación de plataformas
lista_plataformas = []
lista_plataformas.append(Plataform(350, 580, 150, 30, 3))
lista_plataformas.append(Plataform(450, 500, 150, 30, 5))
lista_plataformas.append(Plataform(250, 380, 150, 30, 3))
lista_plataformas.append(Plataform(650, 500, 150, 30, 5))

lista_enemigos = []
num_enemies_to_generate = 3 
nuevos_enemigos = Enemigo.generate_enemies(num_enemies_to_generate)
lista_enemigos.extend(nuevos_enemigos)

lista_trampas = []
num_tramps_to_generate = 3
nuevas_trampas = Tramp.generate_tramps(num_tramps_to_generate)
lista_trampas.extend(nuevas_trampas)

lista_fruits = []

num_fruits_to_generate = 5 
nuevas_frutas = Fruit.generate_fruits(num_fruits_to_generate)
lista_fruits.extend(nuevas_frutas)

max_time = 180

# Reloj para controlar el FPS
clock = pg.time.Clock()
# Bucle principal
juego_ejecutandose = True
inicio_tiempo = pg.time.get_ticks()

while juego_ejecutandose:
    # Obtengo el tiempo transcurrido en milisegundos
    tiempo_transcurrido = (pg.time.get_ticks() - inicio_tiempo) // 1000  # Lo convierto a segundos

    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            juego_ejecutandose = False 

    if tiempo_transcurrido >= max_time:
        juego_ejecutandose = False

    # Dibujar fondo y plataformas
    screen.blit(back_img, back_img.get_rect())
    
    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    if len(lista_enemigos) > 0: 
        for enemigo in lista_enemigos:
            enemigo.update(lista_plataformas)
            enemigo.draw(screen) 

    for trampa in lista_trampas:
        trampa.update()
        trampa.draw(screen) 

    if len(lista_fruits) > 0:
        frutas_a_eliminar = []

        for i in range(len(lista_fruits)):
            if lista_fruits[i].increase_life(nick):
                frutas_a_eliminar.append(i)
            else:
                lista_fruits[i].update(nick)
                lista_fruits[i].draw(screen)

        # Elimina las frutas marcadas
        for index in reversed(frutas_a_eliminar):
            lista_fruits.pop(index)

    for bala in nick.get_bullets:
        bala.update()
    
    nick.get_bullets.draw(screen)

    nick.control_keys()
    nick.update(screen, lista_plataformas, lista_enemigos, lista_trampas)
    nick.draw(screen)
    font = pg.font.Font(None, 36)
    tiempo_texto = font.render(f'Tiempo: {tiempo_transcurrido} segundos', True, "Black")
    screen.blit(tiempo_texto, (10, 10))
    # Actualizar pantalla
    pg.display.update()

    # Controlar el FPS
    delta_ms = clock.tick(FPS)

# Cierre de Pygame
pg.quit()
