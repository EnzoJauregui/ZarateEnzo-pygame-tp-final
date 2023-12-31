import pygame as pg
from auxiliar.constantes import open_config, ANCHO_VENTANA, ALTO_VENTANA
from models.player.main_player import Jugador
from models.platafroma import Plataform
from models.player.main_enemy import Enemigo
from models.tramps import Tramp
from models.Fruits import Fruit

class Game:
    def __init__(self, screen: pg.Surface):
        self.__configs = open_config()
        self.__stage = 1
        
        self.__screen = screen
        self.__player = Jugador(0, 0, 30, 30, 650)
        self.load_stage_config()
        self.__game_active = False

        self.__win = False

    @property
    def get_game_active(self) -> bool:
        """
        Obtiene el estado del juego.

        DEVUELVE:
        bool: True si el juego está activo, False de lo contrario.
        """
        return self.__game_active
    
    @property
    def get_win(self) -> bool:
        """
        Obtiene el estado de victoria del jugador.

        DEVUELVE:
        bool: True si el jugador ha ganado, False de lo contrario.
        """
        return self.__win
        
    @property
    def get_player(self):
        """
        Obtiene el jugador del juego.

        DEVUELVE:
        Jugador: Objeto del jugador.
        """
        return self.__player
    
    def load_stage_config(self):
        """
        Carga la configuración del stage actual del juego desde el archivo de configuración.
        - Carga la imagen de fondo.
        - Establece la posición inicial del jugador.
        - Crea instancias de plataformas, enemigos, trampas y frutas según la configuración del stage.
        - Reproduce el sonido de la etapa.
        """

        pg.mixer.stop()

        stage = self.__configs[f'stage_{self.__stage}']
        self.__back_image = pg.image.load(stage["background"])
        self.__back_image = pg.transform.scale(self.__back_image, (ANCHO_VENTANA, ALTO_VENTANA))
        self.get_player.set_ground_level(stage["ground_level"])
        self.get_player.set_coord_x(self.__configs["player"]["coord_x"])
        self.get_player.set_coord_y(self.__configs["player"]["coord_y"])
        
        self.__plataforms = [Plataform(
                            platform["coord_x"],
                            platform["coord_y"],
                            platform["width"],
                            platform["height"],
                            platform["numb"]
                            ) for platform in stage["platforms"]]

        self.__emenies = Enemigo.generate_enemies(stage["max_enemies"], 
                                                  stage["max_enemy_damage"], 
                                                  stage["max_enemy_speed"],
                                                  stage["ground_level"],
                                                  stage["enemy"])

        self.__tramps = Tramp.generate_tramps(stage["max_tramps"], 
                                              stage["max_tramps_speed"], 
                                              stage["max_tramps_damage"],
                                              stage["ground_level"])
        
        self.__fruits = Fruit.generate_fruits(stage["max_fruits"],
                                              stage["min_life"],
                                              stage["max_life"],
                                              stage["min_points"],
                                              stage["max_points"],
                                              stage["ground_level"])
        
        # self.__sound_stage = pg.mixer.Sound(stage["sound"])
        # self.__sound_stage.play(-1)
    
    def next_stage(self):
        """
        Avanza al siguiente stage del juego.
        - Incrementa el número del stage (self.__stage).
        - Carga la configuración del stage siempre que self.__stage no supere 3.
        - De lo contrario, marca la victoria del jugador.
        """
        self.__stage+=1

        if self.__stage <= 3:
            self.load_stage_config()
        else:
            self.__win = True
    

    def action_enemies(self, delta_ms):
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
                enemy.update(self.__plataforms, delta_ms)
                enemy.draw(self.__screen)
                enemy.bullet_shoot()
                enemy.check_bullet_collision(self.__player.get_bullets)

            self.__emenies = [enemy for enemy in self.__emenies if not enemy.dead]
        else:
            self.next_stage()
    
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
        - Actualiza, dibuja y controla el jugador.
        """
        for bullet in self.__player.get_bullets:
            bullet.update()
    
        self.__player.get_bullets.draw(self.__screen)
        self.__player.update(self.__screen, self.__plataforms, self.__emenies, self.__tramps)
        self.__player.draw(self.__screen)

    def read_keys(self):
        """
        Controla las teclas del jugador.
        """
        self.__player.control_keys()

    def refresh_screen(self):
        """
        Refresca la pantalla, dibujando la imagen de fondo y las plataformas.
        """
        self.__screen.blit(self.__back_image, (0, 0))

        for platform in self.__plataforms:
            platform.draw(self.__screen)
        
    def update(self, delta_ms):
        """
        Actualiza el estado del juego.
        - Refresca la pantalla.
        - Realiza acciones relacionadas con enemigos, trampas, frutas y el jugador.
        """
        self.refresh_screen()
        self.action_enemies(delta_ms)
        self.action_tramps()
        self.action_fruits()
        self.action_player()
