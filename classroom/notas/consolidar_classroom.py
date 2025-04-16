import csv
import os
import re


def read_filtered_result_file(file_path):
    """Lee las primeras 3 líneas del archivo result, eliminando líneas con 'Integrantes'"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [
            line
            for line in file.readlines()[:3]
            if not re.search(r"integrantes", line, re.IGNORECASE)
        ]
    return "".join(lines).lower()  # Convertir a minúsculas para comparación


def process_result_files(result_files_dir):
    """Procesa todos los archivos result_i y devuelve un diccionario {username: feedback}"""
    result_data = {}

    for filename in sorted(os.listdir(result_files_dir)):
        if filename.startswith("result_") and filename.endswith(".txt"):
            file_path = os.path.join(result_files_dir, filename)

            # Leer contenido filtrado (primeras 3 líneas sin "Integrantes")
            content = read_filtered_result_file(file_path)

            # El username podría aparecer en cualquier parte de estas líneas
            # Lo guardamos para hacer match después con el CSV
            result_data[filename] = (
                content  # Usamos el nombre de archivo como clave temporal
            )

    return result_data


def find_matching_username(content, github_username):
    """Busca el github_username en el contenido (ya en minúsculas)"""
    return github_username.lower() in content


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
            updated_row = row.copy()
            github_username = row["github_username"].strip().lower()
            updated_row["realimentacion"] = ""

            # Buscar en todos los archivos result
            for filename, content in result_data.items():
                if find_matching_username(content, github_username):
                    # Leer el archivo completo (sin filtros) para el feedback
                    with open(
                        os.path.join(result_files_dir, filename), "r", encoding="utf-8"
                    ) as f:
                        full_content = f.read()
                    # Eliminar líneas con "Integrantes"
                    filtered_content = "\n".join(
                        line
                        for line in full_content.split("\n")
                        if not re.search(r"integrantes", line, re.IGNORECASE)
                    )
                    updated_row["realimentacion"] = filtered_content
                    break

            if not updated_row["realimentacion"]:
                print(f"Advertencia: No se encontró feedback para {
                      github_username}")

            writer.writerow(updated_row)


if __name__ == "__main__":
    # Configuración de paths
    input_csv_path = "input.csv"
    result_files_dir = "."  # Directorio con archivos result_i.txt
    output_csv_path = "realimentacion.csv"

    main(input_csv_path, result_files_dir, output_csv_path)
