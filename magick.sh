#!/usr/bin/env bash

magick convert -flip -resize 480x320\! -define bmp:subtype=RGB565 magick:ROSE bmp:- | tail -c 307200 > /dev/fb1