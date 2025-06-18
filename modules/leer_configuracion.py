from configparser import ConfigParser
import numpy as np

def leer_configuracion(archivo):
    config = ConfigParser()
    config.read(archivo, encoding='utf-8')

    # Leer sección [Config]
    conf = {
        'num_examenes': config.getint('Config', 'num_examenes'),
        'num_correctas': config.getint('Config', 'num_correctas'),
        'num_preguntas': config.getint('Config', 'num_preguntas'),
        'fecha': config.get('Config', 'fecha'),
        'materia': config.get('Config', 'materia'),
        'examen': config.get('Config', 'examen')
    }

    # Leer sección [Resultados de Aprendizaje]
    resultados_aprendizaje = [
        config.get('Resultados de Aprendizaje', 'ra1'),
        config.get('Resultados de Aprendizaje', 'ra2')
    ]

    # Leer sección [Codificación de Preguntas]
    preguntas_raw = config.get('Codificación de Preguntas', 'preguntas').strip().splitlines()
    codificacion_preguntas = np.array([
        [int(num) for num in line.strip().split(',') if num]
        for line in preguntas_raw if line.strip()
    ])

    # Leer sección [Resultados de Aprendizaje Generales]
    ra_generales = [
        [int(num) for num in line.strip().split(',') if num]
        for line in config.get('Resultados de Aprendizaje Generales', 'generales').strip().splitlines()
        if line.strip()
    ]

    return conf, resultados_aprendizaje, codificacion_preguntas, ra_generales
