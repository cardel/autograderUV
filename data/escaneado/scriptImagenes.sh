#!/bin/bash

mkdir -p "../procesado"

for file in *.jpg; do
    magick "$file" \
        -colorspace Gray \
        -contrast-stretch 5%x5% \
        -deskew 80% \
        -threshold 75% \
        -fill white -draw "polygon 0,0 100,0 100,%[fx:h] 0,%[fx:h] 0,0 \
                           polygon %[fx:w-100],0 %[fx:w],0 %[fx:w],%[fx:h] %[fx:w-100],%[fx:h] %[fx:w-100],0 \
                           polygon 0,0 %[fx:w],0 %[fx:w],100 0,100 0,0 \
                           polygon 0,%[fx:h-100] %[fx:w],%[fx:h-100] %[fx:w],%[fx:h] 0,%[fx:h] 0,%[fx:h-100]" \
        -morphology Close Diamond:1 \
        -adaptive-sharpen 0x1.5 \
        "../procesado/$file"
done
