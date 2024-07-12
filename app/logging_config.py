import logging
import os

def setup_logger():
    '''
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith("funciones_aux.py")]:
            os.chdir(dirpath)
    '''
    logger = logging.getLogger('music_app_logger')
    logger.setLevel(logging.DEBUG)

    # Crear un manejador de archivo con encoding UTF-8
    fh = logging.FileHandler('muscic_app.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Crear un manejador de consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Definir el formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Agregar los manejadores al logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Configurar el logger
logger = setup_logger()