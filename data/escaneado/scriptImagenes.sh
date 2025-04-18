#!/bin/bash

mkdir -p "../procesado"

for file in *.jpg; do
	magick "$file" \
		-colorspace Gray \
		-adaptive-sharpen 0x1 \
		-contrast-stretch 1% \
		-blur 0x0.5 \
		-threshold 80% \
		-morphology Close Diamond:1 \
		"../procesado/$file"
done
