# coding: utf-8
import BaseHTTPServer
import sys
import os

# Request handler for serving the config profile:
class ConfigProfileHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    config = None
    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-Type', 'application/x-apple-aspen-config')
        s.end_headers()
        plist_string = plistlib.writePlistToString(ConfigProfileHandler.config)
        s.wfile.write(plist_string)
    def log_message(self, format, *args):
        
         pass

def run_server(config):
    ConfigProfileHandler.config = config
    server_address = ('', 0)
    httpd = BaseHTTPServer.HTTPServer(server_address, ConfigProfileHandler)
    sa = httpd.socket.getsockname()
    # Point Safari to the local http server:
    print 'http://localhost:'+sa
    # Handle a single request, then stop the server:
    httpd.handle_request()