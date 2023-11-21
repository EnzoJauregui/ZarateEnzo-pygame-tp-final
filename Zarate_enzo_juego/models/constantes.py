import json

ANCHO_VENTANA = 900
ALTO_VENTANA = 800
GROUND_LEVEL = 650
HEIGHT_RECT = 10
RECTIFY = 1.2
FPS = 60
DEBUG = True
CONGIG_FILE_PATH = "Pygame\models\config.json"
PLATAFORM_LIMIT = 300
HEIGHT_RECT = 3
LIFE_POINTS = 100

def open_config() -> dict:
    """
    Abre el archivo de configuración en formato JSON y carga su contenido en un diccionario.

    DEVUELVE:
    dict: Diccionario con la configuración cargada desde el archivo.
    """
    with open(CONGIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)
    