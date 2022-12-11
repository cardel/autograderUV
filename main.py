import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from fpdf import FPDF


class PDF(FPDF):
    pass  # nothing happens when it is executed.


num_correctas = 13.5


def crear_codigo(value):
    if value == "A":
        return "0"
    elif value == "B":
        return "1"
    elif value == "C":
        return "2"
    elif value == "D":
        return "3"
    elif value == "E":
        return "4"
    elif value == "F":
        return "5"
    elif value == "G":
        return "6"
    elif value == "H":
        return "7"
    elif value == "I":
        return "8"
    elif value == "J":
        return "9"
    else:
        return -1;

def procesar():
    data = pd.read_csv("data/resultados.csv")

    C0 = data["cod.C0"].apply(crear_codigo)
    C1 = data["cod.C1"].apply(crear_codigo)
    C2 = data["cod.C2"].apply(crear_codigo)
    C3 = data["cod.C3"].apply(crear_codigo)
    C4 = data["cod.C4"].apply(crear_codigo)
    C5 = data["cod.C5"].apply(crear_codigo)
    C6 = data["cod.C6"].apply(crear_codigo)

    codigo = pd.DataFrame([C0,C1,C2,C3,C4,C5,C6]).transpose()
    codigo["codigo"] = codigo.apply("".join, axis=1)
    data["codigo"] = codigo["codigo"];

    estudiantes = pd.read_csv("data/listadoClase.csv")

    dataEstudiante = []
    for cod in data["codigo"].values:
        codEstudiante = int("20" + cod)
        nombre = estudiantes[estudiantes["codigo"] == codEstudiante]["nombre"].values.tolist()
        correo = estudiantes[estudiantes["codigo"] == codEstudiante]["correo"].values.tolist()
        if len(nombre) > 0:
            dataEstudiante.append([nombre[0],correo[0]])
        else:
            print("Estudiante no encontrado")
            print(data[data["codigo"] == cod])
            print("Causa 1) El estudiante se equivocó al escribir el código")
            print("Causa 2) Hubo un problema al escanear")
            print("Corrige este problema antes de continuar")
            exit(0)

    dataEstudiante = np.array(dataEstudiante)
    data[["nombre","correo"]] = dataEstudiante
    datos_examen = {"nombre": "Fundamentos de análisis y diseño de algoritmos", "fecha": "10 de Diciembre de 2022", "examen": "Parcial 2"}
    respuestas = pd.read_csv("data/respuestas.csv")
    dataPreguntas = []
    for cod in data["codigo"].values:
        correctas = 0
        for pregunta in respuestas.columns:
            if data[data["codigo"] == cod][pregunta].values[0] in respuestas[pregunta].values[0].split("|") or respuestas[pregunta].values[0] == "ANULADA":
                correctas += 1
        dataPreguntas.append([correctas, round(correctas*5.0/num_correctas,1) if (correctas/num_correctas <= 1) else 5.0])

    data[["correctas", "nota"]] = dataPreguntas
    print("Que desea")
    print("1. Generar todo")
    print("2. Solo informe del docente")
    print("3. Solo informes para estudiantes")
    print("4. Solo informe grupal")
    option = int(input("Ingrese la opción: "))

    #Falta por configurar
    resultados_aprendizaje = ('Estructuras de datos', 'Ordenamiento', 'Programación dinámica', 'Programación voraz')
    preg_res_aprendizaje = [[1], [0,2,3,4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]

    if option == 1:
        todo(data, respuestas, datos_examen,resultados_aprendizaje, preg_res_aprendizaje, estudiantes)
    elif option == 2:
        generarInformeDocente(data, estudiantes)
    elif option == 3:
        generarInformeEstudiantes(data, respuestas, resultados_aprendizaje, preg_res_aprendizaje)
    elif option == 4:
        generarInformeGrupal(data, respuestas, datos_examen, resultados_aprendizaje, preg_res_aprendizaje)
    else:
        print("Opcion no válida")

def todo(data, respuestas, datos_examen,resultados_aprendizaje, preg_res_aprendizaje,estudiantes):
    generarInformeDocente(data, estudiantes)
    generarInformeEstudiantes(data, respuestas, resultados_aprendizaje, preg_res_aprendizaje)
    generarInformeGrupal(data, respuestas, datos_examen, resultados_aprendizaje, preg_res_aprendizaje)

def generarInformeGrupal(data, respuestas, datos_examen, res_aprendizaje, preg_res_aprendizaje):
    plt.figure(dpi=150)

    final_mean = data["nota"].mean()
    final_std = data["nota"].std()

    pdf = scipy.stats.norm.pdf(data["nota"].sort_values(), final_mean, final_std)

    plt.plot(data["nota"].sort_values(), pdf)
    plt.xlabel("Nota", size=12)
    plt.ylabel("Frecuencia", size=12)
    plt.axvline(x=final_mean, color='b')
    plt.axvline(x=final_mean - final_std, color='b')
    plt.axvline(x=final_mean + final_std, color='b')
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.savefig("output/normal.png")

    pdf = PDF(format='letter')
    pdf.set_author('Carlos Delgado carlos.andres.delgado@correounivalle.edu.co')
    pdf.set_title("Informe grupal")


    total_grupo = data["codigo"].values.shape[0]
    preguntas = np.zeros((total_grupo, respuestas.shape[1]))
    count = 0
    for cod in data["codigo"].values:
        num_preg = 0
        for preg in respuestas.columns.sort_values():
            marcada_examen = data[data["codigo"] == cod][preg].values[0]
            correcta_examen = respuestas[preg].values[0]
            if marcada_examen == correcta_examen:
                preguntas[count, num_preg] = 1
            num_preg+=1
        count+=1

    promedio_preg = np.mean(preguntas, axis = 1)
    std_preg = np.std(preguntas, axis = 1)
    porcentaje_preg = 100*np.sum(preguntas, axis = 1) / num_preg
    pdf.add_page()
    pdf.set_font("Times", "B", 22)
    pdf.text(65, 12, "Informe grupal parcial")

    pdf.set_font("Times", "B", 18)
    pdf.text(5, 28, "Curso: " + datos_examen["nombre"])
    pdf.text(5, 38, "Fecha: " + datos_examen["fecha"])
    pdf.text(5, 48, "Prueba: " + datos_examen["examen"])

    pdf.set_font("Times", "", 12)
    pdf.image("output/normal.png", x=5, y=60, w=120, h=78)
    pdf.text(125, 80, "Promedio: " + str(round(final_mean, 2)))
    pdf.text(125, 86, "Deviación estandar: " + str(round(final_std, 2)))
    pdf.text(125, 92, "Nota del 66.3% del grupo: " + "[" + str(round(final_mean-final_std, 2)) +" , " + str(round(final_mean+final_std, 2)) +"]")
    count = 1
    pos = 100
    pdf.set_font("Times", "B", 18)
    pdf.text(65, 48 + pos, "Informe de respuestas")
    pdf.set_font("Times", "I", 14)
    pdf.text(5, 56 + pos, "Escala numérica entre 0.0 y 5.0")
    pdf.set_font("Times", "", 16)
    pdf.line(5, 70 + pos, 5, 62 + pos)
    pdf.line(5, 62 + pos, 200, 62 + pos)
    pdf.text(7, 68 + pos, "Pregunta")
    pdf.line(40, 70 + pos, 40, 62 + pos)
    pdf.text(45, 68 + pos, "Promedio")
    pdf.line(100, 70 + pos, 100, 62 + pos)
    pdf.text(105, 68 + pos, "desv stand")
    pdf.line(155, 70 + pos, 155, 62 + pos)
    pdf.text(160, 68 + pos, "% correcta")
    pdf.line(5, 70 + pos, 200, 70 + pos)
    pdf.line(200, 70 + pos, 200, 62 + pos)
    idx_preg = 0
    for preg in respuestas.columns.sort_values():
        if respuestas[preg].values[0] != "ANULADA":
            pdf.line(5, 76 + pos, 5, 68 + pos)
            pdf.text(7 + 12, 74 + pos, str(count))
            pdf.line(40, 76 + pos, 40, 68 + pos)
            pdf.text(45 + 20, 74 + pos, str(round(5*promedio_preg[idx_preg],2)))
            pdf.line(100, 76 + pos, 100, 68 + pos)
            pdf.text(105 + 20, 74 + pos, str(round(5*std_preg[idx_preg],2)))
            pdf.line(155, 76 + pos, 155, 68 + pos)

            correcta = porcentaje_preg[idx_preg]
            if correcta >= 60:
                pdf.set_text_color(0, 0, 255)
            else:
                pdf.set_text_color(255, 0, 0)
            pdf.set_text_color(0, 0, 0)
            pdf.line(5, 76 + pos, 200, 76 + pos)
            pdf.line(200, 76 + pos, 200, 68 + pos)
            pdf.text(160 + 15, 74 + pos, str(round(correcta,2)) + "%")
            pos += 6
        idx_preg+=1
        count+=1
    pdf.add_page()
    val_res_aprendizaje = []
    for pre in preg_res_aprendizaje:
        val_res_aprendizaje.append(np.mean(promedio_preg[pre]))

    dev_std_aprendizaje = []
    for pre in preg_res_aprendizaje:
        dev_std_aprendizaje.append(np.std(promedio_preg[pre]))

    pdf.set_font("Times", "B", 22)
    pdf.text(55, 15, "Resultados de aprendizaje")

    y = 0
    movy = 10  # Espacio para reporte

    for label, value, dstd in zip(res_aprendizaje, val_res_aprendizaje, dev_std_aprendizaje):
        pdf.set_font("Times", "B", 16)
        pdf.text(10, 35 + y, label)
        pdf.set_font("Times", "", 14)
        pdf.text(80, 35 + y, " Promedio: " + str(round(value * 5, 2)))
        pdf.text(130, 35 + y, "Dev estándar: " + str(round(dstd * 5, 2)))
        y += movy

    pdf.text(10, 35 + y, "Anotaciones:")
    y += movy
    pdf.text(10, 35 + y, "Los temas que tienen menor promedio y mayor desviación estándar son los de mayor dificultad")
    y += movy
    pdf.text(10, 35 + y, "Una promedio bajo indica que el grupo NO domina del tema")
    y += movy
    pdf.text(10, 35 + y, "Una deviación estándar elevada indica que el manejo del tema no es uniforme dentro del grupo")
    y += movy
    pdf.text(10, 35 + y, "Se debe hacer mayor enfasis en ellos en el éxamen opcional y en las sesiones de estudio")

    pdf.output("output/reporteGrupal.pdf", 'F')

def generarInformeDocente(data, estudiantes):
    #Informe del profesor (csv con notas)
    data_output = estudiantes.copy()
    data_output["correctas"] = 0
    data_output["nota"] = 0.0
    for idx, row in data_output.iterrows():
        codEstudiante = row["codigo"]
        cod = str(codEstudiante)[2:]
        estudiante = data[data["codigo"] == cod];
        if estudiante.shape[0] > 0:
            data_output.at[idx, "correctas"] = estudiante["correctas"].values[0]
            data_output.at[idx, "nota"] = estudiante["nota"].values[0]

    data_output[["nombre","codigo","correctas","nota"]].sort_values("nombre").to_csv("output/listaCalificaciones.csv")

def generarInformeEstudiantes(data, respuestas, res_aprendizaje, preg_res_aprendizaje):
    #Informe por estudiante
    for cod in data["codigo"].values:
        nombrearchivo = data[data["codigo"]==cod]["Nombre de archivo"].values[0]
        nombre = data[data["codigo"]==cod]["nombre"].values[0]
        codigo = data[data["codigo"] == cod]["codigo"].values[0]

        pdf = PDF(format='letter')
        pdf.set_author('Carlos Delgado carlos.andres.delgado@correounivalle.edu.co')
        pdf.set_title("Informe de calificaciones")
        pdf.add_page()
        pdf.set_font("Times","B",22)
        pdf.text(65,12,"Informe de exámen parcial")
        pdf.set_font("Times", "B", 18)
        pdf.text(5,28,"Estudiante: " + data[data["codigo"] == cod]["nombre"].values[0])
        pdf.text(5,38,"Código: " + str(data[data["codigo"] == cod]["codigo"].values[0]))
        pdf.text(5,48,"Nota: " + str(data[data["codigo"] == cod]["nota"].values[0]))
        pdf.text(65,58,"Informe de respuestas")

        pdf.set_font("Times", "", 16)
        pdf.line(5, 76, 5, 68)
        pdf.line(5, 68, 200, 68)
        pdf.text(7, 74, "Pregunta")
        pdf.line(40, 76, 40, 68)
        pdf.text(45, 74, "Respuesta marcada")
        pdf.line(100, 76, 100, 68)
        pdf.text(105, 74, "Respuesta correcta")
        pdf.line(155, 76, 155, 68)
        pdf.text(160, 74, "¿Es correcta?")
        pdf.line(5, 76, 200, 76)
        pdf.line(200, 76, 200, 68)

        pos = 6
        count = 1
        estadisticas = []
        for preg in respuestas.columns.sort_values():
            marcada_examen = data[data["codigo"] == cod][preg].values[0]
            correcta_examen = respuestas[preg].values[0].split("|")
            pdf.line(5, 76 +pos, 5, 68 +pos)
            pdf.text(7 + 12, 74 + pos, str(count))
            pdf.line(40, 76 + pos, 40, 68 + pos)
            pdf.text(45 + 20, 74 + pos, marcada_examen)
            pdf.line(100, 76 + pos, 100, 68 + pos)
            pdf.text(105 + 20, 74 + pos, "|".join(correcta_examen))
            pdf.line(155, 76 + pos, 155, 68 + pos)
            if marcada_examen in correcta_examen or correcta_examen == "ANULADA":
                pdf.set_text_color(0, 0, 255)
                pdf.text(160 + 15, 74 + pos, "SI")
                estadisticas.append(1)
            else:
                pdf.set_text_color(255, 0, 0)
                pdf.text(160 + 15, 74 + pos, "NO")
                estadisticas.append(0)
            pdf.set_text_color(0, 0, 0)
            pdf.line(5, 76 + pos, 200, 76 + pos)
            pdf.line(200, 76 + pos, 200, 68 + pos)
            pos+=6
            count+=1

        estadisticas = np.array(estadisticas)
        val_res_aprendizaje = []
        for pre in preg_res_aprendizaje:
            val_res_aprendizaje.append(np.average(estadisticas[pre]))

        num_correctas_marcadas = data[data["codigo"] == cod]["correctas"].values[0]
        pdf.text(10, 80 + pos, "Número de correctas: " + str(int(num_correctas_marcadas)))
        pdf.text(10, 90 + pos, "Preguntas correctas para 5.0: " + str(num_correctas))
        pdf.set_font("Times", "B", 22)
        pdf.text(10, 100 + pos, "Tus habilidades 0.0 a 5.0:")
        x = 0
        y = 0
        movx = 57 #Espacio para reporte
        movy = 10
        pdf.set_font("Times", "", 16)
        for label, value in zip(res_aprendizaje, val_res_aprendizaje):
            pdf.text(10 + x, 110 + pos + y, label + ": " + str(round(value*5,1)) )
            x += movx;
            if x > movx*2:
                x = 0
                y += movy
        pdf.set_font("Times", "B", 22)
        pdf.text(10, 130 + pos, "Apuntes finales:")

        pdf.set_font("Times", "", 16)
        pdf.text(10, 140 + pos, "Revisa la segunda página del informe y escribe un correo en caso de alguna inconsistencia")
        pdf.text(10, 150 + pos, "Escribe un correo a: carlos.andres.delgado@correounivalle.edu.co")
        pdf.add_page()
        pdf.image("data/procesado/" + nombrearchivo+".png",x=10,y=2,w=200,h=280)
        pdf.output('output/reports/' + nombre + "-" + codigo + ".pdf", 'F')

if __name__ == '__main__':
    procesar()

