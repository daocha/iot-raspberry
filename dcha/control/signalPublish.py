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

def signal_publish(threadName, lightToggle):
    print(threadName)
    update_json = '{"light":"' + str(lightToggle) + '", "backup":"1"}'
        
    act.updateThing(update_json)



def main():
    try:
        print("initializing, adding event listeners")
        
        lightToggle = int(input('Toggle light: '))
        
        try:
            _thread.start_new_thread(signal_publish, ('[Thread-Signal-Publish]', lightToggle, ))
        except:
            print("Error: unable to start thread")
            traceback.print_exc(file=sys.stdout)
        
        while True:
            pass
        
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
