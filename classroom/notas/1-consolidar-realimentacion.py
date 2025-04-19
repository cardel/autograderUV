import csv
import os
import re


def read_filtered_result_file(file_path):
    """Lee las primeras 25 líneas del archivo result, eliminando la línea 2"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Tomar primeras 25 líneas (o menos si el archivo es más corto)
    filtered_lines = lines[:25]

    # Eliminar siempre la segunda línea (índice 1)
    if len(filtered_lines) > 1:
        del filtered_lines[1]

    # Eliminar lineas que tengan la palabra documentación (con tilde o sin ella) y sin diferencia de mayúscula sin acentos
    filtered_lines = [
        linea
        for linea in filtered_lines
        if not re.search(r"documentaci[oó]n|nota", linea, re.IGNORECASE)
    ]
    texto_filtrado = "\n".join(filtered_lines)
    # Reemplaza 2+ \n por 1 \n
    texto_filtrado = re.sub(r"\n{2,}", "\n", texto_filtrado)

    return texto_filtrado


def process_result_files(result_files_dir):
    """Procesa todos los archivos result_i y devuelve un diccionario por repo_name"""
    result_data = {}

    for filename in sorted(os.listdir(result_files_dir)):
        if filename.startswith("result_") and not os.path.isdir(
            os.path.join(result_files_dir, filename)
        ):
            file_path = os.path.join(result_files_dir, filename)

            # Leer la primera línea para obtener el nombre del repositorio
            with open(file_path, "r", encoding="utf-8") as file:
                repo_name = file.readline().strip()

                # Leer el contenido filtrado (después de la primera línea)
                feedback_content = read_filtered_result_file(file_path)

                # Eliminar la primera línea del feedback (ya que es el repo_name)
                feedback_lines = feedback_content.split("\n")
                if len(feedback_lines) > 1:
                    feedback_content = "\n".join(feedback_lines[1:])
                else:
                    feedback_content = ""

                result_data[repo_name.lower()] = {
                    "repo_name": repo_name,
                    "feedback": feedback_content,
                }

    return result_data


def main(input_csv_path, result_files_dir, output_csv_path):
    # Procesar archivos result
    result_data = process_result_files(result_files_dir)

    # Leer el CSV original y crear el nuevo
    with (
        open(input_csv_path, "r", encoding="utf-8") as input_file,
        open(output_csv_path, "w", newline="", encoding="utf-8") as output_file,
    ):
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ["realimentacion"]

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            repo_name = row["student_repository_name"].strip().lower()
            updated_row = row.copy()

            # Buscar coincidencia por nombre de repositorio
            if repo_name in result_data:
                matching_data = result_data[repo_name]
                updated_row["realimentacion"] = matching_data["feedback"]
            else:
                updated_row["realimentacion"] = ""
                print(f"Advertencia: No se encontró feedback para {repo_name}")

            writer.writerow(updated_row)


if __name__ == "__main__":
    # Configura estos paths según tus necesidades
    input_csv_path = "grades.csv"
    result_files_dir = "."
    output_csv_path = "realimentacion.csv"

    main(input_csv_path, result_files_dir, output_csv_path)
