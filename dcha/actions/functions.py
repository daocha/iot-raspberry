'''
/*
 * Actions triggered by sensor detection
 */
 '''

from awsiot.shadow.shadowUpdater import ShadowUpdater
from awsiot.shadow.shadowDeltaListener import ShadowDelta

class Action:
    @staticmethod
    def updateThing(lightOn, shocking):
        print("Updating iot state...")
        ShadowUpdater.updateAWSThing(lightOn, shocking)
    
    @staticmethod
    def listenDelta():
        print("Listening iot state delta...")
        ShadowDelta.listenDelta()

#Action.updateThing(True, None)