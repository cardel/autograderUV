#!/bin/bash

# Define el nombre del archivo de salida
output_file="ParcialTotal.pdf"

# Busca todos los archivos PDF dentro de la carpeta raíz y subdirectorios, excluyendo ParcialGenerico
pdf_files=$(find . -name "*.pdf" ! -path "./ParcialGenerico/*" | sort)

# Verifica si se encontraron archivos PDF
if [ -z "$pdf_files" ]; then
  echo "No se encontraron archivos PDF para fusionar."
  exit 1
fi

# Crea una cadena con los nombres de archivo PDF para pasar a Ghostscript
pdf_files_string=""
for file in $pdf_files; do
  pdf_files_string+=" $file"
done

# Ejecuta Ghostscript para fusionar los archivos PDF
gs -sPAPERSIZE=letter \
  -sDEVICE=pdfwrite \
  -dPDFSETTINGS=/prepress \
  -dEmbedAllFonts=true \
  -dCompatibilityLevel="1.4" \
  -dNOPAUSE \
  -dBATCH \
  -dSAFER \
  -sOutputFile="$output_file" \
  $pdf_files_string

echo "Archivos PDF fusionados correctamente en $output_file."
