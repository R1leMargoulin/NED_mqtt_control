#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import time
import os

rospy.init_node('rfid_keepalive', anonymous=True)
client = mqtt.Client("rfid_keepalive_local")
client.connect("127.0.0.1")
rfid_topic = "rfid"
client.subscribe(rfid_topic)

if __name__ == '__main__':
    while(True):
        client.publish(rfid_topic, "0")
        time.sleep(5)
