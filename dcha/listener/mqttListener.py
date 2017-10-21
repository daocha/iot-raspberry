'''
/*
 * Listener Raspberry Pi GPIO
 * <p>
 * Push to AWS IoT 
 */
 '''
import _thread
import sys, traceback
from actions.functions import Action as act


print("initializing...")


def add_topic_listening(threadName, topic):
    print(threadName)
    act.subscribeTopic(topic)
        

def main():
    try:
        #topic = "$aws/things/pi2-sensors/shadow/update/accepted"
        topic = "$aws/things/pi2-sensors/shadow/update/delta"
        print("initializing, topic: ", topic)
        
        
        try:
            _thread.start_new_thread(add_topic_listening, ('[Thread-Topic-Listening]', topic,))
        except: 
            print("Error: unable to start thread")
            traceback.print_exc(file=sys.stdout)
        
        while True:
            pass
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
