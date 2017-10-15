'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import json
import project
import configparser


# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
# }

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["desired"]["property"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")
        
def updateAWSThing(lighton, shocking):
    config = configparser.ConfigParser()
    rootpath = project.getProjectPath()
    config.read(rootpath + 'dcha/config/aws.properties')
    host = config['AWSConfig']['endpoint']
    rootCAPath = rootpath + config['AWSConfig']['rootCA']
    certificatePath = rootpath + config['AWSConfig']['cert']
    privateKeyPath = rootpath + config['AWSConfig']['privateKey']
    useWebsocket = config['AWSConfig']['useWebsocket'] == 'True'
    thingName = 'pi2-sensors'
    clientId = config['AWSConfig']['clientId']
    
    if useWebsocket and certificatePath and privateKeyPath:
        print("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)
    
    if not useWebsocket and (not certificatePath or not privateKeyPath):
        print("Missing credentials for authentication.")
        exit(2)
    
    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    
    # Init AWSIoTMQTTShadowClient
    myAWSIoTMQTTShadowClient = None
    if useWebsocket:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
        myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
        myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
        myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
        myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()
    
    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
    
    # Delete shadow JSON doc
    deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)
    
    # Update shadow 
    JSONPayload = '{"state":{"desired":{"lightOn":"' + lighton + '", "shocking":"' + shocking + '"}}}'
    print('Shadow State: \n', JSONPayload)
    deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

updateAWSThing('True','False')