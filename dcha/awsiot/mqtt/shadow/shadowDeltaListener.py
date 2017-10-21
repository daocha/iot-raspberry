'''
/*
 * Connect AWS IoT to list shadow's delta states
 */
 '''
import json

from awsiot.mqtt import mqttUtils


class ShadowDelta:

    # Shadow JSON schema:
    #
    # Name: Bot
    # {
    # 	"state": {
    # 		"desired":{
    # 			"property":<INT VALUE>
    # 		}
    # 	}
    # }
    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        print(responseStatus)
        payloadDict = json.loads(payload)
        print("++++++++DELTA++++++++++")
        print("lightOn: " + str(payloadDict["state"]["lightOn"]))
        print("shocking: " + str(payloadDict["state"]["shocking"]))
        print("motion: " + str(payloadDict["state"]["motion"]))
        print("version: " + str(payloadDict["version"]))
        print("+++++++++++++++++++++++\n\n")
    
    def listenDelta(self):
        thingName = mqttUtils.getDefaultThingName()
        
        myAWSIoTMQTTShadowClient = mqttUtils.createMQTTShadowClient()
        
        if myAWSIoTMQTTShadowClient is None:
            return
        
        # Connect to AWS IoT
        myAWSIoTMQTTShadowClient.connect()
        
        # Create a deviceShadow with persistent subscription
        deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
        
        # Listen on deltas
        deviceShadowHandler.shadowRegisterDeltaCallback(self.customShadowCallback_Delta)
        
        myAWSIoTMQTTShadowClient.disconnect()
        
        # Loop forever
        #while True:
        #    time.sleep(1)
