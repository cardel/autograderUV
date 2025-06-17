#!/bin/bash

# Nombre del archivo de salida
output_file="reporte_commits.txt"

# Eliminar el archivo existente si lo hubiera
> "$output_file"

# Buscar carpetas y procesar repositorios git
for carpeta in */; do
    # Eliminar la barra del final del nombre
    nombre=${carpeta%/}
    
    if [ -d "$carpeta/.git" ]; then
        echo "Procesando: $nombre"
        (
            cd "$carpeta"
            fecha_commit=$(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M' 2>/dev/null)

            
            if [ -n "$fecha_commit" ]; then
                echo "$nombre $fecha_commit" >> "../$output_file"
            else
                echo "  -> No se encontraron commits"
            fi
        )
    else
        echo "Omitiendo: $nombre (no es un repo git)"
    fi
done

echo "¡Reporte generado en $output_file!"
