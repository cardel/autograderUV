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
fecha = '11 de abril de 2024'
materia = "Fundamentos de lenguajes de programación"
examen = "Parcial 1"
resultados_aprendizaje = ('RA1: Uso de gramáticas para analizadores léxicos y sintácticos', 'RA2: Aplicar técnicas para representación de programas', 'RA3: Comprende compilación e interpretación')
preg_res_aprendizaje = [
        [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]],
        [[11,2,7,10,6,4],[0,1,3],[0,1,3,5,8,9,10,12,13,14]],
        [[11,7,2,4,3,12],[0,1,3],[0,1,5,6,8,9,10,13,14]],
        [[0],[0],[1]],
    ]

codificacion_preguntas = [
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14], 
    [0,2,1,3,4,5,6,7,8,9,10,11,12,13,14], 
    [0,3,2,1,4,5,6,7,8,9,10,11,12,13,14], 
    [0,4,2,3,1,5,6,7,8,9,10,11,12,13,14], 
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
]

num_examenes = 1
codificacion_examenes = ["A", "B", "C", "D", "E", "F", "G", "H"]

def todo(data, respuestas, respuestas_totales, datos_examen,resultados_aprendizaje, preg_res_aprendizaje,estudiantes,estudiantes_tipo_examen): 
    generarInformeDocente(data, estudiantes)
    generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, consolidado, PDF)
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
        generarInformeEstudiantes(data, respuestas_totales, resultados_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, consolidado, PDF)
    elif option == 4:
        generarInformeGrupal(data, respuestas, respuestas_totales, datos_examen, resultados_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, codificacion_examenes, consolidado, codificacion_preguntas, PDF)
    elif option == 5:
        codigo_estudiante = input("Ingrese el código del estudiante: ")
        print(data[data["codigo"]==codigo_estudiante]["Nombre de archivo"])
    else:
        print("Opcion no válida")
    

