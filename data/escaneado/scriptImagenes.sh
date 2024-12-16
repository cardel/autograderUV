#!/bin/bash

# Crear el directorio de salida si no existe
mkdir -p "../procesado"

# Procesar cada archivo .jpg
for file in *.jpg; do
  magick "$file" \
    -colorspace Gray \
    -blur 0x2 \
    -level 30%,90% \
    -threshold 70% \
    "../procesado/$file"
done
