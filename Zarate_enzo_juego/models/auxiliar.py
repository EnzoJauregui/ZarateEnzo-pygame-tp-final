import pygame as pg
import sqlite3

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
    
    @staticmethod
    def exportar_a_sql(lista):
        """
        
        """
        # Establece una conexión con la base de datos "HIGH SCORE.db" y la asigna a la variable "conexion"
        with sqlite3.connect("HIGH SCORE.db") as conexion:
            try:
                # Define una consulta SQL para crear la tabla "HIGH SCORE" con sus columnas
                sentencia = """
                            CREATE TABLE HIGH SCORE
                                (
                                    Nombre text
                                    Puntos real
                                )
                            """
                # Intenta ejecutar la consulta para crear la tabla "HIGH SCORE"
                conexion.execute(sentencia)
                print("Se creó la tabla HIGH SCORE")

            except sqlite3.OperationalError:
                # Si la tabla ya existe, imprime un mensaje
                print("La tabla posiciones ya existe")
            try:
                cursor = conexion.cursor()  # Crea un objeto cursor
                cursor.execute("DELETE FROM HIGH SCORE;")
                # Lista de datos de Jugadores obtenidos de self.contenido_ranking_estadisticas_sql()
                lista = []
                for player in lista:
                    
                    cursor.execute("INSERT INTO HIGH SCORE (Nombre, Puntos) VALUES (?, ?)", (player,))

                # Confirma la transacción
                conexion.commit()
                print("Se han insertado los datos en la tabla.")
            except:
                print("Error")

            # Consulta la tabla y muestra los datos
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM HIGH SCORE")
            #Se le puede agregar una condicion para que te devuelve algo en especifico EJ:ranking puntos mayor a 5,
            #agregandole WHERE Puntos>5. y te printea eso

            print("Datos en la tabla HIGH SCORE:")
            for fila in cursor.fetchall():
                print(fila)
