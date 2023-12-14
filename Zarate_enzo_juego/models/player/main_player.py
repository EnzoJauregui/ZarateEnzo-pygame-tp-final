import pygame as pg
from models.auxiliar import SurfaceManager as sf
from auxiliar.constantes import ANCHO_VENTANA, DEBUG, RECTIFY, LIFE_POINTS, HEIGHT_RECT, open_config
from models.platafroma import Plataform
from models.player.main_enemy import Enemigo
from models.tramps import Tramp
from models.bullet import Bullet

class Jugador(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y,w ,h,ground_level ,frame_rate = 60, speed_walk = 3, speed_run = 6):

        self.__configs = open_config()["player"]

        self.__iddle_r = sf.get_surface_from_spritesheet(self.__configs.get("path_iddle", "not found"), 1, 1,(w,h), flip=True)
        self.__iddle_l = sf.get_surface_from_spritesheet(self.__configs.get("path_iddle", "not found"), 1, 1,(w,h))
        self.__walk_r = sf.get_surface_from_spritesheet(self.__configs.get("path_walk", "not found"), 3, 1,(w,h), flip=True)
        self.__walk_l = sf.get_surface_from_spritesheet(self.__configs.get("path_walk", "not found"), 3, 1,(w,h))
        self.__run_r = sf.get_surface_from_spritesheet(self.__configs.get("path_run", "not found"), 3, 1,(w,h), flip=True)
        self.__run_l = sf.get_surface_from_spritesheet(self.__configs.get("path_run", "not found"), 3, 1,(w,h))
        self.__shoot_r = sf.get_surface_from_spritesheet(self.__configs.get("path_shoot", "not found"), 1, 1,(w,h), flip=True)
        self.__shoot_l = sf.get_surface_from_spritesheet(self.__configs.get("path_shoot", "not found"), 1, 1,(w,h))
        self.__jump_r = sf.get_surface_from_spritesheet(self.__configs.get("path_jump", "not found"), 5, 1,(w*RECTIFY,h*RECTIFY), flip=True)
        self.__jump_l = sf.get_surface_from_spritesheet(self.__configs.get("path_jump", "not found"), 5, 1,(w*RECTIFY,h*RECTIFY))
        self.__die = sf.get_surface_from_spritesheet(self.__configs.get("path_die", "not found"), 11, 1,(w,h)) 

        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__is_looking_right = True
        
        self.__gravity = 1
        self.__jump = 15
        self.__is_jumping = False
        self.__star_jump = False
        self.__ground_level = ground_level
        self.__plataform_colition = False
     
        self.__frame_rate = frame_rate
        self.update_time = pg.time.get_ticks()
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()

        self.__life_points = LIFE_POINTS
        self.__lives = 2
        self.counter = 1000

        self.__is_shooting = False
        self.__bullet_ready = True
        self.__bullet_time = 0
        self.__bullet_group = pg.sprite.Group()
        self.__bullet_cooldown = 500
        self.__points = 0

        self.__is_dead = False

        self.__jump_sound = pg.mixer.Sound("./Zarate_enzo_juego/recursos/Sounds/jump.wav")
        self.__impact_shoot = pg.mixer.Sound("./Zarate_enzo_juego/recursos/Sounds/collition.wav")
        self.__shoot = pg.mixer.Sound("./Zarate_enzo_juego/recursos/Sounds/bullet.wav")
        self.__hit = pg.mixer.Sound("./Zarate_enzo_juego/recursos/Sounds/hit.wav")

        
    
    @property
    def get_rect(self) -> pg.Rect:
        """
        Devuelve el rectángulo de colision del jugador.

        DEVUELVE
        self.__rect (pg.Rect): Rectangulo de colisión del jugador.
        """
        return self.__rect
    
    @property
    def get_life_points(self) -> int:
        """
        Devuelve los puntos de vida actuales del jugador.

        DEVUELVE:
        self.__life_points (int): Puntos de vida actuales del jugador.
        """
        return self.__life_points
    
    @property
    def get_points(self) -> int:
        """
        Devuelve la puntuación actual del jugador.

        DEVUELVE:
        self.__points (int): Puntuación actual del jugador.
        """
        return self.__points

    @property
    def get_bullets(self) -> pg.sprite.Group:
        """
        Devuelve el grupo de balas del jugador.

        DEVUELVE:
        self.__bullet_group (pg.sprite.Group): Grupo de balas del jugador.
        """
        return self.__bullet_group
    
    @property
    def get_is_dead(self) -> bool:
        """
        Devuelve el jugador esta muerto o no.

        DEVUELVE:
        self.__is_dead (bool): indica si esta muerto o no.
        """
        return self.__is_dead
    
    @property
    def get_lives(self) -> int:
        """
        Devuelve las vidas del jugador.

        DEVUELVE:
        self.__lives (int): vidas actuales del jugador.
        """
        return self.__lives
    
    def set_ground_level(self, ground_level):
        """
        Establece el nivel del suelo para el jugador.

        RECIBE:
        ground_level: Altura del nivel del suelo.
        """
        self.__ground_level = ground_level

    def set_coord_x(self, coord_x):
        """
        Establece la coordenada X del jugador.

        RECIBE:
        coord_x: Coordenada X del jugador.
        """
        self.__move_x = coord_x
    
    def set_coord_y(self, coord_y):
        """
        Establece la coordenada Y del jugador.

        RECIBE:
        coord_y: Coordenada Y del jugador.
        """
        self.__move_y = coord_y


    def bullet_shoot(self):
        """
        Realiza un disparo de bala.
        
        - Si la bala esta lista para disparar, reproduce el sonido de disparo, crea una nueva bala y la añade al grupo de balas.
        - Marca el jugador como disparando y actualiza el tiempo del último disparo.
        """
        if self.__bullet_ready:
            self.__shoot.play()
            self.__is_shooting = True
            self.__bullet_group.add(self.create_bullet())
            self.__bullet_ready = False
            self.__bullet_time = pg.time.get_ticks()
            
    
    def create_bullet(self) -> Bullet:
        """
        Crea una instancia de la clase Bullet en la posición del jugador.

        DEVUELVE:
        Bullet: Objeto de la clase Bullet.
        """
        return Bullet(self.__rect.centerx, self.__rect.centery, self.__is_looking_right, True)

    def recharge(self):
        """
        Recarga el tiempo de espera para poder disparar otra bala.
        """
        if not self.__bullet_ready:
            current_time = pg.time.get_ticks()
            if current_time - self.__bullet_time >= self.__bullet_cooldown:
                self.__bullet_ready = True

    def check_bullet_collision(self, bullets: pg.sprite.Group):
        """
        Verifica las colisiones entre las balas del jugador y un grupo de balas enemigas.

        RECIBE:
        bullets (pg.sprite.Group): Grupo de balas enemigas.
        """
        for bullet in bullets:
            if self.__rect.colliderect(bullet.rect):
                self.__impact_shoot.play()
                self.reduce_life_points(bullet.get_damage)
                print("me dio")
                bullet.kill()
                break

    def reduce_life_points(self, damage: int):
        """
        Reduce los puntos de vida del jugador en función del daño recibido por parametro.

        RECIBE:
        damage (int): Valor del daño a descontar de los puntos de vida.
        """
        if self.__life_points > 0 and self.__is_dead == False:
            self.__life_points -= damage
    
    def increase_points(self, increase):
        """
        Aumenta la puntuación del jugador.

        RECIBE:
        increase (int): Valor a sumar a la puntuación actual.
        """
        self.__points += increase
    
    def increase_life_points(self, increase: int):
        """
        Incrementa los puntos de vida del jugador.

        RECIBE:
        increase (int): Cantidad de puntos de vida a incrementar.

        ACCIÓN:
        - Si el jugador tiene vidas restantes y los puntos de vida actuales son menores que el maximo,
          incrementa los puntos de vida.
        - Ajusta los puntos de vida a su máximo si se exceden.
        """
        if self.__lives>0:
            if self.__life_points < LIFE_POINTS:
                self.__life_points += increase
                if self.__life_points > LIFE_POINTS:
                    self.__life_points = LIFE_POINTS
            else:
                self.__life_points = LIFE_POINTS
        

    def reduce_lives(self):
        """
        Reduce las vidas del jugador.

        ACCIÓN:
        - Si el jugador tiene vidas restantes y los puntos de vida son igual o inferiores a cero,
          restablece los puntos de vida al máximo y reduce una vida.
        - Si no quedan vidas, establece los puntos de vida a cero y marca al jugador como muerto.
        """
        if self.__lives > 0:    
            if self.__life_points <= 0:
                self.__life_points = LIFE_POINTS
                self.__lives-=1
                print(self.__lives)
        else:
            self.__life_points = 0
            self.__lives = 0
            self.__is_dead = True
            
    
    def move_back(self, amount):
        """
        Mueve al jugador hacia atrás en la dirección opuesta al enemigo o trampa después de una colisión.

        RECIBE:
        amount (int): Valor de desplazamiento hacia atrás.
        """
        self.__move_x -= amount

    def __set_x_animations_preset(self, move_x: int, animation_list: list[pg.surface.Surface], look_r: bool):
        """
        Configura las animaciones y el movimiento para la dirección izquierda/derecha.

        RECIBE:
        move_x (int): Velocidad de desplazamiento horizontal o en x.
        animation_list (list[pg.surface.Surface]): Lista de superficies de animación.
        look_r (bool): Indica si el jugador está mirando hacia la derecha.
        """
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        self.__move_x += move_x
       
    def walk(self, boolean, direction: str = 'Right'):
        """
        Inicia el movimiento de caminar en la dirección especificada y actualiza la animación.

        RECIBE:
        boolean (bool): Indica si el jugador está en un estado de caminar o saltar.
        direction (str): Dirección del movimiento ('Right' o 'Left').
        """
        match direction:
            case 'Right':
                look_right = True
                animation = self.__walk_r if boolean else self.__jump_r
                self.__set_x_animations_preset(self.__speed_walk, animation, look_r=look_right)
            case 'Left':
                look_right = False
                animation = self.__walk_l if boolean else self.__jump_l
                self.__set_x_animations_preset(-self.__speed_walk, animation, look_r=look_right)
       
    def run(self, direction: str = 'Right'):
        """
        Inicia el movimiento de correr en la dirección especificada Y actualiza la animacion.

        RECIBE:
        direction (str): Dirección del movimiento ('Right' o 'Left').
        """
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    
    def stay(self):
        """
        Actualiza la el atributo 'self.__actual_animation' para que el jugador permanezca en reposo.
        """
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
        self.__initial_frame = 0
           
    def jump(self):
        """
        Inicia el salto del jugador.
        """
        if not self.__is_jumping: 
            self.__jump_sound.play()
            self.__gravity = self.__jump
            self.__is_jumping = True
            self.__plataform_colition = False
  
    def applty_gravity(self):
        """
        Aplica la gravedad al movimiento en 'y' del jugador.
        """
        if (self.__is_jumping or self.__move_y < self.__ground_level) and not self.__plataform_colition:
            self.__move_y -= self.__gravity
            self.__gravity-= 1
            self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
            self.__is_jumping = True

            if self.__move_y >= self.__ground_level:  
                self.__move_y = self.__ground_level
                
                self.__star_jump = True
                self.__is_jumping = False
                self.__gravity = 0
        
    def collition_enemy(self, enemies: list[Enemigo]):
        """
        Maneja la colisión con los enemigos, reduce los puntos de vida y realiza un retroceso.

        RECIBE:
        enemies (list[Enemigo]): Lista de objetos Enemigo.
        """
        for enemy in enemies:
            if self.__rect.colliderect(enemy.get_rect):
                print("¡Colision con enemigo!")
                self.__hit.play()
                # Reducir puntos de vida
                self.reduce_life_points(enemy.get_damage)
                print("Puntos de vida restantes:", self.__life_points)
                self.__actual_animation = self.__die
                # Empujar al jugador hacia atrás al recibir daño
                self.move_back(enemy.get_push if self.__rect.x < enemy.get_rect.x else - enemy.get_push) 
                self.__actual_animation = self.__die
                break
    
    def collition_tramp(self, tramps: list[Tramp]):
        """
        Maneja la colisión con las trampas, reduce los puntos de vida y realiza un retroceso.

        RECIBE:
        tramps (list[Tramp]): Lista de objetos Tramp.
        """
        for tramp in tramps:
            if self.__rect.colliderect(tramp.get_rect):
                print("Colision con la trampa. Aplicando danio.")
                self.__hit.play()
                self.reduce_life_points(tramp.get_damage)
                self.__actual_animation = self.__die
                self.move_back(tramp.get_push if self.__rect.x < tramp.get_rect.x else - tramp.get_push)
                print("Puntos de vida restantes:", self.get_life_points)
                          
    def collition_plataform(self, plataforms:list[Plataform]):
        """
        Maneja la colisión con las plataformas y ajusta la posición del jugador.

        RECIBE:
        plataforms (list[Plataform]): Lista de objetos Plataform.
        """
        for plataform in plataforms:
            if self.__rect.colliderect(plataform.get_rect):
                if self.__rect.bottom >= plataform.get_rect.top:
                    self.__rect.bottom = plataform.get_rect.top
                    self.__is_jumping = False
                    self.__plataform_colition = True
                    self.__gravity = 0
                    break
            else:
                self.__plataform_colition = False

    def __set_borders_limits(self):
        """
        Establece los límites de los bordes para el movimiento del jugador.
        """
        if self.__rect.right >= ANCHO_VENTANA:
            self.__move_x = ANCHO_VENTANA - self.__rect.width

        elif self.__rect.left <= 0:
            self.__move_x = 0
                  
    def collitions(self, plataforms: list[Plataform], enemies: list[Enemigo], tramps:list[Tramp]):
        """
        Maneja todas las colisiones (plataformas, enemigos, trampas) del jugador.

        RECIBE:
        plataforms (list[Plataform]): Lista de objetos Plataform.
        enemies (list[Enemigo]): Lista de objetos Enemigo.
        tramps (list[Tramp]): Lista de objetos Tramp.
        """
        self.collition_plataform(plataforms)
        self.collition_enemy(enemies)
        self.collition_tramp(tramps)  


    def control_keys(self):
        """
        Controla las acciones del jugador según las teclas presionadas.
        """
        lista_teclas_presionadas = pg.key.get_pressed()
        
        if lista_teclas_presionadas[pg.K_RIGHT]:
            if lista_teclas_presionadas[pg.K_LSHIFT]:
                self.run('Right')

            elif lista_teclas_presionadas[pg.K_UP]:
                self.jump()
                self.walk(False)
            else:
                self.walk(True)
            
        elif lista_teclas_presionadas[pg.K_LEFT]:
            if lista_teclas_presionadas[pg.K_LSHIFT]:
                self.run('Left')

            elif lista_teclas_presionadas[pg.K_UP]:
                self.jump()
                self.walk(False, 'Left')
            else:
                self.walk(True, 'Left')
        else:
            self.stay()
        
        if lista_teclas_presionadas[pg.K_x] and self.__bullet_ready:
            self.bullet_shoot()
            
        elif self.__is_shooting:
            self.__is_shooting = False
            self.stay()

        if lista_teclas_presionadas[pg.K_UP]:
            self.jump()

    def do_movement(self, plataforms: list[Plataform], enemies: list[Enemigo], tramps:list[Tramp]):
        """
        Maneja el movimiento del jugador.

        RECIBE:
        plataforms (list[Plataform]): Lista de objetos Plataform.
        enemies (list[Enemigo]): Lista de objetos Enemigo.
        tramps (list[Tramp]): Lista de objetos Tramp.
        """
        self.__rect.x =+ self.__move_x
        self.__rect.y =+ self.__move_y
        self.__set_borders_limits()
        self.applty_gravity()
        self.collitions(plataforms, enemies, tramps)
        self.reduce_lives()

    def do_animation(self):
        """
        Controla las acciones del jugador según las teclas presionadas.
        """
        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

        if self.__is_shooting:
            self.__actual_animation = self.__shoot_r if self.__is_looking_right else self.__shoot_l
        elif not self.__star_jump and not self.__plataform_colition:
            self.__actual_img_animation = self.__jump_r[0] if self.__is_looking_right else self.__jump_l[0]
        else:
            self.__actual_animation = self.__actual_animation
            self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            self.update_time = pg.time.get_ticks()

    def update(self,screen: pg.surface.Surface, plataformas: list[Plataform], enemies: list[Enemigo], tramps:list[Tramp]):
        """
        Actualiza el estado del jugador (movimiento y animación).

        RECIBE:
        screen (pg.surface.Surface): Superficie de la pantalla.
        plataforms (list[Plataform]): Lista de objetos Plataform.
        enemies (list[Enemigo]): Lista de objetos Enemigo.
        tramps (list[Tramp]): Lista de objetos Tramp.
        """
        self.recharge()
        self.do_movement(plataformas, enemies, tramps)
        self.do_animation()
        self.__bullet_group.draw(screen)
        self.__bullet_group.update()
    
    def draw(self, screen: pg.surface.Surface):
        """
        Dibuja al jugador en la pantalla y la barra de vida.

        RECIBE:
        screen (pg.surface.Surface): Superficie de la pantalla.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            rect_bottom  = pg.Rect(self.__rect.left, self.__rect.bottom, self.__rect.width, HEIGHT_RECT)
            rect_top = pg.Rect(self.__rect.left, self.__rect.top, self.__rect.width, HEIGHT_RECT)
            pg.draw.rect(screen, "Black", rect_bottom)
            pg.draw.rect(screen, "Black", rect_top)
        
        #health bar
        pg.draw.rect(screen, "Red", (self.__rect.x-8, self.__rect.y - 20, LIFE_POINTS, 10))
        pg.draw.rect(screen, "Green", (self.__rect.x-8, self.__rect.y - 20, self.__life_points, 10))
        screen.blit(self.__actual_img_animation, self.__rect)
        
