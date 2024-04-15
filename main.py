"""
Carlos Andres Delgado
Script para calificar examenes
Fecha: 2024-04-13
Versión: 1.0
"""
from fpdf import FPDF
from modules.informe_docente import generarInformeDocente
from modules.informe_estudiantes import generarInformeEstudiantes
from modules.informe_grupal import generarInformeGrupal
from modules.procesar import procesar

class PDF(FPDF):
    pass  # nothing happens when it is executed.


num_correctas = 15
fecha = '20 de Marzo de 2023'
materia = "Introducción análisis numérico"
examen = "Parcial 1"
resultados_aprendizaje = ('RA1: Conceptos Redes Neuronales', 'RA2: Solución sistemas Redes')
preg_res_aprendizaje = [
        [[0,2,4,6,7,12],[1,3,5,8,9,10,11,13,14]],
        [[11,2,7,10,6,4],[0,1,3,5,8,9,10,12,13,14]],
        [[11,7,2,4,3,12], [0,1,5,6,8,9,10,13,14]],
        [[0],[0]],
    ]
num_examenes = 3
codificacion_examenes = ["A", "B", "C", "D"]

def todo(data, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje,estudiantes,estudiantes_tipo_examen): 
    generarInformeDocente(data, estudiantes)
    generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, PDF)
    generarInformeGrupal(data, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, num_examenes, codificacion_examenes, PDF)

if __name__ == '__main__':
    data, respuestas_totales, datos_examen, estudiantes_tipo_examen, estudiantes = procesar(num_correctas, num_examenes, codificacion_examenes, materia, fecha, examen)
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
        generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, PDF)
    elif option == 4:
        generarInformeGrupal(data, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, num_examenes, codificacion_examenes, PDF)
    else:
        print("Opcion no válida")
    

