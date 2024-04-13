import pandas as pd
import numpy as np


def crear_codigo(value):
    value = value.replace(" ", "")
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
        return -1


def procesar(num_correctas, num_examenes, codificacion_examenes):
    data = pd.read_csv("data/resultados.csv")
	tipo_parcial = data["tipo.Pregunta023"].apply(crear_codigo)
    data.drop(columns=["tipo.Pregunta023"], inplace=True)

    C0 = data["cod.Pregunta001"].apply(crear_codigo)
    C1 = data["cod.Pregunta002"].apply(crear_codigo)
    C2 = data["cod.Pregunta003"].apply(crear_codigo)
    C3 = data["cod.Pregunta004"].apply(crear_codigo)
    C4 = data["cod.Pregunta005"].apply(crear_codigo)
    C5 = data["cod.Pregunta006"].apply(crear_codigo)
    C6 = data["cod.Pregunta007"].apply(crear_codigo)

    

    codigo = pd.DataFrame([C0,C1,C2,C3,C4,C5,C6]).transpose()
    codigo["codigo"] = codigo.apply("".join, axis=1)
    data["codigo"] = codigo["codigo"]
    data["examen"] = tipo_parcial

    estudiantes = pd.read_csv("data/listadoClase.csv")

    dataEstudiante = []
    for cod in data["codigo"].values:
        codEstudiante = int("20" + cod)
        nombre = estudiantes[estudiantes["codigo"] == codEstudiante]["nombre"].values.tolist()
        correo = estudiantes[estudiantes["codigo"] == codEstudiante]["correo"].values.tolist()
        programa = estudiantes[estudiantes["codigo"] == codEstudiante]["programa"].values.tolist()
        if len(nombre) > 0:
            dataEstudiante.append([nombre[0],correo[0],str(cod)+"-"+str(programa[0])])
        else:
            print("Estudiante no encontrado")
            print(data[data["codigo"] == cod])
            print("Causa 1) El estudiante se equivocó al escribir el código")
            print("Causa 2) Hubo un problema al escanear")
            print("Corrige este problema antes de continuar")
            exit(0)

    dataEstudiante = np.array(dataEstudiante)
    data[["nombre","correo","numeroID"]] = dataEstudiante
    datos_examen = {"nombre": materia, "fecha": fecha, "examen": examen}
    
    respuestas_totales = []

    for i in range(num_examenes):
        respuestas_totales.append(pd.read_csv("data/respuestas"+codificacion_examenes[i]+".csv"))
    
    estudiantes_tipo_examen = np.zeros((num_examenes))
    dataPreguntas = []
    for cod,tipo_examen in zip(data["codigo"].values, data["examen"].values):
        correctas = 0.0
        respuestas = respuestas_totales[int(tipo_examen)]
        estudiantes_tipo_examen[int(tipo_examen)] += 1
        for pregunta in respuestas.columns:
            factor = 1
            for i in range(0,3):
                if type(respuestas[pregunta].values[i]) is not str:
                    continue
                if "ANULADA" in respuestas[pregunta].values[i]:
                    correctas+=1
                    continue
                if data[data["codigo"] == cod][pregunta].values[0] in respuestas[pregunta].values[i].split("|"):
                    correctas += factor
                factor -= 0.25 #Esto es cuando tenemos valores diferentes
        dataPreguntas.append([correctas, round(correctas*5.0/num_correctas+0.001,1) if (correctas/num_correctas <= 1) else 5.0])

    data[["correctas", "nota"]] = dataPreguntas
    return data
