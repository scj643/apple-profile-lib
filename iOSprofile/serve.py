# coding: utf-8
# parts by OMZ
import sys
import os
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import plistlib
import socket
if sys.version_info[0] >= 3:
    plistlib.writePlistToString = plistlib.writePlistToBytes
# Request handler for serving the config profile:
class ConfigProfileHandler (BaseHTTPRequestHandler):
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
    httpd = HTTPServer(server_address, ConfigProfileHandler)
    sa = httpd.socket.getsockname()
    # Point Safari to the local http server:
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        try:
            ip = socket.gethostbyname(socket.getfqdn()+'.local')
        except socket.gaierror:
            ip = '127.0.0.1'
    print(('http://')+ip+':'+str(sa[1]))
    print(sa)
    # Handle a single request, then stop the server:
    httpd.handle_request()
