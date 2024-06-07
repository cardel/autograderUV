import pandas as pd
import numpy as np

def crear_codigo(value):
    return str(value)

def procesar(num_correctas, num_examenes, codificacion_examenes, materia, fecha, examen, codificacion_preguntas):
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
    
    data.fillna("No marcada", inplace=True)
    
    #Lemos las 20 preguntas
    respuestas_csv = pd.read_csv("data/respuestas.csv") 
    respuestas_totales = []
    for codif in codificacion_preguntas:
        respuestas_totales.append(respuestas_csv.iloc[:,codif])

    estudiantes_tipo_examen = np.zeros((num_examenes))
    dataPreguntas = []
    consolidado = dict()
    for cod,tipo_examen in zip(data["codigo"].values, data["examen"].values):
        correctas = 0.0
        respuestas = respuestas_totales[int(tipo_examen)].values[0]
        marcadas = data[data["codigo"] == cod].values[0,1:16]
        consolidado[cod] = [respuestas, marcadas]
        for resp,marc in zip(respuestas,marcadas):
            if resp == "ANULADA":
                correctas += 1
                continue
            respuestas_correctas =  resp.split("|")
            total_correctas = len(respuestas_correctas)
            respuestas_marcadas = marc.split("|")
            valor_pregunta = 0
            #Caso de respuesta única
            if len(respuestas_correctas) == 1:
                if respuestas_correctas[0] in respuestas_marcadas:
                    valor_pregunta = 1
                else:
                    valor_pregunta = 0
                    continue
            else:
                #Caso respuesta múltiple
                for resp in respuestas_marcadas:
                    if resp in respuestas_correctas:
                        valor_pregunta += 1.0/total_correctas
                    else:
                        valor_pregunta -= 1.0/(5.0 - total_correctas)
            if valor_pregunta < 0:
                valor_pregunta = 0
            correctas += valor_pregunta
        dataPreguntas.append([float(correctas), round(correctas*5.0/num_correctas,1) if (correctas/num_correctas <= 1) else 5.0])
    data[["correctas", "nota"]] = dataPreguntas
    return data, respuestas_csv, respuestas_totales, datos_examen, estudiantes_tipo_examen, estudiantes, consolidado
