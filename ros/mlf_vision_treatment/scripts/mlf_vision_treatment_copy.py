#!/usr/bin/env python

import sys
import rospy
import socket

from niryo_robot_msgs.msg import ObjectPose
from niryo_robot_poses_handlers.srv import GetTargetPose
from niryo_robot_msgs.msg import RobotState

#rosservice
def GetTargetPose_client(workspace, heigh_offset, x, y, yaw = 0):
     rospy.wait_for_service('add_two_ints')
     try:
         get_target_pose = rospy.ServiceProxy('GetTargetPose', GetTargetPose)
         resp = get_target_pose(workspace, heigh_offset, x, y, yaw)
         return resp
     except rospy.ServiceException as e:
         print("Service call failed: %s"%e)


#socket
def socketrun():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 15555))

    while True:
            s.listen(5)
            client, address = s.accept()
            #print ("{} connected".format( address ))

            response = client.recv(2048)
            if response != "":
                    data = response.split(" ")
                    #workspace, xrel, yrel, angle, offset
                    ws = data[0]
                    x = data[1]
                    y = data[2]
                    angle = data[3]
                    offset = data[4]
                    pose = GetTargetPose_client(ws, offset, x, y, angle)
                    client.sendall(pose)

if __name__ == "__main__":
    socketrun()
