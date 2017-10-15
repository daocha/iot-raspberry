from awsiot.shadow.shadowUpdater import ShadowUpdater

class Action:
    @staticmethod
    def updateThing(lightOn, shocking):
        print("Updating iot state")
        updater = ShadowUpdater()
        updater.updateAWSThing(lightOn, shocking)

#Action.updateThing(True, None)