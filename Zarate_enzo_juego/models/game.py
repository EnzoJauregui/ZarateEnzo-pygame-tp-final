import pygame as pg
from models.player.main_player import Jugador

class Game:
    def __init__(self, screen: pg.Surface, list_plataforms, list_enemies, list_tramps, list_fruits, back_image):

        self.__screen = screen
        self.__player = Jugador(0, 0, 30, 30)
        self.__plataforms = list_plataforms
        self.__emenies = list_enemies
        self.__tramps = list_tramps
        self.__fruits = list_fruits
        self.__back_image = back_image
    
    @property
    def get_player(self):
        """
        Obtiene el jugador del juego.

        DEVUELVE:
        Jugador: Objeto del jugador.
        """
        return self.__player

    def action_enemies(self):
        """
        Realiza las acciones relacionadas con los enemigos en el juego.
        - Verifica colisiones con las balas del jugador.
        - Actualiza y dibuja cada enemigo.
        - Realiza disparos de los enemigos.
        - Verifica colisiones de las balas de los enemigos con el jugador.
        """
        if len(self. __emenies)> 0:
            for enemy in self.__emenies:
                self.__player.check_bullet_collision(enemy.get_bullets)
                enemy.update(self.__plataforms)
                enemy.draw(self.__screen)
                enemy.bullet_shoot()
                enemy.check_bullet_collision(self.__player.get_bullets)

            self.__emenies = [enemy for enemy in self.__emenies if not enemy.dead]
    
    def action_tramps(self):
        """
        Realiza las acciones relacionadas con las trampas en el juego.
        - Dibuja y actualiza cada trampa.
        """
        for tramps in self.__tramps:
            tramps.draw(self.__screen)
            tramps.update()

    def action_fruits(self):
        """
        Realiza las acciones relacionadas con las frutas en el juego.
        - Elimina las frutas que incrementan la vida del jugador.
        - Actualiza y dibuja cada fruta.
        """
        if len(self.__fruits) > 0:
            fruits_to_eliminate = []

            for i in range(len(self.__fruits)):
                if self.__fruits[i].increase_life(self.__player):
                    fruits_to_eliminate.append(i)
                else:
                    self.__fruits[i].update(self.__player)
                    self.__fruits[i].draw(self.__screen)

            # Elimina las frutas marcadas
            for fruit in (fruits_to_eliminate):
                self.__fruits.pop(fruit)
    
    def action_player(self):
        """
        Realiza las acciones relacionadas con el jugador en el juego.
        - Actualiza las balas del jugador.
        - Dibuja las balas del jugador.
        - Controla las teclas del jugador.
        - Actualiza, dibuja y controla el jugador.
        """
        for bullet in self.__player.get_bullets:
            bullet.update()
    
        self.__player.get_bullets.draw(self.__screen)
        self.__player.control_keys()
        self.__player.update(self.__screen, self.__plataforms, self.__emenies, self.__tramps)
        self.__player.draw(self.__screen)

    def refresh_screen(self):
        """
        Refresca la pantalla, dibujando la imagen de fondo y las plataformas.
        """
        self.__screen.blit(self.__back_image, (0, 0))

        for plataform in self.__plataforms:
            plataform.draw(self.__screen)
        
    def update(self):
        """
        Actualiza el estado del juego.
        - Refresca la pantalla.
        - Realiza acciones relacionadas con enemigos, trampas, frutas y el jugador.
        """
        self.refresh_screen()
        self.action_enemies()
        self.action_tramps()
        self.action_fruits()
        self.action_player()



