#!/bin/bash

# Definir carpetas
folders=("ParcialA" "ParcialB" "ParcialC" "ParcialD")

# Recorre cada carpeta
for folder in "${folders[@]}"; do
  # Elimina los archivos ParcialX.tex, mapeo.txt y archivos PDF
  rm -f "${folder}/Parcial*.tex"
  rm -f "${folder}/mapeo.txt"
  rm -f "${folder}/*.pdf"

  # Puedes agregar otros patrones de archivos a limpiar si es necesario, por ejemplo:
  # rm -f "${folder}/*.aux" "${folder}/*.log" "${folder}/*.out"

  echo "Archivos en ${folder} eliminados."
done

echo "Limpieza completada."

