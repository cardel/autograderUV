"""
Carlos Andres Delgado
Script para calificar examenes
Fecha: 2024-04-13
Versión: 1.0
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from fpdf import FPDF
from modules.informe_docente import generarInformeDocente
from modules.informe_estudiantes import generarInformeEstudiantes
from modules.informe_grupal import generarInformeGrupal
from modules.procesar import procesar



class PDF(FPDF):
    pass  # nothing happens when it is executed.


num_correctas = 15
fecha = '27 de Junio de 2023'
materia = "Fundamentos de análisis y diseño de algoritmos"
examen = "Parcial 2"
resultados_aprendizaje = ('Estructuras de datos', 'Ordenamiento', 'Estrategias algoritmicas')
preg_res_aprendizaje = [[0,1,2,3], [4,5,6, 7, 8, 9], [10,11, 12, 13, 14]]
num_examenes = 3
codificacion_examenes = ["A","B","C","D"]




def todo(data, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje,estudiantes,estudiantes_tipo_examen):
    generarInformeDocente(data, estudiantes)
    generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje)
    generarInformeGrupal(data, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen)


if __name__ == '__main__':
    data = procesar(num_correctas, num_examenes, codificacion_examenes, materia, fecha, examen)
    print("Que desea")
    print("1. Generar todo")
    print("2. Solo informe del docente")
    print("3. Solo informes para estudiantes")
    print("4. Solo informe grupal")
    option = int(input("Ingrese la opción: "))
    
	
    if option == 1:
        todo(data, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje, estudiantes,estudiantes_tipo_examen)
    elif option == 2:
        generarInformeDocente(data, estudiantes)
    elif option == 3:
        generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje)
    elif option == 4:
        generarInformeGrupal(data, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen)
    else:
        print("Opcion no válida")

