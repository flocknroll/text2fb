#!/usr/bin/env bash

magick convert -flip -resize 480x320\! -define bmp:subtype=RGB565 magick:ROSE bmp:- | tail -c 307200 > /dev/fb1

magick convert -font Inconsolata-Regular -background black -fill red -gravity center -size 480x320 label:`date +%H:%M` png:- \
    | ffmpeg -vcodec png -i - -vcodec rawvideo -f rawvideo -pix_fmt rgb565 - > /dev/fb1

magick convert -font Inconsolata-Regular -background black -fill red -gravity center -size 120x80 label:`date +%H:%M` png:- \
    | ffmpeg -vcodec png -i - -vf scale=480:320 -sws_flags neighbor -vcodec rawvideo -f rawvideo -pix_fmt rgb565 - > /dev/fb1
