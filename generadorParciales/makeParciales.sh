#!/bin/bash

# Recorre todas las carpetas que comienzan con "Parcial"
for dir in Parcial*; do
  if [ -d "$dir" ]; then
    echo "Entrando a la carpeta $dir"
    cd "$dir" || exit
    echo "Ejecutando make -B en $dir"
    make -B
    echo "Ejecutando make clean en $dir"
    make clean
    cd ..
    echo "Saliendo de la carpeta $dir"
  fi
done

