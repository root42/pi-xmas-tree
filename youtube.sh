#!/bin/bash

raspivid -o - -awb shade -t 0 -vf -hf -fps 30 -b 1000000 | avconv -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv "rtmp://a.rtmp.youtube.com/live2/$1"
