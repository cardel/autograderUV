#!/bin/bash

# Archivo de entrada
input_file="todasPreguntas.tex"

# Contador de preguntas
count=1

# Usa awk para leer entre bloques que empiezan y terminan con { y }
awk '
/^{/ { in_block = 1; block = ""; }
/^}/ { in_block = 0; block = block $0; print block > "pregunta" count ".tex"; count++; }
/^{|^}/ { block = block $0 ORS; next; }
in_block { block = block $0 ORS; }
' count=$count "$input_file"

echo "Archivos de preguntas generados correctamente."
