#!/usr/bin/env python

import sys
from gpiozero import LEDBoard, PWMLED
from gpiozero.tools import random_values
from signal import pause
import json
import tornado.httpclient
import tornado.ioloop
import tornado.web
import datetime

def ts():
    st = str(datetime.datetime.utcnow())
    return "[%s] " % st

tree = LEDBoard( *list(range(2,28)), pwm=True )
old_tree = [ 0.0 for i in range( 0, 26 ) ]

url = "http://localhost:8888/led/" # change this to your host which serves the backend

def getLedStatus():
    http_client = tornado.httpclient.HTTPClient()
    try:
        response = http_client.fetch( url )
        json_data = json.loads( response.body )
        for led in json_data[ "leds" ]:
            value = float( led[ "value" ] )
            index = int( led[ "index" ] )
            if old_tree[ index ] != value:
                print(ts() + "Setting led %u to %f" % (index, value))
                tree[ index ].value = value
                old_tree[ index ] = value
    except tornado.httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        print(( ts() + "Error: " + str(e)))
    except Exception as e:
        # Other errors are possible, such as IOError.
        print(( ts() + "Error: " + str(e)))
    http_client.close()

if __name__ == "__main__":
    if len( sys.argv ) > 1:
        url = sys.argv[ 1 ]
    print("leds: %i" % len(tree))
    tornado.ioloop.PeriodicCallback( getLedStatus, 500 ).start()
    tornado.ioloop.IOLoop.instance().start()
