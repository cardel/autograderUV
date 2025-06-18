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
from modules.leer_configuracion import leer_configuracion
import numpy as np


class PDF(FPDF):
    pass  # nothing happens when it is executed.


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
    conf, resultados_aprendizaje, codificacion_preguntas, ra_generales = leer_configuracion('config.txt')
    codificacion_preguntas = (codificacion_preguntas - 1).tolist()

    preg_res_aprendizaje = []

    num_examenes = conf['num_examenes']
    num_correctas = conf['num_correctas']
    num_preguntas = conf['num_preguntas']
    fecha = conf['fecha']
    materia = conf['materia']
    examen = conf['examen']

    for cod in codificacion_preguntas:
        prog_cod = []
        for i in range(len(ra_generales)):
            res = []
            for pre in cod:
                if pre in ra_generales[i]:
                    res.append(pre)
            prog_cod.append(res)
        preg_res_aprendizaje.append(prog_cod)
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
        print(data[data["codigo"] == codigo_estudiante]["File name"])
    else:
        print("Opcion no válida")
