'''
/*
 * Connect AWS IoT to list shadow's delta states
 */
 '''

import configparser
import json
import logging

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
        config = configparser.ConfigParser()
        rootpath = project.getProjectPath()
        config.read(rootpath + 'config/aws.properties')
        host = config['AWSConfig']['endpoint']
        rootCAPath = rootpath + config['AWSConfig']['rootCA']
        certificatePath = rootpath + config['AWSConfig']['cert']
        privateKeyPath = rootpath + config['AWSConfig']['privateKey']
        useWebsocket = config['AWSConfig']['useWebsocket'] == 'True'
        connectAWS = config['AWSConfig']['connectAWS'] == 'True'
        thingName = config['AWSConfig']['thingName']
        clientId = config['AWSConfig']['clientId']
        
        if not connectAWS:
            print("Connecting AWS is turned off. Aborting...")
            return
        
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
        deviceShadowHandler.shadowRegisterDeltaCallback(ShadowDelta.customShadowCallback_Delta)
        
        myAWSIoTMQTTShadowClient.disconnect()
        
        # Loop forever
        #while True:
        #    time.sleep(1)
