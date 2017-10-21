
import json
from .device import Device
from interface import implements

class PC(implements(Device)):
    
    def startBackup(self):
        print("Start backing up data...")
        
    def onMessage(self, topic, payload):
        payloadDict = json.loads(payload)
        
        if payloadDict["backup"] is not None and payloadDict["backup"] == 'on':
            self.startBackup()