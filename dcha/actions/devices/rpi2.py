
import json
from .device import Device
from interface import implements

class RPi2(implements(Device)):
    def toggleLight(self, enable):
        if enable:
            print("Turning on light")
        else:
            print("Turning off light")
        
    def startBackup(self):
        print("Start backing up data...")
        
    def onMessage(self, topic, payload):
        payloadDict = json.loads(payload)
        
        if payloadDict["light"] is not None and payloadDict["light"] == '1':
            self.toggleLight(True)
        elif payloadDict["light"] is not None and payloadDict["light"] == '0':
            self.toggleLight(False)
            
        if payloadDict["backup"] is not None and payloadDict["backup"] == '1':
            self.startBackup()