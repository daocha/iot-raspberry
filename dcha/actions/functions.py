'''
/*
 * Actions triggered by sensor detection
 */
 '''

from awsiot.mqtt.shadow.shadowDeltaListener import ShadowDelta
from awsiot.mqtt.shadow.shadowGet import ShadowCall
from awsiot.mqtt.shadow.shadowUpdater import ShadowUpdater
from awsiot.mqtt.topic.topicSubscriber import TopicSubscriber


class Action:
    @staticmethod
    def updateThing(update_json):
        print("Updating iot state: ", update_json)
        shadowUpdater = ShadowUpdater()
        shadowUpdater.updateAWSThing(update_json)
    
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
    def subscribeTopic(topic):
        print("Subscribing Topic: ", topic)
        topicSub = TopicSubscriber()
        topicSub.subscribeTopic(topic)

#Action.updateThing(True, None)