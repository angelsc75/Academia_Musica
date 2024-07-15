import logging
#from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('music_app')
    logger.setLevel(logging.DEBUG)

    # Crear un manejador de archivo con encoding UTF-8
    fh = logging.FileHandler('music_app.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Crear un manejador de consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Definir el formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Agregar los manejadores al logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger