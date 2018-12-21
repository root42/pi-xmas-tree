#!/usr/bin/env python

import sys
import json
import tornado.ioloop
import tornado.web

class JsonHandler( tornado.web.RequestHandler ):
    """Request handler where requests and responses speak JSON."""
    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                print "Request: %s " % self.request.body
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request

        # Set up response dictionary.
        self.response = dict()
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'PUT, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')
        self.set_header('Accept:', 'application/json')

    def options(self, arguments):
        # no body
        self.set_status(204)
        self.finish()

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        # print "Response: %s" % self.response
        output = json.dumps(self.response)
        print "Response: %s" % output
        self.write(output)

class MainHandler(tornado.web.RequestHandler):
    def get( self, filename ):
        if len( filename ) == 0:
            filename = "index.html"
        if filename == "index.html" or filename == "xmas.js":
            with open( filename, "r" ) as indexFile:
                map( self.write, indexFile )
        else:
            self.write( "404 - file not found: %s" % filename )
            self.set_status(404)
            self.finish()

class LedHandler( JsonHandler ):

    tree = [ { "index" : i, "value" : 0.0 } for i in range(0, 26) ]

    def initialize( self ):
        print "leds: %i" % len( LedHandler.tree )

    def get( self, ledIndex=None ):
        if ledIndex == None or len( ledIndex ) == 0:
            self.response[ 'leds' ] = LedHandler.tree
        else:
            led = LedHandler.tree[ int( ledIndex ) ]
            self.response = led
        self.write_json()

    def put( self, ledIndex ):
        if ledIndex == None or len( ledIndex ) == 0:
            LedHandler.tree = self.request.arguments[ 'leds' ]
            self.response[ 'leds' ] = LedHandler.tree
        else:
            led = LedHandler.tree[ int( ledIndex ) ]
            led[ "value" ] = float( self.request.arguments[ 'value' ] )
            self.response[ 'value' ] = str( led[ "value" ] )
        self.write_json()
        
def make_app():
    return tornado.web.Application([
        (r"/led/(.*)", LedHandler),
        (r"/(.*)", MainHandler)
    ])

if __name__ == "__main__":
    port = 8888
    if len( sys.argv ) > 1:
        port = int( sys.argv[ 1 ] )
    app = make_app()
    app.listen( port )
    tornado.ioloop.IOLoop.current().start()
