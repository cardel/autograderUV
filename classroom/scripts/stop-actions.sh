#!/bin/bash

# Verificar que el archivo existe
if [ ! -f "repo.txt" ]; then
    echo "Error: El archivo repo.txt no existe"
    exit 1
fi

# Leer cada repositorio del archivo
while read -r repo_url; do
    # Extraer owner y repo de la URL
    owner_repo=$(echo "$repo_url" | sed 's|https://github.com/||')
    
    echo "Cancelando workflows en: $owner_repo"
    
    # Obtener todos los workflow runs activos
    run_ids=$(gh run list -R "$owner_repo" --json databaseId -q '.[].databaseId' 2>/dev/null)
    
    if [ -z "$run_ids" ]; then
        echo "No se encontraron ejecuciones activas"
        continue
    fi
    
    # Cancelar cada ejecución
    for run_id in $run_ids; do
        echo "Cancelando ejecución ID: $run_id"
        gh run cancel "$run_id" -R "$owner_repo"
    done
    
    echo "--------------------------------------"
done < repo.txt

echo "Proceso completado"
