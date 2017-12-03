# pi-xmas-tree
Web control for the PiHut 3D Xmas Tree

https://thepihut.com/products/3d-xmas-tree-for-raspberry-pi

## Architecture

This project needs three layers:

* Pi with GPIO and attached Xmas tree, it will poll from the web backend.
* Pi (same or other) with attached RasPiCam, streaming to YouTube
* Any server (same Pi or other device) which serves as the web backend.
* Any server (same Pi or other device) which serves the frontend.

## Installation

Prerequisites:

The Raspberry Pi(s) needs the following packages:

* gpiozero
* python-tornado
* av-tools

Tornado is the web framework used by the two programs:

* xmas-client.py
* xmas-web.py

The xmas-client.py serves as the part that interfaces both with the Xmas tree 
via GPIO and also via http with the web backend. 

The backend is implemented via xmas-web.py and stores the LED state in memory.
It can run on the same pi, or on some other server in the internet. The URL
to this server needs to be configured in xmas-client.py.

We also need a Pi with a RasPiCam. There you will need to run the script youtube.sh.

The only parameter to this script is the private YouTube streaming key. See this link 
for details on YouTube streaming:

http://www.makeuseof.com/tag/live-stream-youtube-raspberry-pi/

The frontend needs to be deployed ... TBD.
