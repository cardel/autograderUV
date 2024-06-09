"""
Carlos Andres Delgado
Script para calificar examenes
Fecha: Mayo 05 2024
Versión: 1.1
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
materia = "Fundamentos de Programación imperativa"
examen = "Examen parcial II"
resultados_aprendizaje = ("RA1 Propone algoritmos para resolver problemas", "RA2: Utiliza un lenguaje de programación")


codificacion_preguntas = [
    [7, 19, 12, 8, 18, 9, 3, 13, 14, 4, 10, 6, 2, 16, 0],
    [6, 9, 13, 16, 1, 5, 2, 15, 14, 3, 18, 7, 12, 0, 4],
    [15, 7, 9, 11, 3, 1, 10, 12, 13, 2, 17, 14, 4, 5, 18],
    [6, 10, 5, 7, 2, 9, 19, 17, 3, 16, 14, 8, 13, 4, 15]
]
resultados_aprendizaje_generales = [[13,4,0],[1,2,3,5,6,9,10,11,12,14,15,16,17,18,19]]

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
    

