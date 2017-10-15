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

import configparser
import json
import logging
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import project

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
        print("version: " + str(payloadDict["version"]))
        print("+++++++++++++++++++++++\n\n")
        
    def listenDelta(self):
        config = configparser.ConfigParser()
        rootpath = project.getProjectPath()
        config.read(rootpath + 'config/aws.properties')
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
        logger.setLevel(logging.ERROR)
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
        
        # Listen on deltas
        deviceShadowHandler.shadowRegisterDeltaCallback(self.customShadowCallback_Delta)
        
        # Loop forever
        while True:
            time.sleep(1)
