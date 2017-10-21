'''
/*
 * Listener Raspberry Pi GPIO
 * <p>
 * Push to AWS IoT 
 */
 '''

import _thread
import sys, traceback
import time

from actions.functions import Action as act


global lighton, lighton_new, shocking, shocking_new, motion, motion_new, shock_timer
lighton = False
lighton_new = False
shocking = False
shocking_new = False
motion = False
motion_new = False

def status_checking():
    print("status checking...")
    global lighton, lighton_new, shocking, shocking_new, motion, motion_new
    updating = False
    
    if lighton ^ lighton_new:
        updating = True
        lighton = lighton_new
    
    if motion ^ motion_new:
        updating = True
        motion = motion_new
        
    if shocking ^ shocking_new:
        updating = True
        shocking = shocking_new
        
    update_json = '{"lightOn":"' + str(lighton_new) 
    update_json += '", "shocking":"' + str(shocking_new) 
    update_json += '", "motion":"' + str(motion_new) + '"}'
        
    if updating:
        act.updateThing(update_json)

def loop_status_checking(threadName):
    while True:
        print(threadName)
        status_checking()
        time.sleep(15)

def loop_delta_listening(threadName):
    while True:
        print(threadName)
        act.listenDelta()
        time.sleep(15)

def main():
    try:
        print("initializing, adding event listeners")
        topic = "$aws/things/pi2-sensors/shadow/update"
        try:
            _thread.start_new_thread(loop_status_checking, ('[Thread-Status-Checking]',))
             # *** This delta listening can not be running in a new thread ***
             loop_delta_listening('[Thread-Delta-Listening]')
        except: 
            print("Error: unable to start thread")
            traceback.print_exc(file=sys.stdout)
        
        while True:
            pass
        
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
