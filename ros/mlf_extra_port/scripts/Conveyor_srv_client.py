#!/usr/bin/env python
import rospy
import socket
import numpy
import pickle
import zlib
import struct
import numpy as np
import math
import os
from conveyor_interface.srv import ControlConveyor

max_length = 65000

gw = os.popen("/sbin/ifconfig eth0 | grep inet |awk '{ print $2}'").read().split() #la commande permet de recuperer l ip de l'interface eth0 dans son premier element
z = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
z.connect((gw[0], 0))
IPAddr = z.getsockname()[0] #on r cupere l ip
HOST= IPAddr
PORT = 5004
print(HOST,PORT)

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, UDP
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')

print("-> waiting for connection")

timeout = rospy.get_param("/niryo_robot/python_ros_wrapper/action_execute_timeout")

while True:
    
    data, address = s.recvfrom(max_length)

    conveyor_info = pickle.loads(data)

    rospy.wait_for_service('/niryo_robot/conveyor/control_conveyor',timeout)

    service = rospy.ServiceProxy('/niryo_robot/conveyor/control_conveyor', ControlConveyor)
    
    conv=service(conveyor_info['id'],conveyor_info['control_on'],conveyor_info['speed'],conveyor_info['direction'])

