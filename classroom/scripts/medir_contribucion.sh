#!/bin/bash

# Configuración
OUTPUT_DIR="informes_contribuciones"

# Función para limpiar y preparar el directorio de salida
prepare_output_dir() {
    if [ -d "$OUTPUT_DIR" ]; then
        # Borrar solo el contenido, no la carpeta
        rm -rf "$OUTPUT_DIR"/*
        echo "Contenido de la carpeta de salida eliminado: $OUTPUT_DIR"
    else
        # Crear el directorio si no existe
        mkdir -p "$OUTPUT_DIR"
        echo "Carpeta de salida creada: $OUTPUT_DIR"
    fi

    echo ""
}


# Función para analizar contribuciones en un repositorio
analyze_repo() {
    local repo_path="$1"
    cd "$repo_path" || return
    
    local repo_name
    repo_name=$(basename "$repo_path")
    local output_file="../${OUTPUT_DIR}/${repo_name}_contribuciones.txt"

    # Crear/sobreescribir el archivo de salida
    > "${output_file}"
    
    echo "Analizando repositorio: $repo_name" | tee "$output_file"
    echo "=============================================" | tee -a "$output_file"
    
    # Obtener lista de autores excluyendo github-classroom
    local authors
    authors=$(git shortlog -s --all | grep -vi "github-classroom" | cut -c8-)
    
    # Variables para totales globales
    local total_added=0
    local total_subs=0
    local total_loc=0
    declare -A user_totals  # Array asociativo para totales por usuario
    
    # Primera pasada para calcular totales globales y por usuario
    while read -r i; do
        # Estadísticas generales del usuario
        stats=$(git log --author="$i" --pretty=tformat: --numstat | \
            awk '{add += $1; subs += $2; loc += $1 - $2} END {print add, subs, loc}')
        
        user_added=$(echo "$stats" | awk '{print $1}')
        user_subs=$(echo "$stats" | awk '{print $2}')
        user_loc=$(echo "$stats" | awk '{print $3}')
        
        # Acumular totales globales
        total_added=$((total_added + user_added))
        total_subs=$((total_subs + user_subs))
        total_loc=$((total_loc + user_loc))
        
        # Guardar totales por usuario
        user_totals["$i"]="$user_added $user_subs $user_loc"
    done <<< "$authors"
    
    # Segunda pasada para mostrar estadísticas con porcentajes
    while read -r i; do
		read -r user_added user_subs user_loc <<< "${user_totals["$i"]}"

		echo "Autor: $i" | tee -a "$output_file"
        # Calcular porcentajes de contribución total
        local pct_total_add=0
        local pct_total_sub=0
        local pct_total_loc=0
        
        if [ $total_added -gt 0 ]; then
            pct_total_add=$(echo "scale=2; $user_added * 100 / $total_added" | bc)
            pct_total_sub=$(echo "scale=2; $user_subs * 100 / $total_subs" | bc)
            pct_total_loc=$(echo "scale=2; $user_loc * 100 / $total_loc" | bc)
        fi
        
        # Estadísticas generales con porcentaje total
        echo "  - Totales:" | tee -a "$output_file"
        echo "    - Líneas agregadas: $user_added ($pct_total_add% del total)" | tee -a "$output_file"
        echo "    - Líneas eliminadas: $user_subs ($pct_total_sub% del total)" | tee -a "$output_file"
        echo "    - Líneas netas: $user_loc ($pct_total_loc% del total)" | tee -a "$output_file"
        
        # Estadísticas para documentos (solo .md en docs/)
		doc_stats=$(git log --author="$i" --pretty=tformat: --numstat --glob='*docs*/*.md' | \
			awk '{add += $1; subs += $2; loc += $1 - $2} END {
				printf "  - Documentación (.md en docs/):\n    - Líneas agregadas: %s\n    - Líneas eliminadas: %s\n    - Líneas netas: %s\n", add, subs, loc
			}')
        echo "$doc_stats" | tee -a "$output_file"
        
        # Estadísticas para código (excluyendo .md)
        code_stats=$(git log --author="$i" --pretty=tformat: --numstat -- . ":!*.md" | \
            awk '{add += $1; subs += $2; loc += $1 - $2} END {
                printf "  - Código (excluyendo .md):\n    - Líneas agregadas: %s\n    - Líneas eliminadas: %s\n    - Líneas netas: %s\n", add, subs, loc
            }')
        echo "$code_stats" | tee -a "$output_file"
        
        # Estadísticas de código significativo (ignorando espacios y comentarios)
        echo "  - Código significativo (excluyendo espacios y comentarios):" | tee -a "$output_file"
        git log --author="$i" --pretty=tformat:%H | while read -r commit; do
            git show --pretty="format:" --name-only "$commit" | \
            grep -vE '\.md$' | while read -r file; do
                [ -f "$file" ] || continue
                # Filtrar cambios significativos
                git show "$commit" -- "$file" | \
                    awk '!/^[ \t]*($|#|\/{2})/ && !/^\/\*/,/\*\// {print}' | \
                    wc -l | awk '{print $1}'
            done
        done | awk '{add += $1} END {printf "    - Líneas significativas agregadas: %s\n", add}' | tee -a "$output_file"
        
        echo "" | tee -a "$output_file"
    done <<< "$authors"
    
    # Mostrar contribución porcentual por autor
    echo "Contribución porcentual por autor (basado en líneas netas):" | tee -a "$output_file"
    while read -r i; do
        read -r _ _ user_loc <<< "${user_totals["$i"]}"
        pct_total_loc=0
        if [ $total_loc -gt 0 ]; then
            pct_total_loc=$(echo "scale=2; $user_loc * 100 / $total_loc" | bc)
        fi
        echo "  - $i: $pct_total_loc%" | tee -a "$output_file"
    done <<< "$authors"   
    # Mostrar resumen global del repositorio
    echo ""
    echo "Resumen global del repositorio:" | tee -a "$output_file"
    echo "  - Total líneas agregadas: $total_added" | tee -a "$output_file"
    echo "  - Total líneas eliminadas: $total_subs" | tee -a "$output_file"
    echo "  - Total líneas netas: $total_loc" | tee -a "$output_file"
    echo "" | tee -a "$output_file"
    
    echo "Informe generado en: $output_file"
    echo ""
    cd - >/dev/null || return
}

# Preparar directorio de salida
prepare_output_dir


# Buscar repositorios git en subcarpetas
find . -type d -name ".git" -exec dirname {} \; | while read -r repo; do
    analyze_repo "$repo"
done

echo "Proceso completado. Todos los informes se han guardado en la carpeta $OUTPUT_DIR/"
