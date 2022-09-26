#!/usr/bin/env python
import rospy
from niryo_robot_rpi.msg import DigitalIOState
import socket
import struct
import pickle

max_length = 65000
UDP_IP = 'localhost'
UDP_PORT = 5002

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) ##Internet UDP

def gpio_callback(msg):
    message = {'modes':list(msg.modes),'names':list(msg.names),'pins':list(msg.pins),'states':list(msg.states)}
    sock.sendto(pickle.dumps(message), (UDP_IP, UDP_PORT))
    #print(message)


def main():
    rospy.init_node('GPIO_listener')
    gpio_topic="/niryo_robot_rpi/digital_io_state"
    rospy.Subscriber(gpio_topic, DigitalIOState, gpio_callback,queue_size = 1)
    rospy.spin()

if __name__ == '__main__':
    main()
