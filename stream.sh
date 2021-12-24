#!/bin/bash

if [ $# -eq 0 ]
then
  echo -n "Streaming key: "
  read -s streamingkey
  echo
else
  streamingkey=$1
fi

# Pick one of the two URLs below: twitch or youtube
URL="rtmp://live.twitch.tv/app/${streamingkey}"
#URL="rtmp://a.rtmp.youtube.com/live2/${streamingkey}"

raspivid -o - -awb auto -t 0 -vf -hf -fps 30 -b 1000000 |  \
ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 \
-i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k \
-g 50 -strict experimental -f flv "${URL}"
