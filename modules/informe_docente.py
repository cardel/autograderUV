def generarInformeDocente(data, estudiantes):
	#Informe del profesor (csv con notas)
	data_output = estudiantes.copy()
	data_output["correctas"] = 0.0
	data_output["nota"] = 0.0
	for idx, row in data_output.iterrows():
		codEstudiante = row["codigo"]
		cod = str(codEstudiante)[2:]
		estudiante = data[data["codigo"] == cod];
		if estudiante.shape[0] > 0:
			data_output.at[idx, "correctas"] = estudiante["correctas"].values[0]
			data_output.at[idx, "nota"] = estudiante["nota"].values[0]
			data_output.at[idx, "numeroID"] = estudiante["numeroID"].values[0]
		else:
			data_output.at[idx, "numeroID"] = str(row["codigo"])[2:]+"-"+str(row["programa"])

	data_output[["nombre","codigo","correctas","nota","numeroID"]].sort_values("nombre").to_csv("output/listaCalificaciones.csv")

