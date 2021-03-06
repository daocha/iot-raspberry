'''
/*
 * Actions triggered by sensor detection
 */
 '''

from awsiot.mqtt.shadow.shadowDeltaListener import ShadowDelta
from awsiot.mqtt.shadow.shadowGet import ShadowCall
from awsiot.mqtt.shadow.shadowUpdater import ShadowUpdater
from awsiot.mqtt.topic.topicSubscriber import TopicSubscriber
from actions.devices.rpi2 import RPi2
from actions.devices.pc import PC

import configparser
import project

global device
device = None

class Action:
    
    @staticmethod
    def updateThing(update_json, callbackFn = None):
        print("Updating iot state: ", update_json)
        shadowUpdater = ShadowUpdater()
        shadowUpdater.updateAWSThing(update_json, callbackFn)
    
    @staticmethod
    def listenDelta():
        print("Listening iot state delta...")
        shadowDelta = ShadowDelta()
        shadowDelta.listenDelta()
    
    @staticmethod
    def getThingState():
        print("Retrieving thing's state...")
        shadowCall = ShadowCall()
        return shadowCall.call()

    @staticmethod
    def subscribeTopic(topic, isMaster = False, callbackFn = None):
        print("Subscribing Topic: ", topic)
        topicSub = TopicSubscriber()
        topicSub.subscribeTopic(topic, isMaster, callbackFn)
        
    @staticmethod
    def onMessage(message):
        config = configparser.ConfigParser()
        rootpath = project.getProjectPath()
        config.read(rootpath + 'config/aws.properties')
        deviceName = config['DevicecConfig']['deviceName']
        
        global device
        if device is None and deviceName == "pi2":
            device = RPi2()
        elif device is None and deviceName == "pc":
            device = PC()
        
        if device is not None:
            device.onMessage(message.topic, message.payload)
        

#Action.updateThing(True, None)