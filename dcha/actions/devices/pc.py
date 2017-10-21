
import json
from .device import Device
from interface import implements

class PC(implements(Device)):
    
    def startBackup(self):
        print("Start backing up data...")
        
    def onMessage(self, topic, payload):
        payloadDict = json.loads(payload)
        state = payloadDict["state"]
        if state is not None:
            if state["backup"] is not None and state["backup"] == 'on':
                self.startBackup()