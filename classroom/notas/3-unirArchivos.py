import csv

NOTAS_FINALES = "notas_finales.csv"
SALIDA_FINAL = "salida_final.csv"
TOTAL = "total.csv"

# Leer el archivo notas_finales y crear un diccionario {ID: nota_final}
notas_dict = {}
with open(NOTAS_FINALES, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        notas_dict[row["ID"]] = row["nota_final"]

# Procesar salida_final.csv y agregar la nota_final
rows = []
with open(SALIDA_FINAL, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ["nota_final"]  # Agregar la nueva columna

    for row in reader:
        # Obtener la nota correspondiente al ID o '' si no existe
        row["nota_final"] = notas_dict.get(row["ID"], "")
        rows.append(row)

# Escribir el archivo total.csv
with open(TOTAL, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
