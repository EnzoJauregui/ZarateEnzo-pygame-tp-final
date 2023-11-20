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
back_img = pg.image.load(r'Zarate_enzo_juego\recursos\fondo.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

# Creación del jugador y enemigo
nick = Jugador(0, 0, 30, 30)

# Creación de plataformas
lista_plataformas = []
lista_plataformas.append(Plataform(350, 580, 100, 30, 3))
lista_plataformas.append(Plataform(450, 500, 100, 30, 5))
lista_plataformas.append(Plataform(250, 380, 100, 30, 3))
lista_plataformas.append(Plataform(650, 500, 100, 30, 5))
lista_enemigos = []
lista_enemigos.append(Enemigo(100, 0, 40, 40, 2,4, 4, 2))
lista_enemigos.append(Enemigo(350, 0, 40, 40,2, 3, 4,2))
lista_enemigos.append(Enemigo(500, 0, 40, 40,2,1, 6,2))


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

    
    # Dibujar fondo y plataformas
    screen.blit(back_img, back_img.get_rect())
    
    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    for enemigo in lista_enemigos:
        enemigo.update()
        enemigo.draw(screen)   

    nick.control_keys()
    nick.update(lista_plataformas)
    nick.draw(screen)
    # Actualizar pantalla
    pg.display.update()

    # Controlar el FPS
    delta_ms = clock.tick(FPS)

# Cierre de Pygame
pg.quit()
