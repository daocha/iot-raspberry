'''
/*
 * Actions triggered by sensor detection
 */
 '''

from awsiot.shadow.shadowUpdater import ShadowUpdater
from awsiot.shadow.shadowDeltaListener import ShadowDelta
from awsiot.shadow.shadowGet import ShadowCall

class Action:
    @staticmethod
    def updateThing(update_json):
        print("Updating iot state: ", update_json)
        shadowUpdater = ShadowUpdater
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

#Action.updateThing(True, None)