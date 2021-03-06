'''
/*
 * Connect AWS IoT to update shadow document
 */
 '''
import json

from awsiot.mqtt import mqttUtils


class ShadowUpdater:

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
    def customShadowCallback_Update(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
            
            for key, value in payloadDict.items():
                print("[", key, "] = ", value)
                
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")
    
    def customShadowCallback_Delete(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Delete request " + token + " time out!")
        if responseStatus == "accepted":
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Delete request with token: " + token + " accepted!")
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Delete request " + token + " rejected!")
    
    def updateAWSThing(self, update_json, callbackFn = None):
        thingName = mqttUtils.getDefaultThingName()
        
        myAWSIoTMQTTShadowClient = mqttUtils.createMQTTShadowClient()
        
        if myAWSIoTMQTTShadowClient is None:
            return
        
        # Connect to AWS IoT
        myAWSIoTMQTTShadowClient.connect()
        
        # Create a deviceShadow with persistent subscription
        deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
        
        # Delete shadow JSON doc
        #deviceShadowHandler.shadowDelete(self.customShadowCallback_Delete, 5)
        
        # Update shadow 
        JSONPayload = '{"state":{"desired":' + update_json + '}}'
        #print('Shadow State: \n', JSONPayload)
        deviceShadowHandler.shadowUpdate(JSONPayload, callbackFn, 5)

#updater = ShadowUpdater()
#updater.updateAWSThing(None, 'True')
