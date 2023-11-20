import pygame as pg
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador
from models.player.main_enemy import Enemigo
from models.platafroma import Plataform

# Inicialización de Pygame
pg.init()

# Creación de la pantalla
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Creación del fondo
back_img = pg.image.load(r'recursos\fondo.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

# Creación del jugador y enemigo
nick = Jugador(0, 0, 30, 30)
enemy = Enemigo(50, 0, 40, 40)

# Creación de plataformas
lista_plataformas = []
lista_plataformas.append(Plataform(350, 580, 50, 30, 3))

# Reloj para controlar el FPS
clock = pg.time.Clock()

# Bucle principal
juego_ejecutandose = True
while juego_ejecutandose:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            juego_ejecutandose = False
    
    # Actualizar jugador y enemigo
    nick.control_keys()
    nick.update(lista_plataformas)

    enemy.update()

    # Dibujar fondo y plataformas
    screen.blit(back_img, back_img.get_rect())
    for plataforma in lista_plataformas:
        
        plataforma.draw(screen)

    # Dibujar jugador y enemigo
    nick.draw(screen)
    enemy.draw(screen)

    # Actualizar pantalla
    pg.display.update()

    # Controlar el FPS
    delta_ms = clock.tick(FPS)

# Cierre de Pygame
pg.quit()
