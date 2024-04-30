import scipy
import matplotlib.pyplot as plt
import numpy as np

def generarInformeGrupal(data, respuestas, respuestas_totales, datos_examen, res_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, codificacion_examenes, consolidado, codificacion_preguntas, PDF):
    plt.figure(dpi=150)

    final_mean = data["nota"].mean()
    final_std = data["nota"].std()

    dist = scipy.stats.norm.pdf(data["nota"].sort_values(), final_mean, final_std)

    plt.plot(data["nota"].sort_values(), dist)
    plt.xlabel("Nota", size=12)
    plt.ylabel("Frecuencia", size=12)
    plt.axvline(x=final_mean, color='b')
    plt.axvline(x=final_mean - final_std, color='b')
    plt.axvline(x=final_mean + final_std, color='b')
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.savefig("output/normal.png")

    pdf = PDF(format='legal')
    pdf.set_author('Carlos Delgado carlos.andres.delgado@correounivalle.edu.co')
    pdf.set_title("Informe grupal")


    total_grupo = data["codigo"].values.shape[0]
    preguntas = np.zeros((total_grupo, respuestas_totales[0].shape[1]))

    count = 0
    promedio_preg = np.zeros(respuestas_totales[0].shape[1])
    examen = dict()
    resultados_estudiantes = []
    for cod,tipo_examen in zip(data["codigo"].values,data["examen"].values):
        examen_por_estudiante = []

        respuestas_correctas = consolidado[cod][0]
        respuestas_marcadas = consolidado[cod][1]
        num_preg = 0
        for marcada_examen, correcta_examen in zip(respuestas_marcadas, respuestas_correctas):
            if marcada_examen in correcta_examen:
                promedio_preg[num_preg] += 1/total_grupo
                examen_por_estudiante.append(1)
            else:
                examen_por_estudiante.append(0)    
            num_preg+=1
        count+=1
        #Expandir a 20 preguntas
        examen_general_estudiante = np.zeros(respuestas.shape[1])
        examen_general_estudiante[codificacion_preguntas] = examen_por_estudiante
        examen[cod] = (int(tipo_examen), examen_general_estudiante)
        resultados_estudiantes.append(examen_general_estudiante)

    resultados_estudiantes = np.array(resultados_estudiantes)
    std_preg = np.std(resultados_estudiantes, axis = 0)
    porcentaje_preg = np.sum(resultados_estudiantes, axis=0)/total_grupo
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


    pdf.set_font("Times", "B", 16)
    pdf.text(45, 150, "Resultados de aprendizaje del examen " )

    movy = 10  # Espacio para reporte
    y = 0
    promedio_grupal_aprendizaje = np.zeros(len(res_aprendizaje))
    promedio_grupal_desviacion = np.zeros(len(res_aprendizaje))
    for i in range(0, len(res_aprendizaje)):
        total_promedio = 0
        total_std = 0
        cnt_promedio = 0
        cnt_std = 0
        for preg_arp in preg_res_aprendizaje:
            obj_preg = preg_arp[i]
            total_promedio += np.sum(promedio_preg[obj_preg])
            total_std += np.sum(std_preg[obj_preg])
            cnt_promedio += len(promedio_preg[obj_preg])
            cnt_std += len(std_preg[obj_preg])
        promedio_grupal_aprendizaje[i] = total_promedio/cnt_promedio
        promedio_grupal_desviacion[i] = total_std/cnt_std
    
    for label, value, dstd in zip(res_aprendizaje, promedio_grupal_aprendizaje, promedio_grupal_desviacion):
        pdf.set_font("Times", "B", 16)
        pdf.text(10, 165 + y, label)
        pdf.set_font("Times", "", 14)
        y += movy
        pdf.text(10, 165 + y, " Promedio: " + str(round(value * 5, 2)))
        pdf.text(70, 165 + y, "Dev estándar: " + str(round(dstd * 5, 2)))
        y += movy

    y = 200
    pdf.text(10, 35 + y, "Anotaciones:")
    y += movy
    pdf.text(10, 35 + y, "Los temas que tienen menor promedio y mayor desviación estándar son los de mayor dificultad")
    y += movy
    pdf.text(10, 35 + y, "Una promedio bajo indica que el grupo NO domina del tema")
    y += movy
    pdf.text(10, 35 + y, "Una deviación estándar elevada indica que el manejo del tema no es uniforme dentro del grupo")
    y += movy
    pdf.text(10, 35 + y, "Se debe hacer mayor enfasis en ellos en el éxamen opcional y en las sesiones de estudio")
    
    pdf.add_page()
    count = 1
    pos = -10
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

    preguntas_estudiantes_totales = resultados_estudiantes.T
    cnt = 0
    for preg in preguntas_estudiantes_totales:
        if respuestas.iloc[0,cnt] != "ANULADA":
            pdf.line(5, 76 + pos, 5, 68 + pos)
            pdf.text(7 + 12, 74 + pos, str(count))
            pdf.line(40, 76 + pos, 40, 68 + pos)
            pdf.text(45 + 20, 74 + pos, str(round(5*preg.mean(),2)))
            pdf.line(100, 76 + pos, 100, 68 + pos)
            pdf.text(105 + 20, 74 + pos, str(round(5*preg.std(),2)))
            pdf.line(155, 76 + pos, 155, 68 + pos)

            correcta = preg.mean()
            

            pdf.line(5, 76 + pos, 200, 76 + pos)
            pdf.line(200, 76 + pos, 200, 68 + pos)
            if correcta >= 0.6:
                pdf.set_text_color(0, 0, 255)
            else:
                pdf.set_text_color(255, 0, 0)
            pdf.text(160 + 15, 74 + pos, str(round(100*correcta,2)) + "%")
            pdf.set_text_color(0, 0, 0)
            pos += 6
        idx_preg+=1
        count+=1
    

        movy = 10  # Espacio para reporteid
    cnt+=1

    
    pdf.output("output/reporteGrupal.pdf", 'F')

