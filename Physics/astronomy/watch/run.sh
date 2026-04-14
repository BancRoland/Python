#!/bin/bash

## FOR TH PICTURES
# mkdir pics
# python3 picgen.py

## FOR THE NAIVE SOLUTION (COLORS ARE OFF)
# ffmpeg -pattern_type glob -i 'Budapest_23/*.png' video0.gif

# cd Budapest_23

# for f in watchface_*_Budapest.png; do
#   n=$(echo "$f" | sed -E 's/.*_([0-9]+)_Budapest\.png/\1/')
#   printf "mv %q %q\n" "$f" "$(printf "watchface_%03d_Budapest.png" "$n")"
#   mv "$f" "$(printf "watchface_%03d_Budapest.png" "$n")"
# done

## FOR COLOR CORRECTION WE USE PALETTE
ffmpeg -pattern_type glob -i 'Budapest_23/*.png' -vf palettegen palette.png
ffmpeg -pattern_type glob -i 'Budapest_23/*.png' -i palette.png -lavfi paletteuse video1.gif
# rm palette.png

# ffmpeg -framerate 5 -pattern_type glob -i 'Budapest_23/*.png' -i palette.png -lavfi paletteuse video2.gif
