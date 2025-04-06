#!/bin/bash

# Definir carpetas y preguntas
folders=("ParcialA" "ParcialB" "ParcialC" "ParcialD")
questions=($(seq 1 20)) # Preguntas
num_questions=10        # Cantidad de preguntas por parcial

code_questions=($(seq 1 10))
code_num_questions=5

# Recorre cada carpeta
for folder in "${folders[@]}"; do
  # Obtener la letra correspondiente a cada parcial
  letter=${folder: -1}

  # Generar archivo ParcialX.tex y agregar el contenido de EnunciadoX.tex
  enunciado_file="${folder}/Enunciado${letter}.tex"
  output_file="${folder}/Parcial${letter}.tex"
  mapeo_file="${folder}/mapeo.txt"

  # Comienza copiando el contenido del enunciado
  cat "$enunciado_file" >"$output_file"

  # Generar una lista aleatoria de preguntas sin repetición
  shuffled_questions=($(shuf -e "${questions[@]}"))

  # Agregar la lista de preguntas al archivo de salida y registrar el mapeo
  echo "\\begin{enumerate}" >>"$output_file"
  # Generar un contador para el ciclo
  counter=0
  for i in "${!shuffled_questions[@]}"; do
    question_number="${shuffled_questions[$i]}"
    # Incrementar el contador
    counter=$((counter + 1))
    echo "\\item \\input{../Generador/pregunta${question_number}.tex}" >>"$output_file"
    #Cuando se han alcanzado las num_questions preguntas se detiene el ciclo
    if [ $counter -eq $num_questions ]; then
      break
    fi
  done
  echo "\\end{enumerate}" >>"$output_file"

  #Incluir preguntas código
  echo "\\input{../Generador/EnunciadoCodigo.tex}" >>"$output_file"
  echo "\\begin{enumerate}" >>"$output_file"
  echo "\\setcounter{enumi}{$((num_questions))}" >>"$output_file"
  code_shuffled_questions=($(shuf -e "${code_questions[@]}"))
  counter=0

  for i in "${!code_shuffled_questions[@]}"; do
    question_number="${code_shuffled_questions[$i]}"
    # Incrementar el contador
    counter=$((counter + 1))
    echo "\\item \\input{../Generador/preguntaCodigo${question_number}.tex}" >>"$output_file"
    #Cuando se han alcanzado las code_num_questions preguntas se detiene el ciclo
    if [ $counter -eq $code_num_questions ]; then
      break
    fi
  done
  echo "\\end{enumerate}" >>"$output_file"
  echo "\\end{document}" >>"$output_file"

  # Guardar la lista de preguntas en el archivo mapeo.txt
  echo "${shuffled_questions[*]}" >"$mapeo_file"
  echo "${code_shuffled_questions[*]}" >>"$mapeo_file"
done

echo "Archivos generados exitosamente."
