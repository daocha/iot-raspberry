'''
/*
 * Listener Raspberry Pi GPIO
 * <p>
 * Push to AWS IoT 
 */
 '''
import RPi.GPIO as gpio

import _thread
import time
import threading
import sys,traceback
from actions.functions import Action as act

gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
gpio.setup(26, gpio.IN)

print("initializing...")

def reset_shockstate():
    global shocking_new
    shocking_new = False

global lighton, lighton_new, shocking, shocking_new, motion, motion_new, shock_timer
lighton = False
lighton_new = False
shocking = False
shocking_new = False
motion = False
motion_new = False
shock_timer = threading.Timer(10.0, reset_shockstate)

def light_callback(channel):
    onoff = gpio.input(channel)
    print("Light detected, value = " + str(onoff))
    global lighton_new
    if onoff:
        lighton_new = True
    else:
        lighton_new = False

def motion_callback(channel):
    onoff = gpio.input(channel)
    print("Body motion detected, value = " + str(onoff))
    global motion_new
    if onoff:
        motion_new = True
    else:
        motion_new = False
        
def shock_callback(channel):
    print("Shocking detected.")
    global shocking_new, shock_timer
    shocking_new = True
    shock_timer.cancel()
    shock_timer.start()

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
        print("adding event listeners")
        # 26 for light sensor: light on
        # gpio.add_event_detect(26, gpio.BOTH, callback=light_callback, bouncetime=1000)
        
        # 26 for body motion detecting sensor
        gpio.add_event_detect(26, gpio.BOTH, callback=motion_callback, bouncetime=200)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.RISING, callback=shock_callback, bouncetime=10)
        
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
        gpio.cleanup()

if __name__ == "__main__":
    main()
