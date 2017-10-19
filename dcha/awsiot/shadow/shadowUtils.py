'''
/*
 * create generic shadow client connecting to AWS
 */
 '''
 
import configparser
import project
import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

def getDefaultThingName():
        config = configparser.ConfigParser()
        rootpath = project.getProjectPath()
        config.read(rootpath + 'config/aws.properties')
        thingName = config['AWSConfig']['thingName']
        return thingName

def createShadowClient():
        config = configparser.ConfigParser()
        rootpath = project.getProjectPath()
        config.read(rootpath + 'config/aws.properties')
        host = config['AWSConfig']['endpoint']
        rootCAPath = rootpath + config['AWSConfig']['rootCA']
        certificatePath = rootpath + config['AWSConfig']['cert']
        privateKeyPath = rootpath + config['AWSConfig']['privateKey']
        useWebsocket = config['AWSConfig']['useWebsocket'] == 'True'
        connectAWS = config['AWSConfig']['connectAWS'] == 'True'
        clientId = config['AWSConfig']['clientId']
        
        if not connectAWS:
            print("Connecting AWS is turned off. Aborting...")
            return None
        
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
        
        return myAWSIoTMQTTShadowClient