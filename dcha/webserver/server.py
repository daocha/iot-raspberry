from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
from awsiot.shadow import shadowUtils as shadowUtils
 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    shadowResult = '' 
    
    def customShadowCallback_Get(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        if responseStatus == "timeout":
            self.shadowResult += "Get request " + token + " time out!<br />"
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            self.shadowResult += "<hr />"
            self.shadowResult += "Get request with token: " + token + " accepted!<br />"
            try:
                self.shadowResult += "lightOn: " + str(payloadDict["state"]["desired"]["lightOn"]) + "<br />"
            except:
                self.shadowResult += ''
                
            try:
                self.shadowResult += "shocking: " + str(payloadDict["state"]["desired"]["shocking"]) + "<br />"
            except:
                pass
            
            try:
                self.shadowResult += "motion: " + str(payloadDict["state"]["desired"]["motion"]) + "<br />"
            except:
                pass
                
            self.shadowResult += "<hr><br />"
        if responseStatus == "rejected":
            self.shadowResult += "Get request " + token + " rejected!"
            
    # GET
    def do_GET(self):
        
        thingName = shadowUtils.getDefaultThingName()
        
        myAWSIoTMQTTShadowClient = shadowUtils.createShadowClient()
        
        if myAWSIoTMQTTShadowClient is not None:
            # Connect to AWS IoT
            myAWSIoTMQTTShadowClient.connect()
            
            # Create a deviceShadow with persistent subscription
            deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
            
            # Listen on deltas
            deviceShadowHandler.shadowGet(self.customShadowCallback_Get,5)
            
            time.sleep(5)
            
            output = self.shadowResult
            
            print(output)
        else:
            output = 'Connection to AWS is disabled'
        
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
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
