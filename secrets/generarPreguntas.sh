#!/bin/bash

# Contador para los archivos qN.txt
counter=1

# Buscar todas las carpetas en el directorio actual (excepto ocultas)
for folder in */; do
	# Eliminar la barra final del nombre
	folder_name=${folder%/}

	# Nombre del archivo de salida (q1.txt, q2.txt, etc.)
	output_file="q${counter}.txt"

	# Incrementar contador
	((counter++))

	# Crear archivo y escribir nombre de la carpeta
	echo "=== REPOSITORIO: $folder_name ===" >"$output_file"
	echo "" >>"$output_file"

	# --- SECCIÓN DE CÓDIGO ---
	echo "### ARCHIVOS DE CÓDIGO ###" >>"$output_file"
	echo "" >>"$output_file"

	find "$folder_name" -type f \( -name "*.scala" -o -name "*.java" -o -name "*.py" -o -name "*.cpp" -o -name "*.mzn" -o -name "*.dzn" \) \
		-not -path "*informes_contribuciones/*" \
		-not -name "*package*" | while read code_file; do
		echo ">>> $code_file <<<" >>"$output_file"
		echo "" >>"$output_file"
		cat "$code_file" >>"$output_file"
		echo "" >>"$output_file"
		echo "--------------------------------------------------" >>"$output_file"
		echo "" >>"$output_file"
	done
	# --- SECCIÓN DE README (RAÍZ) ---
	echo "### README (archivo raíz) ###" >>"$output_file"
	echo "" >>"$output_file"

	# Buscar README.md (insensible a mayúsculas/minúsculas) en la raíz
	find "$folder_name" -maxdepth 1 -type f -iname "readme.md" | while read readme_file; do
		echo ">>> $readme_file <<<" >>"$output_file"
		echo "" >>"$output_file"
		cat "$readme_file" >>"$output_file"
		echo "" >>"$output_file"
		echo "--------------------------------------------------" >>"$output_file"
		echo "" >>"$output_file"
	done

	# --- SECCIÓN DE DOCUMENTACIÓN (docs/) ---
	echo "### DOCUMENTACIÓN (archivos .md en docs/) ###" >>"$output_file"
	echo "" >>"$output_file"

	# Buscar archivos .md en docs/ o cualquier variación de mayúsculas/minúsculas (si existe la carpeta)
	found_docs_folder=$(find "$folder_name" -maxdepth 1 -type d -iname "docs" | head -n 1)

	if [ -n "$found_docs_folder" ]; then
		find "$found_docs_folder" -type f -name "*.md" | while read md_file; do
			echo ">>> $md_file <<<" >>"$output_file"
			echo "" >>"$output_file"
			cat "$md_file" >>"$output_file"
			echo "" >>"$output_file"
			echo "--------------------------------------------------" >>"$output_file"
			echo "" >>"$output_file"
		done
	else
		echo "No se encontró la carpeta 'docs/' (o cualquier variación de mayúsculas) en $folder_name" >>"$output_file"
		echo "" >>"$output_file"
	fi

	echo "✅ Procesado: $folder_name → $output_file"
done

echo "✨ ¡Listo! Se generaron $((counter - 1)) archivos qN.txt."
