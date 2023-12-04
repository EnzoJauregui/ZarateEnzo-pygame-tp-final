import pygame as pg
from auxiliar.constantes import DEBUG, ANCHO_VENTANA

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, img_path = False):
        super().__init__()
        self.__load_img(img_path)
        self.__rect = self.image.get_rect(center=(x, y))
        self.__direction = direction
        self.__speed = 5
        self.__alive = True
        self.__damage = 2

    @property
    def rect(self):
        """
        Devuelve el rectángulo asociado a la bala.

        DEVUELVE:
        pg.Rect: Rectángulo de la bala.
        """
        return self.__rect
    
    @property
    def get_damage(self) -> int:
        """
        Devuelve la cantidad de daño infligido por la bala.

        DEVUELVE:
        int: Daño infligido por la bala.
        """
        return self.__damage
    
    @property
    def is_alive(self):
        """
        Indica si la bala está activa.

        DEVUELVE:
        bool: True si la bala está activa, False de lo contrario.
        """
        return self.__alive
    
    def __load_img(self, img_path: bool):
        """
        Carga la imagen de la bala.

        RECIBE:
        img_path (bool): Ruta de la imagen de la bala (opcional, predeterminado a False).
        """
        if img_path:
            self.image = pg.image.load('./Zarate_enzo_juego/recursos/bullet/1.png')
        else: 
            self.image = pg.Surface((4, 20))
            self.image.fill('Black')


    def update(self):
        """
        Actualiza la posición de la bala y verifica si ha salido de la pantalla.
        """
        self.__rect.x += self.__speed if self.__direction else -self.__speed

        if 0 >= self.__rect.x <= ANCHO_VENTANA:
            self.kill()

       