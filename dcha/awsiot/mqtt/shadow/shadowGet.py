import json
import time

from awsiot.mqtt import mqttUtils


class ShadowCall:
    
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
                self.shadowResult += "bright: " + str(payloadDict["state"]["desired"]["brt"]) + "<br />"
            except:
                self.shadowResult += ''
                
            try:
                self.shadowResult += "shocking: " + str(payloadDict["state"]["desired"]["shk"]) + "<br />"
            except:
                pass
            
            try:
                self.shadowResult += "motion: " + str(payloadDict["state"]["desired"]["mot"]) + "<br />"
            except:
                pass
                
            self.shadowResult += "<hr><br />"
        if responseStatus == "rejected":
            self.shadowResult += "Get request " + token + " rejected!"
            
    def call(self):
        thingName = mqttUtils.getDefaultThingName()
        
        myAWSIoTMQTTShadowClient = mqttUtils.createMQTTShadowClient()
        
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
        
        return output