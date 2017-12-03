#!/usr/bin/env python

import json
import tornado.ioloop
import tornado.web

tree = [ { "index" : i, "value" : 0.0 } for i in range(0, 26) ]

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
    def get(self):
        self.write( "Hello, world" )

class LedHandler( JsonHandler ):

    def get( self, ledIndex=None ):
        if ledIndex == None or len( ledIndex ) == 0:
            self.response[ 'leds' ] = tree
        else:
            led = tree[ int( ledIndex ) ]
            self.response = led
        self.write_json()

    def put( self, ledIndex ):
        led = tree[ int( ledIndex ) ]
        led[ "value" ] = float( self.request.arguments[ 'value' ] )
        self.response[ 'value' ] = str( led[ "value" ] )
        self.write_json()
        
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/led/(.*)", LedHandler)
    ])

if __name__ == "__main__":
    print "leds: %i" % len(tree)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
