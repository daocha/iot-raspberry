'''
/*
 * Actions triggered by sensor detection
 */
 '''

from awsiot.shadow.shadowUpdater import ShadowUpdater
from awsiot.shadow.shadowDeltaListener import ShadowDelta

class Action:
    @staticmethod
    def updateThing(update_json):
        print("Updating iot state: ", update_json)
        ShadowUpdater.updateAWSThing(update_json)
    
    @staticmethod
    def listenDelta():
        print("Listening iot state delta...")
        ShadowDelta.listenDelta()

#Action.updateThing(True, None)