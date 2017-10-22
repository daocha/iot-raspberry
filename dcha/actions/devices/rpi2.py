
import json
from .device import Device
from interface import implements

class RPi2(implements(Device)):
    
    lightOn = False
    backingUp = False
    
    def toggleLight(self, enable):
        
        if self.lightOn ^ enable:
            if enable:
                print("*********** Turning on light...")
            else:
                print("*********** Turning off light...")
        else:
            if self.lightOn:
                print("*********** Light is already on....")
            else:
                print("*********** Light is already off....")
        self.lightOn = enable
        
    def startBackup(self):
        if not self.backingUp:
            print("Start backing up data...")
        else:
            print("*********** Backup is in progress...")
        self.backingUp = True
        
    def onMessage(self, topic, payload):
        
        print("Received a new message: ")
        print(payload)
        print("from topic: ")
        print(topic)
        print("--------------\n\n")
        
        payloadDict = json.loads(payload)
        state = payloadDict["state"]
        if state is not None:
            if "light" in state and state["light"] == '1':
                self.toggleLight(True)
            elif "light" in state and state["light"] == '0':
                self.toggleLight(False)
                
            if "backup" in state and state["backup"] == '1':
                self.startBackup()
                
                