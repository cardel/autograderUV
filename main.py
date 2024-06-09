"""
Carlos Andres Delgado
Script para calificar examenes
Fecha: Junio 9 2024
Versión: 1.5
"""
from fpdf import FPDF
from modules.informe_docente import generarInformeDocente
from modules.informe_estudiantes import generarInformeEstudiantes
from modules.informe_grupal import generarInformeGrupal
from modules.procesar import procesar

class PDF(FPDF):
    pass  # nothing happens when it is executed.

num_correctas = 12
fecha = '05 de junio de 2024'
materia = "Introducción al análisis numérico"
examen = "Examen parcial III"
resultados_aprendizaje = ("RA2: Comprendela naturaleza de la solución numérica de sistemas lineales y no  lineales",)


codificacion_preguntas = [
    [14, 3, 9, 8, 12, 0, 2, 7, 13, 6, 4, 10, 11, 5, 1],
    [5, 6, 10, 1, 4, 14, 13, 0, 8, 12, 11, 3, 7, 9, 2],
    [1, 0, 14, 12, 10, 7, 6, 4, 2, 13, 3, 5, 8, 11, 9],
    [8, 7, 6, 12, 13, 10, 9, 2, 4, 11, 14, 3, 0, 5, 1]
]
resultados_aprendizaje_generales = [[1,2,3,4,5,6,7,9,10,11,12,13,14,15]]

preg_res_aprendizaje = []

for cod in codificacion_preguntas:
    prog_cod = []
    for i in range(len(resultados_aprendizaje_generales)):
        res = []
        for pre in cod:
            if pre in resultados_aprendizaje_generales[i]:
                res.append(pre) 
        prog_cod.append(res)
    preg_res_aprendizaje.append(prog_cod)


num_examenes = 4
codificacion_examenes = ["A", "B", "C", "D", "E", "F", "G", "H"]

def todo(data, respuestas, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje,estudiantes,estudiantes_tipo_examen): 
    generarInformeDocente(data, estudiantes)
    generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, consolidado, codificacion_preguntas, PDF)
    generarInformeGrupal(data, respuestas, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, codificacion_examenes, consolidado, codificacion_preguntas, PDF)

if __name__ == '__main__':
    data, respuestas, respuestas_totales, datos_examen, estudiantes_tipo_examen, estudiantes, consolidado = procesar(num_correctas, num_examenes, codificacion_examenes, materia, fecha, examen, codificacion_preguntas)
    print("Que desea")
    print("1. Generar todo")
    print("2. Solo informe del docente")
    print("3. Solo informes para estudiantes")
    print("4. Solo informe grupal")
    print("5. Buscar estudiante")
    option = int(input("Ingrese la opción: "))
    
	
    if option == 1:
        todo(data, respuestas, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje, estudiantes,estudiantes_tipo_examen)
    elif option == 2:
        generarInformeDocente(data, estudiantes)
    elif option == 3:
        generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, consolidado, codificacion_preguntas, PDF)
    elif option == 4:
        generarInformeGrupal(data, respuestas, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, codificacion_examenes, consolidado, codificacion_preguntas, PDF)
    elif option == 5:
        codigo_estudiante = input("Ingrese el código del estudiante: ")
        print(data[data["codigo"]==codigo_estudiante]["Nombre de archivo"])
    else:
        print("Opcion no válida")
    

