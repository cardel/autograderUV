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
num_correctas = 13
num_preguntas = 28
fecha = "Jueves, 12 de Noviembre de 2024"
materia = "Infraestructuras paralelas y distribuidas"
examen = "Primer exámen"
resultados_aprendizaje = (
    "RA1: Desarrolla programas paralelos en ambientes donde no se comparte memoria",
)


codificacion_preguntas = np.array(
    [
        [5, 16, 12, 28, 3, 24, 11, 4, 17, 9, 22, 14, 7, 1, 19],
        [10, 6, 15, 23, 4, 18, 26, 1, 12, 27, 3, 20, 8, 13, 5],
        [2, 14, 25, 9, 7, 28, 16, 22, 11, 4, 5, 21, 3, 10, 17],
        [13, 8, 26, 2, 23, 19, 1, 15, 27, 18, 12, 9, 6, 5, 21],
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
