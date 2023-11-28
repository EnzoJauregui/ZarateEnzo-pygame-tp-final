import json
import sqlite3

ANCHO_VENTANA = 900
ALTO_VENTANA = 800
GROUND_LEVEL = 650
HEIGHT_RECT = 10
RECTIFY = 1.2
FPS = 60
DEBUG = False
CONGIG_FILE_PATH = "./Zarate_enzo_juego/models/config.json"
PLATAFORM_LIMIT = 300
HEIGHT_RECT = 3
LIFE_POINTS = 50
PUSH = 50
CANTIDAD = 2

def open_config() -> dict:
    """
    Abre el archivo de configuración en formato JSON y carga su contenido en un diccionario.

    DEVUELVE:
    dict: Diccionario con la configuración cargada desde el archivo.
    """
    with open(CONGIG_FILE_PATH, 'r', encoding='utf-8') as config:
        contenido = json.load(config)
        return contenido["game"]

def exportar_a_sql(lista):
        # Establecer una conexión con la base de datos "HIGH_SCORE.db" y asignarla a la variable "conexion"
        with sqlite3.connect("HIGH_SCORE.db") as conexion:
            try:
                # Define una consulta SQL para crear la tabla "HIGH_SCORE" con sus columnas
                sentencia = """
                            CREATE TABLE IF NOT EXISTS HIGH_SCORE
                                (
                                    Nombre TEXT,
                                    Puntos REAL
                                )
                            """
                # Intenta ejecutar la consulta para crear la tabla "HIGH_SCORE"
                conexion.execute(sentencia)
                print("Se creó la tabla HIGH_SCORE")

            except sqlite3.OperationalError:
                # Si la tabla ya existe, imprime un mensaje
                print("La tabla HIGH_SCORE ya existe")

            try:
                cursor = conexion.cursor()  # Crea un objeto cursor
                cursor.execute("DELETE FROM HIGH_SCORE;")

                # Lista de datos de Jugadores obtenidos de self.contenido_ranking_estadisticas_sql()
                for jugador, puntos in lista:
                    cursor.execute("INSERT INTO HIGH_SCORE (Nombre, Puntos) VALUES (?, ?)", (jugador, puntos))

                # Confirma la transacción
                conexion.commit()
                print("Se han insertado los datos en la tabla.")

                # Consulta la tabla y muestra los datos ordenados por puntaje descendente
                cursor.execute("SELECT * FROM HIGH_SCORE ORDER BY Puntos DESC")
                print("Datos en la tabla HIGH_SCORE (ordenados por puntaje descendente):")
                for fila in cursor.fetchall():
                    print(fila)

            except sqlite3.Error as e:
                print(f"Error: {e}")