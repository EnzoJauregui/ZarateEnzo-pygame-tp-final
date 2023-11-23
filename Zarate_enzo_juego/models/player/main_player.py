import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, DEBUG, GROUND_LEVEL, RECTIFY, LIFE_POINTS, HEIGHT_RECT
from models.platafroma import Plataform
from models.player.main_enemy import Enemigo
from models.tramps import Tramp
from models.bullet import Bullet
from models.Fruits import Fruit



class Jugador:
    def __init__(self, coord_x, coord_y,w ,h ,frame_rate = 200, speed_walk = 3, speed_run = 6):
        self.__iddle_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\iddle\0.png', 1, 1,(w,h), flip=True)
        self.__iddle_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\iddle\0.png', 1, 1,(w,h))
        self.__walk_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\walk\0.png', 3, 1,(w,h), flip=True)
        self.__walk_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\walk\0.png', 3, 1,(w,h))
        self.__run_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\run\0.png', 3, 1,(w,h), flip=True)
        self.__run_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\run\0.png', 3, 1,(w,h))
        self.atack_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\atak\0.png', 1, 1,(w,h), flip=True)
        self.atack_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\atak\0.png', 1, 1,(w,h))
        self.__jump_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\jump\0.png', 5, 1,(w*RECTIFY,h*RECTIFY), flip=True)
        self.__jump_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\jump\0.png', 5, 1,(w*RECTIFY,h*RECTIFY))
        self.__die = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\die\0.png', 11, 1,(w,h)) 

        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__is_looking_right = True
        
        self.__gravity = -1
        
        self.__jump = 15
        self.__is_jumping = False
        self.__star_jump = False
     
        self.__frame_rate = frame_rate
        self.update_time = pg.time.get_ticks()
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()

        self._plataform_colition = False
        self._grund_collition_rect = pg.Rect(self.__rect.x, self.__rect.y+self.__rect.h-10, self.__rect.w, 2)
        self.__life_points = LIFE_POINTS
        self.counter = 1000

        self.__bullet_ready = True
        self.__bullet_time = 0
        self.__bullet_group = pg.sprite.Group()
        self.__bullet_cooldown = 500
        self.__points = 0
    
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
    
    def bullet_shoot(self):
        """
        Dispara una bala desde la posición del jugador.
        """
        if self.__bullet_ready:
           
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
                print("me dio")
                
                break

    def reduce_life_points(self, damage: int):
        """
        Reduce los puntos de vida del jugador en función del daño recibido por parametro.

        RECIBE:
        damage (int): Valor del daño a descontar de los puntos de vida.
        """
        self.__life_points -= damage
    
    def increase_points(self, increase):
        """
        Aumenta la puntuación del jugador.

        RECIBE:
        increase (int): Valor a sumar a la puntuación actual.
        """
        self.__points += increase
    
    def increase_life_points(self, increase: int):
        if self.__life_points < LIFE_POINTS:
            self.__life_points += increase
        else:
            self.__life_points = LIFE_POINTS
    
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
            self.__gravity = self.__jump
            self.__is_jumping = True
            self._plataform_colition = False
    
    def applty_gravity(self):
        """
        Aplica la gravedad al movimiento en 'y' del jugador.
        """
        if (self.__is_jumping or self.__move_y < GROUND_LEVEL) and not self._plataform_colition:
            self.__move_y -= self.__gravity
            self.__gravity-= 1
            self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
            self.__is_jumping = True

            if self.__move_y >= GROUND_LEVEL:  
                self.__move_y = GROUND_LEVEL
                
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
                # Reducir puntos de vida
                self.reduce_life_points(enemy.get_damage)
                print("Puntos de vida restantes:", self.__life_points)

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
                self.reduce_life_points(tramp.get_damage)
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
                    self._plataform_colition = True
                    self.__gravity = 0
                    break
            else:
                self._plataform_colition = False

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
           
    def do_animation(self):
        """
        Controla las acciones del jugador según las teclas presionadas.
        """
        if self.__initial_frame >= len(self.__actual_animation) - 1:
            self.__initial_frame = 0

        if not self.__star_jump:
            self.__actual_img_animation = self.__jump_r[0] if self.__is_looking_right else self.__jump_l[0]
        else:
            self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            
        if pg.time.get_ticks() - self.update_time >= self.__frame_rate:
            self.__initial_frame += 1
            self.update_time = pg.time.get_ticks()

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
            self.__bullet_ready = False
            self.bullet_time = pg.time.get_ticks()
            print("shot")

        if lista_teclas_presionadas[pg.K_UP]:
            self.jump()

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
        
