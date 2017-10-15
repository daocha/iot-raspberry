from dcha.awsiot.shadow.basicShadowUpdater import

from dcha.awsiot.shadow import shadowUpdater

class Action:
    @staticmethod
    def updateThing(lightOn, shocking):
        print("Updating iot state")
        shadowUpdater(lightOn, shocking)