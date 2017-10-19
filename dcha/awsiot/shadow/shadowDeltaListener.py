'''
/*
 * Connect AWS IoT to list shadow's delta states
 */
 '''
import json
from awsiot.shadow import shadowUtils as shadowUtils

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
    @staticmethod
    def customShadowCallback_Delta(payload, responseStatus, token):
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
    
    @staticmethod
    def listenDelta():
        thingName = shadowUtils.getDefaultThingName()
        
        myAWSIoTMQTTShadowClient = shadowUtils.createShadowClient()
        
        if myAWSIoTMQTTShadowClient is None:
            return
        
        # Connect to AWS IoT
        myAWSIoTMQTTShadowClient.connect()
        
        # Create a deviceShadow with persistent subscription
        deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
        
        # Listen on deltas
        deviceShadowHandler.shadowRegisterDeltaCallback(ShadowDelta.customShadowCallback_Delta)
        
        myAWSIoTMQTTShadowClient.disconnect()
        
        # Loop forever
        #while True:
        #    time.sleep(1)
