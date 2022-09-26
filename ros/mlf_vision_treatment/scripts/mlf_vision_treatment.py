#!/usr/bin/env python

import sys
import rospy
import socket
import paho.mqtt.client as mqtt
import time

from niryo_robot_msgs.msg import ObjectPose
from niryo_robot_poses_handlers.srv import GetTargetPose
from niryo_robot_poses_handlers.workspace_manager import WorkspaceManager
from niryo_robot_msgs.msg import RobotState

rospy.init_node('matrix_mqtt_service', anonymous=True)

#rosservice
def GetTargetPose_client(workspace, heigh_offset, x, y, yaw = 0):
    rospy.wait_for_service('/niryo_robot_poses_handlers/get_target_pose')
    try:
        #print("on appelle le srvv zzzzeparti!")
        #ws_manager = WorkspaceManager("~/niryo_robot_saved_files/niryo_robot_workspaces")
        #ws_obj = ws_manager.read(workspace) 
        get_target_pose = rospy.ServiceProxy('/niryo_robot_poses_handlers/get_target_pose', GetTargetPose)
        resp = get_target_pose(str(workspace), float(heigh_offset), float(x), float(y), float(yaw))
        print("service reussi")
        return resp
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    except Exception as e:
        print(e)

#MQTT

def on_msg(cl, userdata, message):
    print("message received")
    msg = str(message.payload.decode("utf-8"))
    data = msg.split(" ")
    #print(data)
    #workspace, xrel, yrel, angle, offset
    ws = data[0]
    x = data[1]
    y = data[2]
    angle = data[3]
    offset = data[4]
    pose = GetTargetPose_client(ws, offset, x, y, angle)
    #print("pose: "+ str(pose))
    cl.publish("matrix/ans", str(pose))



client = mqtt.Client("matrixToPoseNode")
client.connect("127.0.0.1")
client.subscribe("matrix/ask")
client.on_message = on_msg
client.loop_forever()
