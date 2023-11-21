import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA, DEBUG, GROUND_LEVEL, RECTIFY, LIFE_POINTS, HEIGHT_RECT
from models.platafroma import Plataform
from models.player.main_enemy import Enemigo
from models.tramps import Tramp



class Jugador:
    def __init__(self, coord_x, coord_y,w,h:tuple, frame_rate = 60, speed_walk = 3, speed_run = 6):
        self.__iddle_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\iddle\0.png', 1, 1,(w,h), flip=True)
        self.__iddle_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\iddle\0.png', 1, 1,(w,h))
        self.__walk_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\walk\0.png', 3, 1,(w,h), flip=True)
        self.__walk_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\walk\0.png', 3, 1,(w,h))
        self.__run_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\run\0.png', 3, 1,(w,h), flip=True)
        self.__run_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\run\0.png', 3, 1,(w,h))
        self.atack_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\atak\0.png', 3, 1,(w,h), flip=True)
        self.atack_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\atak\0.png', 3, 1,(w,h))
        self.__jump_r = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\jump\0.png', 5, 1,(w*RECTIFY,h*RECTIFY), flip=True)
        self.__jump_l = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\jump\0.png', 5, 1,(w*RECTIFY,h*RECTIFY))
        self.__die = sf.get_surface_from_spritesheet(r'Zarate_enzo_juego\recursos\player\nick\die\0.png', 11, 1,(w,h)) 

        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__is_looking_right = True
        self.__gravity_jump = 1
        self.__gravity = -self.__gravity_jump
        
        self.__jump = 15
        self.__is_jumping = False
        self.__star_jump = False
        self.falling = False
        self.__is_death = False
        self.empuje = 50
     
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
    
    @property
    def get_rect(self):
        """
        Devuelve el valor del atributo privado 'self.__rect'
        
        DEVUELVE:
        self.__rect (int): valor del dicho atributo.
        """
        return self.__rect
    
    @property
    def get_life_points(self):
        """
        Devuelve el valor del atributo privado 'self.__life_points'
        
        DEVUELVE:
        self.__life_points (int): valor del dicho atributo.
        """
        return self.__life_points

    def reduce_life_points(self, damage: int):
        """
        Reduce los puntos de vida.

        RECIBE:
        damage (int): valor que se descontaran a los puntos de vida
        """
        self.__life_points -= damage
    
    def move_back(self,amount):
        self.__move_x - amount

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
    
    def collition_enemy(self, enemies: list[Enemigo]):
        for enemy in enemies:
            if self.__rect.colliderect(enemy.get_rect):
                print("¡Colisión con enemigo!")
                # Reducir puntos de vida
                self.reduce_life_points(enemy.get_damage)
                print("Puntos de vida restantes:", self.__life_points)

                # Empujar al jugador hacia atrás al recibir daño
                self.__move_x += -self.empuje if self.__is_looking_right else self.empuje
                self.__actual_animation = self.__die
                self.__is_death = True
                self.counter -= 1
                break
    
    def collition_tramp(self, trampas: list[Tramp]):
        for trampa in trampas:
            if self.get_rect.colliderect(trampa.get_rect):
                print("Colisión con la trampa. Aplicando daño.")
                self.reduce_life_points(trampa.get_damage)
                self.move_back(trampa.get_empuje)
                print(self.get_life_points)
                break

    def collition_plataform(self, plataforms:list[Plataform]):
        for plataform in plataforms:
            if self.__rect.colliderect(plataform.get_rect_ground_colition):
                if self.__rect.bottom >= plataform.get_rect_ground_colition.top:
                    self.__rect.bottom = plataform.get_rect_ground_colition.top
                    self.__is_jumping = False
                    self._plataform_colition = True
                    self.__gravity = 0

                elif self.__rect.colliderect(plataform.get_rect_top_colition):
                    if self.__rect.top >= plataform.get_rect_top_colition.bottom:
                        self.__rect.top = plataform.get_rect_top_colition.bottom
                        print("hola")
                        self._plataform_colition = False
                        print(self._grund_collition_rect)
                break
                #   self.falling = False
                # elif self.__rect.top >= plataform.get_rect.bottom:
                #     print("hola")
                #     self.falling = True
            else:
                self._plataform_colition = False
            

    def applty_gravity(self):
        """
        Aplica la gravedad al movimiento en 'y' del jugador.
        """
        if (self.__is_jumping or self.__move_y < GROUND_LEVEL) and not self._plataform_colition:
            self.__move_y -= self.__gravity
            self.__gravity-=self.__gravity_jump
            self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
            self.__is_jumping = True

            if self.__move_y >= GROUND_LEVEL:  
                self.__move_y = GROUND_LEVEL
                
                self.__star_jump = True
                self.__is_jumping = False
                self.__gravity = 0
                #self.falling = False

        # if self.falling:
        #     self.__move_y += 5
        #     self.__gravity = 0
        #     self.__jump = 0
       
    def __set_borders_limits(self):
        """
        Establece los límites de los bordes para el movimiento del jugador.
        """
        if self.__rect.right >= ANCHO_VENTANA:
            self.__move_x = ANCHO_VENTANA - self.__rect.width

        elif self.__rect.left <= 0:
            self.__move_x = 0
                

    def do_movement(self, plataforms: list[Plataform], enemies: list[Enemigo]):
        """
        Maneja el movimiento del jugador.
        """
        self.__rect.x =+ self.__move_x
        self.__rect.y =+ self.__move_y
        self.__set_borders_limits()
        self.applty_gravity()
        self.collition_plataform(plataforms)
        self.collition_enemy(enemies)
        self.collition_tramp
       
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

        if lista_teclas_presionadas[pg.K_UP]:
            self.jump()

    def update(self, plataformas: list[Plataform], enemies: list[Enemigo]):
        """
        Actualiza el estado del jugador (movimiento y animación).
        """
        self.do_movement(plataformas, enemies)
        self.do_animation()
    
    def draw(self, screen: pg.surface.Surface):
        """
        Dibuja al jugador en la pantalla.

        RECIBE:
        screen (pg.surface.Surface): Superficie de la pantalla.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            rect_bottom  = pg.Rect(self.__rect.left, self.__rect.bottom, self.__rect.width, HEIGHT_RECT)
            rect_top = pg.Rect(self.__rect.left, self.__rect.top, self.__rect.width, HEIGHT_RECT)
            pg.draw.rect(screen, "Black", rect_bottom)
            pg.draw.rect(screen, "Black", rect_top)
        
        screen.blit(self.__actual_img_animation, self.__rect)
        