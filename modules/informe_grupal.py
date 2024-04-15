import scipy
import matplotlib.pyplot as plt
import numpy as np

def generarInformeGrupal(data, respuestas_totales, datos_examen, res_aprendizaje, preg_res_aprendizaje,estudiantes_tipo_examen, num_examenes, PDF):
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
    preguntas_por_examen = []
    
    for i in range(num_examenes):
        preguntas_por_examen.append([])

    num_preguntas_examen = respuestas_totales[0].shape[1]
    count = 0
    promedio_preg = np.zeros((num_examenes,respuestas_totales[0].shape[1]))
    for cod,tipo_examen in zip(data["codigo"].values,data["examen"].values):
        num_preg = 0
        respuestas = respuestas_totales[int(tipo_examen)]
        examen_por_estudiante = []
        for preg in respuestas.columns.sort_values():
            marcada_examen = data[data["codigo"] == cod][preg].values[0]
            correcta_examen = respuestas[preg].values[0]
            
            if marcada_examen in correcta_examen:
                preguntas[count, num_preg] = 1
                promedio_preg[int(tipo_examen),num_preg] += 1/estudiantes_tipo_examen[int(tipo_examen)]
                examen_por_estudiante.append(1)
            else:
                examen_por_estudiante.append(0)    
            num_preg+=1
        preguntas_por_examen[int(tipo_examen)].append(examen_por_estudiante)    
        count+=1

    std_preg = np.zeros((int(num_examenes),num_preguntas_examen))
    for i in range(num_examenes):
        std_preg[i,:] = np.std(np.array(preguntas_por_examen[i]), axis = 0)

    porcentaje_preg = np.zeros((int(num_examenes),num_preguntas_examen))
    for i in range(num_examenes):
        examen = np.array(preguntas_por_examen[i])
        porcentaje_preg[i,:] = np.sum(examen, axis=0)/np.sum(examen.shape[0])
    
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
    pdf.add_page()
    for num_examen in range(0,num_examenes):
        respuestas = respuestas_totales[int(num_examen)]
        count = 1
        pos = -10
        pdf.set_font("Times", "B", 18)
        pdf.text(65, 48 + pos, "Informe de respuestas, exámen "+ codificacion_examenes[int(num_examen)])
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
                pdf.text(45 + 20, 74 + pos, str(round(5*promedio_preg[int(num_examen),idx_preg],2)))
                pdf.line(100, 76 + pos, 100, 68 + pos)
                pdf.text(105 + 20, 74 + pos, str(round(5*std_preg[int(num_examen),idx_preg],2)))
                pdf.line(155, 76 + pos, 155, 68 + pos)

                correcta = porcentaje_preg[int(num_examen),idx_preg]
                

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
        val_res_aprendizaje = []
        for pre in preg_res_aprendizaje:
            val_res_aprendizaje.append(np.mean(promedio_preg[num_examen,pre]))

        dev_std_aprendizaje = []
        for pre in preg_res_aprendizaje:
            dev_std_aprendizaje.append(np.std(promedio_preg[num_examen,pre]))
        
        y = pos + 70
        pdf.set_font("Times", "B", 16)
        pdf.text(45, 15+y, "Resultados de aprendizaje del examen " + codificacion_examenes[num_examen])

        movy = 10  # Espacio para reporte

        for label, value, dstd in zip(res_aprendizaje, val_res_aprendizaje, dev_std_aprendizaje):
            pdf.set_font("Times", "B", 16)
            pdf.text(10, 35 + y, label)
            pdf.set_font("Times", "", 14)
            pdf.text(100, 35 + y, " Promedio: " + str(round(value * 5, 2)))
            pdf.text(150, 35 + y, "Dev estándar: " + str(round(dstd * 5, 2)))
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
        if num_examen < num_examenes - 1:
            pdf.add_page()
    
    pdf.output("output/reporteGrupal.pdf", 'F')

