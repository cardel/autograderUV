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

num_correctas = 14
fecha = '22 de mayo de 2024'
materia = "Introducción al análisis numérico"
examen = "Parcial 2"
resultados_aprendizaje = ('RA2: Comprende naturaleza redes neuronales','RA6: Selecciona una red neuronal, usando los parametros apropiados ')

codificacion_preguntas = [
    [14,5,0,7,11,4,12,13,9,10,3,2,1,6,8],
    [7,9,11,12,4,10,14,13,8,6,2,0,5,3,1], 
    [13,8,3,12,1,10,11,4,9,2,6,7,5,14,15], 
    [11,10,6,12,7,1,13,4,5,14,9,0,8,3,2]
]
resultados_aprendizaje_generales = [[6,9,13],[0,1,2,3,4,5,7,8,10,11,12,14]]

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
    

