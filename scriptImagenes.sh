#!/bin/bash
for file in *.png
do 
  convert  -fill white -fuzz 75% +opaque "#000000" -brightness-contrast -70x100 "$file" "procesado/$file"
done
