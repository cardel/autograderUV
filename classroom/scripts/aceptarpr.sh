
#!/bin/bash

# Verificar dependencias
command -v gh >/dev/null 2>&1 || { echo "Error: GitHub CLI (gh) no está instalado"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "Error: jq no está instalado"; exit 1; }

# Verificar archivo de repos
if [ ! -f "repo.txt" ]; then
    echo "Error: Archivo repo.txt no encontrado"
    exit 1
fi

# Procesar cada repositorio
while read -r repo_url; do
    # Extraer owner/repo
    owner_repo=$(echo "$repo_url" | sed 's|https://github.com/||')

    echo "Procesando: $owner_repo"

    # Obtener PRs abiertos
    pr_numbers=$(gh pr list -R "$owner_repo" --json number -q '.[].number' 2>/dev/null)

    if [ -z "$pr_numbers" ]; then
        echo "No hay pull requests abiertos"
        continue
    fi

    # Aprobar y mergear cada PR
    for pr_num in $pr_numbers; do
        echo "Merging PR #$pr_num (Classroom Sync)"

        # Mergear sin borrar rama (que no existe)
        gh pr merge "$pr_num" -R "$owner_repo" \
            --merge \
            --subject "Merge automático: Sync Assignment" \
            <<< "y"

        # Esperar entre operaciones
        sleep 1
    done

    echo "--------------------------------------"
done < repo.txt

echo "Proceso completado para todos los repositorios"
