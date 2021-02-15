#!/usr/bin/env bash

ffmpeg -vcodec mjpeg -i image-1-480x320.jpg -vcodec rawvideo -f rawvideo -pix_fmt rgb565 - > /dev/fb1