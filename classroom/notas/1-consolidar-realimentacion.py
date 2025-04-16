import csv
import os
import re


def read_filtered_result_file(file_path):
    """Lee las primeras 25 líneas del archivo result, eliminando la línea 2"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Tomar primeras 25 líneas (o menos si el archivo es más corto)
    filtered_lines = lines[:25]

    # Buscar en las 3 primeras lineas la palabra "integrantes" sin distinción de mayúsculas
    for i in range(3):
        if re.search(r"integrantes", filtered_lines[i], re.IGNORECASE):
            # Si se encuentra, eliminar la línea
            del filtered_lines[i]
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
    """Procesa todos los archivos result_i y devuelve un diccionario por username"""
    result_data = {}

    # Expresión regular mejorada para extraer el nombre del repositorio
    repo_name_pattern = re.compile(
        r"\*\*Repositorio:\*\*\s*(.*?)\s*$", re.IGNORECASE | re.MULTILINE
    )

    for filename in sorted(os.listdir(result_files_dir)):
        if filename.startswith("result_") and not os.path.isdir(
            os.path.join(result_files_dir, filename)
        ):
            file_path = os.path.join(result_files_dir, filename)

            # Leer contenido para extraer nombre de repositorio
            with open(file_path, "r", encoding="utf-8") as file:
                # Leer suficiente para encontrar el nombre
                content = file.read(1000)

            repo_match = repo_name_pattern.search(content)
            if not repo_match:
                print(
                    f"Advertencia: No se encontró nombre de repositorio en {filename}"
                )
                continue

            repo_name = repo_match.group(1).strip()
            username = repo_name.split("/")[0].strip().lower()

            if not username:
                print(
                    f"Advertencia: No se pudo extraer username de {repo_name} en {
                        filename
                    }"
                )
                continue

            # Leer el contenido filtrado
            feedback_content = read_filtered_result_file(file_path)
            result_data[username] = {
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
            github_username = row["github_username"].strip().lower()
            updated_row = row.copy()
            result_keys = result_data.keys()
            # El github_username esta contenido dentro de alguna de las llaves del diccionario
            # Buscar y asignar una variable llamada repo_match, la comparación debe ignorar mayúsculas
            repo_match = None
            for key in result_keys:
                if github_username in key:
                    repo_match = key
                    break

            # Buscar coincidencia por username
            if repo_match is not None:
                matching_data = result_data[repo_match]
                updated_row["student_repository_name"] = matching_data["repo_name"]
                updated_row["realimentacion"] = matching_data["feedback"]
            else:
                updated_row["realimentacion"] = ""
                print(f"Advertencia: No se encontró feedback para {github_username}")

            writer.writerow(updated_row)


if __name__ == "__main__":
    # Configura estos paths según tus necesidades
    input_csv_path = "grades.csv"
    result_files_dir = "."
    output_csv_path = "realimentacion.csv"

    main(input_csv_path, result_files_dir, output_csv_path)
