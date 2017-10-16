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
        updater = ShadowUpdater()
        updater.updateAWSThing(lightOn, shocking)
    
    @staticmethod
    def listenDelta():
        print("Listening iot state delta...")
        delta = ShadowDelta()
        delta.listenDelta()

#Action.updateThing(True, None)