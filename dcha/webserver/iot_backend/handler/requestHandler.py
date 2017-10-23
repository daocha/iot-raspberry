from django.http import HttpResponse
import json
import time
from actions.functions import Action as act


class ControlRequest:
    
    timeout = 5
    
    update_result = None

    def controlRequest_callback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
                
            for key, value in payloadDict.items():
                print("[", key, "] = ", value)
                    
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")
        
        if responseStatus == "accepted":
            self.update_result = {"success":"1"}
        else:
            self.update_result = {"success":"0"}
    
    @staticmethod
    def controlRequest(request):
        
        controlReq = ControlRequest()
        
        req_json = json.loads(request.body.decode('utf8'))
        
        control = req_json["control"]
        
        print(control)
        
        if control is not None:
            if "light" in control:
                update_json = {"lgt": control["light"]}
                
            if "backup" in control:
                update_json = {"bak": control["backup"]}
                
            act.updateThing(json.dumps(update_json), controlReq.controlRequest_callback)
            
            startTime = time.time()
            
            while True:
                currentTime = time.time()
                
                timediff = currentTime - startTime
                
                if(timediff > controlReq.timeout):
                    print("AWS IoT shadow update request timed out")
                    break
                
                if controlReq.update_result is not None:
                    print("Result: ", controlReq.update_result)
                    return HttpResponse(json.dumps(controlReq.update_result))
                
                time.sleep(0.5)
            
            return HttpResponse("{'success':'0'}")
        else:
            return HttpResponse("{'success':'0'}")