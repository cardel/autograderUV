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

num_correctas = 13
fecha = '17 de abril de 2024'
materia = "Fundamentos de Programación imperativa"
examen = "Parcial 1"
resultados_aprendizaje = ('RA1: Propone algoritmos para solucionar problemas', 'RA2: Utiliza un lenguaje para implementar algoritmos')

codificacion_preguntas = [
    [5,12,7,2,9,3,16,15,14,13,19,6,10,11,1],
    [1,8,12,7,17,19,13,17,2,14,4,10,3,15,0], 
    [13,4,15,6,3,2,17,9,18,10,16,19,14,9,7], 
    [10,8,9,14,11,7,3,2,6,12,5,15,17,0,13]
]
resultados_aprendizaje_generales = [[0,1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18,19]]

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
    

