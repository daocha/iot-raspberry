
import json
from .device import Device
from interface import implements

class RPi2(implements(Device)):
    
    lightOn = False
    backingUp = False
    
    def toggleLight(self, enable):
        
        if not self.lightOn:
            if enable:
                print("*********** Turning on light...")
            else:
                print("*********** Turning off light...")
        else:
            print("*********** Light is already on....")
        self.lightOn = enable
        
    def startBackup(self):
        if not self.backingUp:
            print("Start backing up data...")
        else:
            print("*********** Backup is in progress...")
        self.backingUp = True
        
    def onMessage(self, topic, payload):
        payloadDict = json.loads(payload)
        state = payloadDict["state"]
        if state is not None:
            if state["light"] is not None and state["light"] == '1':
                self.toggleLight(True)
            elif state["light"] is not None and state["light"] == '0':
                self.toggleLight(False)
                
            if state["backup"] is not None and state["backup"] == '1':
                self.startBackup()