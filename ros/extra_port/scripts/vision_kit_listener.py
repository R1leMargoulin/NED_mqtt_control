#!/usr/bin/env python
import rospy
from sensor_msgs.msg import CompressedImage
import socket
import numpy
import pickle
import zlib
import struct
import numpy as np
import math

max_length = 65000
UDP_IP = 'localhost'
UDP_PORT = 5001


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) ##Internet UDP

def image_callback(msg):
	frame = msg.data
	# get size of the frame
	buffer_size = len(frame)

	num_of_packs = 1
	if buffer_size > max_length:
	    num_of_packs = int(math.ceil(float(buffer_size)/max_length))
	frame_info = {"packs":num_of_packs}

	sock.sendto(pickle.dumps(frame_info,2), (UDP_IP, UDP_PORT))

	left = 0
	right = max_length

	for i in range(num_of_packs):
	    # truncate data to send
	    data = frame[left:right]
	    left = right
	    right += max_length

	    # send the frames accordingly
	    sock.sendto(data, (UDP_IP, UDP_PORT))


def main():
    rospy.init_node('Vision_kit_listener')
    image_topic="/niryo_robot_vision/compressed_video_stream"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size = 1)
    rospy.spin()

if __name__ == '__main__':
    main()
