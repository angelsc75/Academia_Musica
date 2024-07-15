import logging

"""
Configura y devuelve un logger para la aplicación EscuelaMusical.

Este logger registra mensajes en un archivo y en la consola con diferentes niveles de severidad y formatos.

Returns:
    logger (logging.Logger): El logger configurado.
"""

def setup_logger():
    # Crear un logger con el nombre 'music_app'
    logger = logging.getLogger('music_app')
    # Configurar el nivel de severidad del logger a DEBUG
    logger.setLevel(logging.DEBUG)

    # Crear un manejador de archivo que registra mensajes en 'music_app.log' con codificación UTF-8
    fh = logging.FileHandler('music_app.log', encoding='utf-8')
    # Configurar el nivel de severidad del manejador de archivo a DEBUG
    fh.setLevel(logging.DEBUG)
    
    # Crear un manejador de consola que imprime mensajes de nivel ERROR y superior
    ch = logging.StreamHandler()
    # Configurar el nivel de severidad del manejador de consola a ERROR
    ch.setLevel(logging.ERROR)
    
    # Definir el formato de los mensajes del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Asignar el formato definido al manejador de archivo
    fh.setFormatter(formatter)
    
    # Agregar los manejadores (archivo y consola) al logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Devolver el logger configurado
    return logger