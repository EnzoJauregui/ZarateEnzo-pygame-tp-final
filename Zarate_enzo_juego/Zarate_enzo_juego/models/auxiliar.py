import pygame as pg

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, tamanio:tuple, step=1, flip: bool = False) -> list[pg.surface.Surface]:
        """
        Carga una hoja de sprites desde un archivo de imagen y la divide en una lista de superficies individuales.

        RECIBE:
        img_path (str): La ruta del archivo de imagen que contiene la hoja de sprites.
        cols (int): El número de columnas en la hoja de sprites.
        rows (int): El número de filas en la hoja de sprites.
        step (int, opcional): El paso utilizado para seleccionar las columnas en la hoja de sprites.
        flip (bool, opcional): True si se deben voltear horizontalmente las superficies.

        DEVUELVE:
        sprites_list  list[pg.surface.Surface]: Una lista de objetos Surface que representan cada sprite individual de la hoja.
        """
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width() / cols)
        frame_height = int(surface_img.get_height() / rows)

        for row in range(rows):
            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(x_axis, y_axis, frame_width, frame_height)
                frame_surface = pg.transform.scale(frame_surface, tamanio)

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                    frame_surface = pg.transform.scale(frame_surface, tamanio)
                sprites_list.append(frame_surface)
        return sprites_list
