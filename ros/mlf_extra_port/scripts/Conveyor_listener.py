#!/usr/bin/env python
import rospy
from conveyor_interface.msg import ConveyorFeedbackArray
import socket
import numpy
import pickle
import zlib
import struct
import numpy as np
import math

max_length = 65000
UDP_IP = 'localhost'
UDP_PORT = 5003


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) ##Internet UDP

def conveyor_callback(msg):
    message = {'conveyor_id':msg.conveyors[0].conveyor_id,'running':msg.conveyors[0].running,'speed':msg.conveyors[0].speed,'direction':msg.conveyors[0].direction}
    sock.sendto(pickle.dumps(message), (UDP_IP, UDP_PORT))


def main():
    rospy.init_node('Conveyor_listener')
    conveyor_topic="/niryo_robot/conveyor/feedback"
    rospy.Subscriber(conveyor_topic, ConveyorFeedbackArray, conveyor_callback,queue_size = 1)
    rospy.spin()

if __name__ == '__main__':
    main()
