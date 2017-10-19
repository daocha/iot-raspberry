from http.server import BaseHTTPRequestHandler, HTTPServer
from actions.functions import Action as act

 
# HTTPRequestHandler class
class AWSShadowCheck(BaseHTTPRequestHandler):
    
    # GET
    def do_GET(self):
        
        output = act.getThingState()
        
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Write content as utf-8 data
        self.wfile.write(bytes(output, "utf8"))
        return
 
def run():
    print('starting server...')
 
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, AWSShadowCheck)
    print('running server...')
    httpd.serve_forever()
