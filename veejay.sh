#!/bin/bash

while true; do
    ffmpeg -re -i "$(find -iname '*.mp4' | shuf -n 1)" -c copy -f flv rtmp://localhost:1935/stream/live
done
