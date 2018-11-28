#!/bin/bash

if [ $# -eq 0 ]
then
  echo -n "Streaming key: "
  read -s streamingkey
  echo
else
  streamingkey=$1
fi
raspivid -o - -awb shade -t 0 -vf -hf -fps 30 -b 1000000 |  \
avconv -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 \
-i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k \
-g 50 -strict experimental -f flv "rtmp://a.rtmp.youtube.com/live2/${streamingkey}"
