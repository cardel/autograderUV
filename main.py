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
num_preguntas = 28
fecha = "01 de Abril de 2025"
materia = "Infraestructuras paralelas y distribuidas"
examen = "Primer exámen"
resultados_aprendizaje = (
    "RA1: Desarrolla programas paralelos en ambientes donde no se comparte memoria",
)


codificacion_preguntas = np.array(
[
    [6, 2, 19, 1, 13, 5, 12, 23, 7, 8, 9, 21, 25, 28, 26],
    [23, 25, 24, 27, 20, 1, 22, 4, 12, 2, 21, 11, 6, 19, 5],
    [13, 20, 9, 14, 19, 6, 27, 22, 24, 23, 16, 17, 12, 4, 15],
    [11, 9, 17, 22, 8, 27, 24, 20, 7, 2, 5, 4, 18, 23, 26]
]
)

codificacion_preguntas = (codificacion_preguntas - 1).tolist()

resultados_aprendizaje_generales = [[i for i in range(0, 28)]]

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
