'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

import time

from awsiot.mqtt import mqttUtils


class TopicSubscriber:

    # General message notification callback
    def customOnMessage(self, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
    
    
    # Suback callback
    def customSubackCallback(self, mid, data):
        print("Received SUBACK packet id: ")
        print(mid)
        print("Granted QoS: ")
        print(data)
        print("++++++++++++++\n\n")
    
    
    # Puback callback
    def customPubackCallback(self, mid):
        print("Received PUBACK packet id: ")
        print(mid)
        print("++++++++++++++\n\n")
        
    def subscribeTopic(self, topic):
        
        myAWSIoTMQTTClient = mqttUtils.createMQTTClient()
    
        myAWSIoTMQTTClient.onMessage = self.customOnMessage
        
        # Connect and subscribe to AWS IoT
        myAWSIoTMQTTClient.connect()
        # Note that we are not putting a message callback here. We are using the general message notification callback.
        myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=self.customSubackCallback)
        time.sleep(2)
        
        # Publish to the same topic in a loop forever
        #loopCount = 0
        #while True:
        #    myAWSIoTMQTTClient.publishAsync(topic, "New Message " + str(loopCount), 1, ackCallback=self.customPubackCallback)
        #    loopCount += 1
        #    time.sleep(3)
