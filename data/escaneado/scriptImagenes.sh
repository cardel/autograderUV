#!/bin/bash
for file in *.jpg; do
  #convert  -fill white -fuzz 80% +opaque "#000000" -brightness-contrast -70x100 "$file" "../procesado/$file"
  magick "$file" -colorspace Gray -evaluate-sequence Max -threshold 80% "../procesado/$file"
done
