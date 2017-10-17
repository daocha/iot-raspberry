'''
/*
 * Listener Raspberry Pi GPIO
 * <p>
 * Push to AWS IoT 
 */
 '''

import _thread
import time
import sys,traceback
from actions.functions import Action as act



print("initializing...")

global lighton, lighton_new, shocking, shocking_new
lighton = False
lighton_new = True
shocking = False
shocking_new = True


def status_checking():
    print("status checking...")
    global lighton, lighton_new, shocking, shocking_new
    lighton_new = not lighton_new
    shocking_new = not shocking_new
    
    update = False
    
    if lighton ^ lighton_new:
        update = True
        lighton = lighton_new
        
    if shocking ^ shocking_new:
        update = True
        shocking = shocking_new
        
    if update:
        act.updateThing(str(lighton_new), str(shocking_new))

def loop_status_checking(threadName):
    while True:
        print(threadName)
        status_checking()
        time.sleep(10)

def loop_delta_listening(threadName):
    while True:
        print(threadName)
        act.listenDelta()
        time.sleep(10)

def main():
    try:
        print("adding event listeners")
        
        try:
            _thread.start_new_thread(loop_delta_listening, ('[Thread-Delta-Listening]',))
            _thread.start_new_thread(loop_status_checking, ('[Thread-Status-Checking]',))
        except: 
            print("Error: unable to start thread")
            traceback.print_exc(file=sys.stdout)
        
        while True:
            pass
        
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
