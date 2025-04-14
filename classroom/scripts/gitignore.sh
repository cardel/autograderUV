#!/bin/bash

OUTPUT_FILE="nogitignore.txt"

echo "Listado de repositorios sin .gitignore en su raíz" > "$OUTPUT_FILE"
echo "Generado el: $(date)" >> "$OUTPUT_FILE"
echo "=============================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

COUNT=0

# Buscar todos los repositorios Git (carpetas que contienen .git)
find . -type d -name ".git" | while read -r git_folder; do
    repo_dir=$(dirname "$git_folder")
    
    # Verificar si no existe .gitignore en la raíz del repositorio
    if [ ! -f "$repo_dir/.gitignore" ]; then
        echo "$repo_dir" >> "$OUTPUT_FILE"
        ((COUNT++))
    fi
done

echo "" >> "$OUTPUT_FILE"
echo "Total de repositorios sin .gitignore en raíz: $COUNT" >> "$OUTPUT_FILE"

echo "Proceso completado. Se encontraron $COUNT repositorios sin .gitignore en su raíz."
echo "El listado se ha guardado en: $OUTPUT_FILE"
