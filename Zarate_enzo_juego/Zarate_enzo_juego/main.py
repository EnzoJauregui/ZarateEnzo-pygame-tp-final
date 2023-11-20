import pygame as pg
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()

back_img = pg.image.load(r'Zarate_enzo_juego\recursos\fondo.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

juego_ejecutandose = True

nick = Jugador(0, 0,30,30, frame_rate=100, speed_walk=3, speed_run=6)


while juego_ejecutandose:
    #print(delta_ms)
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
            print('Estoy CERRANDO el JUEGO')
            juego_ejecutandose = False
    
    nick.control_keys()        

    screen.blit(back_img, back_img.get_rect())
    delta_ms = clock.tick(FPS)
    nick.update()
    nick.draw(screen)
    pg.display.update()

pg.quit()