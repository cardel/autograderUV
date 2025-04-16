import csv


def main():
    # Archivos de entrada y salida
    input_feedback = "realimentacion.csv"
    input_github = "github.csv"
    output_file = "salida_final.csv"
    not_found_file = "no_encontrado.csv"

    # Leer los datos de github.csv y crear un diccionario {username: id}
    github_users = {}
    with open(input_github, "r", encoding="utf-8") as github_file:
        reader = csv.DictReader(github_file)
        for row in reader:
            username = row["Indicar su usuario de Github"].strip().lower()
            user_id = row["Número de ID"].strip()
            github_users[username] = user_id

    # Columnas deseadas en la salida
    output_columns = [
        "github_username",
        "points_awarded",
        "points_available",
        "realimentacion",
        "ID",
    ]

    # Procesar realimentacion.csv
    with (
        open(input_feedback, "r", encoding="utf-8") as feedback_file,
        open(output_file, "w", newline="", encoding="utf-8") as out_file,
        open(not_found_file, "w", newline="", encoding="utf-8") as not_found_out_file,
    ):
        reader = csv.DictReader(feedback_file)

        # Configurar writers para ambos archivos con las columnas especificadas
        writer = csv.DictWriter(out_file, fieldnames=output_columns)
        not_found_writer = csv.DictWriter(
            not_found_out_file,
            # Sin columna ID
            fieldnames=[col for col in output_columns if col != "ID"],
        )

        writer.writeheader()
        not_found_writer.writeheader()

        for row in reader:
            username = row["github_username"].strip().lower()
            user_id = github_users.get(username, "")

            # Crear fila filtrada solo con las columnas deseadas
            filtered_row = {
                "github_username": row["github_username"],
                "points_awarded": row["points_awarded"],
                "points_available": row["points_available"],
                "realimentacion": row.get(
                    "realimentacion", ""
                ),  # Usar get por si no existe
                "ID": user_id,
            }

            if user_id:  # Si se encontró el ID
                writer.writerow(filtered_row)
            else:  # Si NO se encontró el ID
                # Eliminar la columna ID para el archivo no_encontrado
                del filtered_row["ID"]
                not_found_writer.writerow(filtered_row)


if __name__ == "__main__":
    main()
