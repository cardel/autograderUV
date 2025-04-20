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
import numpy as np


class PDF(FPDF):
    pass  # nothing happens when it is executed.


num_examenes = 4
num_correctas = 14
num_preguntas = 32
fecha = "03 de Abril de 2025"
materia = "Fundamentos de compilación e interpretación de lenguajes de programación"
examen = "Primer exámen"
resultados_aprendizaje = (
    "RA1: Utiliza gramáticas independientes del contexto,Analizadores léxicos y sintácticos",
    "RA2: Aplica técnicas de Representación de programas y análisis semántico"
)


codificacion_preguntas = np.array(
 [
    [18, 7, 13, 20, 8, 15, 6, 4, 1, 14, 25, 23, 32, 26, 28],
    [6, 2, 5, 13, 9, 3, 12, 1, 8, 4, 29, 24, 27, 31, 23],
    [5, 13, 17, 4, 20, 1, 14, 9, 12, 10, 23, 28, 31, 26, 27],
    [2, 16, 1, 17, 10, 4, 8, 20, 15, 3, 28, 23, 29, 24, 32]
]
)

codificacion_preguntas = (codificacion_preguntas - 1).tolist()

resultados_aprendizaje_generales = [[i for i in range(0, 23)],[i+23 for i in range(0, 10)]]

# Fin de variables iniciales del programa
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


codificacion_examenes = ["A", "B", "C", "D", "E", "F", "G", "H"]


def todo(
    data,
    respuestas,
    respuestas_totales,
    datos_examen,
    resultados_aprendizaje,
    preg_res_aprendizaje,
    estudiantes,
    estudiantes_tipo_examen,
):
    generarInformeDocente(num_preguntas, data, estudiantes)
    generarInformeEstudiantes(
        num_preguntas,
        data,
        respuestas_totales,
        resultados_aprendizaje,
        preg_res_aprendizaje,
        codificacion_examenes,
        num_correctas,
        consolidado,
        codificacion_preguntas,
        PDF,
    )
    generarInformeGrupal(
        num_preguntas,
        data,
        respuestas,
        respuestas_totales,
        datos_examen,
        resultados_aprendizaje,
        preg_res_aprendizaje,
        estudiantes_tipo_examen,
        codificacion_examenes,
        consolidado,
        codificacion_preguntas,
        PDF,
    )


if __name__ == "__main__":
    (
        data,
        respuestas,
        respuestas_totales,
        datos_examen,
        estudiantes_tipo_examen,
        estudiantes,
        consolidado,
    ) = procesar(
        num_correctas,
        num_examenes,
        codificacion_examenes,
        materia,
        fecha,
        examen,
        codificacion_preguntas,
    )
    print("Que desea")
    print("1. Generar todo")
    print("2. Solo informe del docente")
    print("3. Solo informes para estudiantes")
    print("4. Solo informe grupal")
    print("5. Buscar estudiante")
    option = int(input("Ingrese la opción: "))

    if option == 1:
        todo(
            data,
            respuestas,
            respuestas_totales,
            datos_examen,
            resultados_aprendizaje,
            preg_res_aprendizaje,
            estudiantes,
            estudiantes_tipo_examen,
        )
    elif option == 2:
        generarInformeDocente(num_preguntas, data, estudiantes)
    elif option == 3:
        generarInformeEstudiantes(
            num_preguntas,
            data,
            respuestas_totales,
            resultados_aprendizaje,
            preg_res_aprendizaje,
            codificacion_examenes,
            num_correctas,
            consolidado,
            codificacion_preguntas,
            PDF,
        )
    elif option == 4:
        generarInformeGrupal(
            num_preguntas,
            data,
            respuestas,
            respuestas_totales,
            datos_examen,
            resultados_aprendizaje,
            preg_res_aprendizaje,
            estudiantes_tipo_examen,
            codificacion_examenes,
            consolidado,
            codificacion_preguntas,
            PDF,
        )
    elif option == 5:
        codigo_estudiante = input("Ingrese el código del estudiante: ")
        print(data[data["codigo"] == codigo_estudiante]["Nombre de archivo"])
    else:
        print("Opcion no válida")
