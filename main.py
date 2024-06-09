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

num_correctas = 11.5
fecha = '06 de junio de 2024'
materia = "Fundamentos de lenguajes de programación"
examen = "Examen parcial II"
resultados_aprendizaje = ("RA2: Aplica técnicas para representar programas, análisis lexico y semántico",)


codificacion_preguntas = [
    [19, 14, 11, 16, 8, 5, 1, 9, 4, 0, 10, 15, 12, 17, 13],
    [10, 0, 15, 4, 9, 14, 12, 5, 11, 2, 1, 7, 19, 6, 8],
    [3, 5, 10, 2, 12, 13, 18, 0, 4, 11, 1, 7, 14, 15, 6],
    [18, 3, 19, 8, 2, 17, 6, 12, 13, 15, 11, 10, 9, 14, 7],
    [12, 10, 9, 16, 8, 18, 6, 19, 3, 0, 5, 2, 11, 7, 1],
    [19, 11, 15, 8, 6, 5, 4, 1, 3, 14, 10, 2, 7, 9, 17],
    [10, 8, 13, 4, 16, 5, 18, 7, 3, 11, 17, 0, 19, 15, 9],
    [11, 14, 13, 17, 12, 8, 19, 10, 5, 0, 7, 1, 15, 9, 4]
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


num_examenes = 8
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
    

