import csv
from collections import defaultdict

CAMPUS_CSV = "github.csv"
GRADES_CSV = "grades.csv"
SALIDA_CSV = "notas_finales.csv"


def procesar_csv():
    # Leer el primer archivo CSV (usuarios)
    usuarios = []
    with open(CAMPUS_CSV, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            usuarios.append(
                {
                    "ID": row["Número de ID"],
                    "github_original": row["github"]
                    .strip()
                    .lower(),
                    "email": row["Correo electrónico"],
                }
            )

    # Leer el segundo archivo CSV (asignaciones)
    asignaciones = defaultdict(list)
    with open(GRADES_CSV, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row["github_username"].strip().lower()
            if not username:
                continue

            try:
                points_awarded = (
                    float(row["points_awarded"]) if row["points_awarded"] else 0.0
                )
                points_available = (
                    float(row["points_available"]) if row["points_available"] else 1.0
                )
                nota = round(5 * points_awarded / points_available, 1)
            except (ValueError, ZeroDivisionError):
                nota = 0.0

            asignaciones[username].append(nota)

    # Calcular la nota promedio por usuario
    notas_promedio = {}
    for username, notas in asignaciones.items():
        notas_promedio[username] = round(sum(notas) / len(notas), 1)

    # Combinar los datos y preparar el archivo de salida
    resultados = []
    for usuario in usuarios:
        github = usuario["github_original"]
        nota = notas_promedio.get(github, 0.0)

        resultados.append(
            {"ID": usuario["ID"], "github_username": github, "nota": nota}
        )

    # Escribir el archivo de salida
    with open(SALIDA_CSV, mode="w", encoding="utf-8", newline="") as file:
        campos = ["ID", "github_username", "nota"]
        writer = csv.DictWriter(file, fieldnames=campos)

        writer.writeheader()
        writer.writerows(resultados)

    print(f"Archivo {SALIDA_CSV} generado con éxito.")


if __name__ == "__main__":
    procesar_csv()
