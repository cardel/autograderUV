import numpy as np

def generarInformeEstudiantes(data, respuestas_totales, res_aprendizaje, preg_res_aprendizaje, codificacion_examenes, num_correctas, consolidado, codificacion_preguntas, PDF):
    #Informe por estudiante
    for cod,tipo_examen in zip(data["codigo"].values, data["examen"].values):
        respuestas = respuestas_totales[int(tipo_examen)]
        nombrearchivo = data[data["codigo"]==cod]["Nombre de archivo"].values[0]
        nombre = data[data["codigo"] == cod]["nombre"].values[0]
        codigo = data[data["codigo"] == cod]["codigo"].values[0]

        nombre_examen = codificacion_examenes[int(tipo_examen)]
        pdf = PDF(format='legal')
        pdf.set_author('Carlos Delgado carlos.andres.delgado@correounivalle.edu.co')
        pdf.set_title("Informe de calificaciones")
        pdf.add_page()
        pdf.set_font("Times","B",22)
        pdf.text(65,10,"Informe de exámen parcial")
        pdf.set_font("Times", "B", 18)
        pdf.text(5,24,"Estudiante: " + data[data["codigo"] == cod]["nombre"].values[0])
        pdf.text(5,34,"Código: " + str(data[data["codigo"] == cod]["codigo"].values[0]))
        pdf.text(5,44,"Nota: " + str(data[data["codigo"] == cod]["nota"].values[0]))
        pdf.text(5,54,"Examen: " + nombre_examen)
        pdf.text(65,64,"Informe de respuestas")

        pdf.set_font("Times", "", 16)
        pdf.line(5, 76, 5, 68)
        pdf.line(5, 68, 200, 68)
        pdf.text(7, 74, "Pregunta")
        pdf.line(40, 76, 40, 68)
        pdf.text(45, 74, "Respuesta marcada")
        pdf.line(100, 76, 100, 68)
        pdf.text(105, 74, "Respuesta correcta")
        pdf.line(155, 76, 155, 68)
        pdf.text(160, 74, "Desmpeño")
        pdf.line(5, 76, 200, 76)
        pdf.line(200, 76, 200, 68)

        pos = 6
        count = 1
        estadisticas = np.zeros(20)
        respuestas_correctas = consolidado[cod][0]
        marcadas = consolidado[cod][1]
        
        for correcta_examen, marcada_examen in zip(respuestas_correctas, marcadas):
            correcta_examen = correcta_examen.split("|")
            pdf.line(5, 76 +pos, 5, 68 +pos)
            pdf.text(7 + 12, 74 + pos, str(count))
            pdf.line(40, 76 + pos, 40, 68 + pos)
            pdf.text(45 + 20, 74 + pos, str(marcada_examen))
            pdf.line(100, 76 + pos, 100, 68 + pos)
            #Agregar otros factores
            otros = ""
            factor = len(otros)+3 if len(otros)>0 else 0
            pdf.text(105 + 20 - factor, 74 + pos, "|".join(correcta_examen)+otros)
            pdf.line(155, 76 + pos, 155, 68 + pos)
            numero_correctas = 0
            total_correctas = len(correcta_examen)
            
            for marcada in marcada_examen.split("|"):
                if marcada in correcta_examen:
                    numero_correctas+=1/total_correctas
                else:
                    numero_correctas-=1/(5-total_correctas)

            if "ANULADA" in correcta_examen:
                numero_correctas = 1

            if numero_correctas < 0:
                numero_correctas = 0

            if numero_correctas >= 0.5 or "ANULADA" in correcta_examen:
                pdf.set_text_color(0, 0, 255)
                pdf.text(160 + 15, 74 + pos, str(round(numero_correctas*100,2))+"%")
            else:
                pdf.set_text_color(255, 0, 0)
                pdf.text(160 + 15, 74 + pos, str(round(numero_correctas*100,2))+"%")
            num_pregunta = codificacion_preguntas[int(tipo_examen)][count-1]
            estadisticas[num_pregunta] = numero_correctas
            pdf.set_text_color(0, 0, 0)
            pdf.line(5, 76 + pos, 200, 76 + pos)
            pdf.line(200, 76 + pos, 200, 68 + pos)
            pos+=6
            count+=1

        estadisticas = np.array(estadisticas)
        val_res_aprendizaje = []
        for pre in preg_res_aprendizaje[int(tipo_examen)]:
            val_res_aprendizaje.append(np.average(estadisticas[pre]))
        num_correctas_marcadas = np.sum(estadisticas)
        pdf.text(10, 80 + pos, "Número de correctas: " + str(round(num_correctas_marcadas,2)))
        pdf.text(10, 90 + pos, "Preguntas correctas para 5.0: " + str(num_correctas))
        pdf.set_font("Times", "B", 22)
        pos+=5
        pdf.text(10, 100 + pos, "Tus habilidades 0.0 a 5.0:")
        x = 0
        y = 0
        movx = 57 #Espacio para reporte
        movy = 10
        pdf.set_font("Times", "", 16)
        general = codificacion_preguntas[int(tipo_examen)]
        for label, value, preg in zip(res_aprendizaje, val_res_aprendizaje, preg_res_aprendizaje[int(tipo_examen)]):
            pdf.text(10 + x, 110 + pos + y, label + ": " + str(round(value*5,1)) )
            y += movy
            index = list(map(lambda x: general.index(x), preg))
            pdf.text(10 + x, 110 + pos + y, "Preguntas asociadas: " + str(np.array(index)+1))
            y += movy
        pos+=y-10
        pdf.set_font("Times", "B", 22)
        pdf.text(10, 130 + pos, "Mapeo de preguntas:")

        posx = 0
        pos+=10
        pdf.set_font("Times", "", 16)
        pdf.line(5, 125+pos, 202, 125+pos)
        pdf.text(10, 130+pos, "Pregunta exámen")
        pdf.text(10, 140+pos, "Solucionario")
        pdf.line(5, 145+pos, 202, 145+pos)
        pdf.line(5,125+pos, 5, 145+pos)

        for i in range(0,len(codificacion_preguntas[int(tipo_examen)])):
            pdf.line(51+posx, 125+pos, 51+posx, 145+pos)
            pdf.text(54+posx, 130+pos, str(i+1) )
            pdf.text(54+posx, 140+pos, str(codificacion_preguntas[int(tipo_examen)][i]+1))
            posx += 10
        pdf.line(202,125+pos , 202 ,145+pos)
        pos+=30
        pdf.set_font("Times", "B", 22)
        """
        pdf.text(10, 130 + pos, "Apuntes finales:")
        pdf.set_font("Times", "", 16)
        pdf.text(10, 140 + pos, "Revisa la segunda página del informe y escribe un correo en caso de alguna inconsistencia")
        pdf.text(10, 150 + pos, "Escribe un correo a: carlos.andres.delgado@correounivalle.edu.co")
        """
        pdf.add_page()
        pdf.image("data/procesado/" + nombrearchivo+".png",x=10,y=2,w=200,h=280)
        pdf.output('output/reports/' + nombre + "-" + codigo + ".pdf", 'F')

