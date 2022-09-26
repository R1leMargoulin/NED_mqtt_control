#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from niryo_robot_rpi.msg import DigitalIOState
import paho.mqtt.client as mqtt
import time
import os

rospy.init_node('gpio_sender', anonymous=True)
client = mqtt.Client("gpio_local")
client.connect("127.0.0.1")
gpio_topic = "gpio"
client.subscribe(gpio_topic)


def callback(data):

    datadict = {
    "1A" : data.digital_inputs[0].value,
    "1B" : data.digital_inputs[1].value,
    "1C" : data.digital_inputs[2].value,
    "2A" : data.digital_inputs[3].value,
    "2B" : data.digital_inputs[4].value,
    "2C" : data.digital_inputs[5].value
    }
    client.publish(gpio_topic,  str(datadict))

def listener():
    rospy.Subscriber("/niryo_robot_rpi/digital_io_state", DigitalIOState, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
