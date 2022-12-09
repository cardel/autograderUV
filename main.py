import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from fpdf import FPDF


class PDF(FPDF):
    pass  # nothing happens when it is executed.


num_correctas = 13

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

    dataEstudiante = np.array(dataEstudiante)
    data[["nombre","correo"]] = dataEstudiante

    respuestas = pd.read_csv("data/respuestas.csv")
    dataPreguntas = []
    for cod in data["codigo"].values:
        correctas = 0
        for pregunta in respuestas.columns:
            if data[data["codigo"] == cod][pregunta].values[0] == respuestas[pregunta].values[0] or respuestas[pregunta].values[0] == "ANULADA":
                correctas+=1
        dataPreguntas.append([correctas, round(correctas*5.0/num_correctas,1) if (correctas/num_correctas <= 1) else 5.0])

    data[["correctas", "nota"]] = dataPreguntas
    data[["nombre","codigo","correctas","nota"]].sort_values("nombre").to_csv("output/listaCalificaciones.csv")
    generarSalidas(data, respuestas)

def generarSalidas(data, respuestas):
    #Informe del profesor
    plt.figure(dpi=150)

    final_mean = data["nota"].mean()
    final_std = data["nota"].std()

    pdf = scipy.stats.norm.pdf(data["nota"].sort_values(), final_mean, final_std)

    plt.plot(data["nota"].sort_values(), pdf)
    plt.xlabel("Nota", size=12)
    plt.ylabel("Frecuencia", size=12)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.savefig("output/normal.png")

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

        pos = 6;
        count = 1;
        estadisticas = []
        for preg in respuestas.columns.sort_values():
            marcada_examen = data[data["codigo"] == cod][preg].values[0]
            correcta_examen = respuestas[preg].values[0]
            pdf.line(5, 76 +pos, 5, 68 +pos)
            pdf.text(7 + 12, 74 + pos, str(count))
            pdf.line(40, 76 + pos, 40, 68 + pos)
            pdf.text(45 + 20, 74 + pos, marcada_examen)
            pdf.line(100, 76 + pos, 100, 68 + pos)
            pdf.text(105 + 20, 74 + pos, correcta_examen)
            pdf.line(155, 76 + pos, 155, 68 + pos)
            if marcada_examen == correcta_examen or correcta_examen == "ANULADA":
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

        plt.figure(dpi=150)
        estadisticas = np.array(estadisticas)
        res1 = np.average(estadisticas[[0,1,2,4]])
        res2 = np.average(estadisticas[[5,6,7,8,9]])
        res3 = np.average(estadisticas[[10,11,12,13,14]])
        res4 = np.average(estadisticas[[10,11,12,13,14]])
        labels = ('Conteo básico', 'RR Homogeneas', 'RR No homogeneas')
        values = [res1, res2, res3]
        num_correctas_marcadas = data[data["codigo"] == cod]["correctas"].values[0]
        pdf.text(10, 80 + pos, "Número de correctas: " + str(int(num_correctas_marcadas)))
        pdf.text(10, 90 + pos, "Preguntas correctas para 5.0: " + str(num_correctas))
        pdf.set_font("Times", "B", 22)
        pdf.text(10, 100 + pos, "Tus habilidades 0.0 a 5.0:")
        x = 0
        y = 0
        mov = 57
        pdf.set_font("Times", "", 16)
        for label, value in zip(labels, values):
            pdf.text(10 + x, 110 + pos + y, label + ": " + str(round(value*5,1)) )
            x += 57;
            if x > 57*2:
                x = 0
                y += 10
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

