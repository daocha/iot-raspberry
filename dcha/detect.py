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
import sys,traceback
from actions.functions import Action as act


gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
gpio.setup(26, gpio.IN)

print("initializing...")

global lighton, lighton_new, shocking, shocking_new
lighton = False
lighton_new = False
shocking = False
shocking_new = False

def light_callback(channel):
    onoff = gpio.input(channel)
    print("Light detected, value = " + str(onoff))
    global lighton, lighton_new
    if onoff:
        lighton_new = True
    else:
        lighton_new = False
    
    

def shock_callback(channel):
    onoff = gpio.input(channel)
    print("Shocking detected, value = " + str(onoff))
    global shocking, shocking_new
    shocking_new = True
    time.sleep(10)
    shocking_new = False

def status_checking():
    print("status checking...")
    global lighton, lighton_new, shocking, shocking_new
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
        gpio.add_event_detect(26, gpio.BOTH, callback=light_callback, bouncetime=1000)
        
        # 24 for shock sensor: shocking
        gpio.add_event_detect(24, gpio.RISING, callback=shock_callback, bouncetime=1000)
        
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
