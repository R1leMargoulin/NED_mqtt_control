#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import time
import os

rospy.init_node('rfid_sender', anonymous=True)


def callback(data):
    client = mqtt.Client("rfid_local")
    client.connect("127.0.0.1")
    rfid_topic = "rfid"
    client.subscribe(rfid_topic)
    client.publish(rfid_topic, str(data.data))

def listener():
    rospy.Subscriber("rfid", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
