from email.policy import default
from http import client
from numpy import place
from pyniryo import *
import threading
import ConveyorThread
import socket
import numpy as np
#import queue
import time
import paho.mqtt.client as mqtt
import Get_matrix_from_contours


import pyniryo
import mqtt_thread

#shape=ObjectShape.ANY, color=ObjectColor.ANY
class NedCMD(threading.Thread):
    def __init__(self, ip , nedinfos, conveyor, linkedrobot = 0): #demarrage et initialisation du thread
        threading.Thread.__init__(self)
        #NIRYO START------------------------------------------------------------
        self.name = socket.gethostname()
        self.ned = nedinfos
        self.ip = ip
        self.ned.calibrate_auto()
        #-----------------------------------------------------------------------

        #MQTT-------------------------------------------------------------------
        self.mqtt = mqtt_thread.Mqtt_Thread(self.ip,linkedrobot)
        self.mqtt.start()

        
        #-----------------------------------------------------------------------

        #CAMERA-----------------------------------------------------------------
        self.placeover = 0 #attributs pour le camera pick
        self.color = ObjectColor.ANY
        self.shape = ObjectShape.ANY
        #-----------------------------------------------------------------------

        self.assembled = False

        #CONVEYOR AND TOOL------------------------------------------------------
        self.conveyor = conveyor
        self.ned.set_conveyor()
        self.ned.update_tool()
        self.conveyor.start()
        self.conveyor.update(0,-1)
        self.ned.release_with_tool()
        #------------------------------------------------------------------------


    
    def run(self): # Ce thread se refere aux commandes MQTT pour le controle des robots
        while True:
            if(len(self.mqtt.commandList) > 0):
                cmd = self.mqtt.commandList.pop(0).split(" ")
                print(cmd)
                if(cmd[0] =="pick"):
                    self.pickCmdHandling(cmd)
                elif(cmd[0] =="assembling"):
                    self.assemblingCmdHandling(cmd)
                elif(cmd[0] == "conveyor"):
                    self.conveyorCmdHandling(cmd)
                elif(cmd[0]== "move"):
                    self.move_command_handling(cmd)
                elif(cmd[0]=="change"):
                    if(cmd[1]== "Color"):
                        self.changeColorCmdHandling(cmd)
                    elif(cmd[1]=="Shape"):
                        self.changeShapeCmdHandling(cmd)
                elif(cmd[0] == "wait"):
                    self.waitHandling(int(cmd[1]))
                elif(cmd[0]=="translation"):
                    self.translationCmdHandling(cmd)
                elif(cmd[0] == "release"):
                    self.cmdGraspHandling()
                elif(cmd[0] == "grasp"):
                    self.cmdReleaseHandling()
                elif(cmd[0] == "finished"):
                    self.mqtt.finishHandle()
                elif(cmd[0] == "registeredPose"):
                    self.cmdRegisteredPose(cmd[-1])
                elif(cmd[0] == "SetMaxSpeed"):
                    self.cmdMaxSpeed(int(cmd[1]))
                else:
                    time.sleep(0.1)

    def move(self, goto):
        self.ned.move_joints(goto[0], goto[1], goto[2], goto[3], goto[4], goto[5])
    
    def conveyorUpdate(self, speed, direction):
        print("speed: "+str(speed))
        print("dir: "+str(direction))
        self.conveyor.update(speed,direction)
    
    def Translation(self,x,y,z):
        mlist = self.ned.get_joints()
        pose = PoseObject.to_list(self.ned.forward_kinematics( mlist[0], mlist[1], mlist[2], mlist[3], mlist[4], mlist[5]))
        pose[0] = pose [0] + x
        pose[1] = pose [1] + y
        pose[2] = pose [2] + z
        goto = self.ned.move_pose(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5])


    def pickCmd(self, ws, x=0, y=0, z=0):
        self.ned.release_with_tool()
        self.ned.vision_pick(ws, color=self.color, shape=self.shape,height_offset=z)

        #self.place_over(ws)
        #self.pick_over(x,y,z)

    
    def place_over(self, ws): #cette fonction sert a preciser qu on veut faire du pick avec la camera et preciser les formes et couleurs
        verif = False
        while(not verif):
            targetPose = self.ned.get_target_pose_from_cam(ws , height_offset=0.0, shape=self.shape, color=self.color)
            verif = targetPose[0]
        #print(PoseObject.to_list(targetPose[1]))
        if (PoseObject.to_list(targetPose[1]) != [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
            goto = self.ned.inverse_kinematics(PoseObject.to_list(targetPose[1])[0],PoseObject.to_list(targetPose[1])[1],PoseObject.to_list(targetPose[1])[2] + 0.05,PoseObject.to_list(targetPose[1])[3],PoseObject.to_list(targetPose[1])[4],PoseObject.to_list(targetPose[1])[5])
            #print(goto)
            print(PoseObject.to_list(targetPose[1])[2] + 0.075)
            self.ned.move_joints(goto[0], goto[1], goto[2], goto[3], goto[4], goto[5])
            #ned.move_joints(goto[0], goto[1], goto[2], goto[3], goto[4], goto[5])


    def pick_over(self, xt = 0, yt = 0, zt = 0):#une fois qu'on est au dessus de l'objet, plus qu'a le prendre
                    #On prevoie des translations en parametres si jamais il faut readapter
        mlist = self.ned.get_joints() #prise des angles moteurs au demarrage apres calibration
        pose = PoseObject.to_list(self.ned.forward_kinematics( mlist[0], mlist[1], mlist[2], mlist[3], mlist[4], mlist[5]))
        pose[0] = pose [0] + xt #xt = x translation
        pose[1] = pose [1] + yt
        pose[2] = pose [2] + zt
        print(pose)
        goto = self.ned.inverse_kinematics(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5])
        print(pose[2])
        self.ned.move_joints(goto[0], goto[1], goto[2], goto[3], goto[4], goto[5])
        self.ned.pull_air_vacuum_pump()
        

    def release_over(self, rotation6ToZero = False, Zdown = 0.04):
        mlist = self.ned.get_joints() #prise des angles moteurs au demarrage apres calibration
        #pose = PoseObject.to_list(self.ned.forward_kinematics( mlist[0], mlist[1], mlist[2], mlist[3], mlist[4], mlist[5]))
        #pose[1] = pose [1]  - 0.02
        if(rotation6ToZero == True):
            mlist = self.ned.get_joints()
            #pose = pose.to_list()
            print("c'est la pose : " + str(mlist))
            mlist[5] = mlist[0]
            self.ned.move_joints(mlist[0], mlist[1], mlist[2], mlist[3], mlist[4], mlist[5])

        
        self.ned.shift_pose(RobotAxis.Z, -Zdown)
        #print(pose)
        time.sleep(2)
        self.ned.release_with_tool()

    def assembling(self, ws, RotToZero = 0, Zdown = 0.4):
        self.place_over(ws)
        self.release_over(RotToZero, Zdown)


    def uncompress_image(compressed_image):
        """
        Take a compressed img and return an OpenCV image
        :param compressed_image: compressed image
        :type compressed_image: str
        :return: OpenCV image
        :rtype: numpy.array
        """
        np_arr = np.fromstring(compressed_image, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # def move_test(self): #fonction de test
    #     while True:
    #         self.ned.move_joints(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    #         time.sleep(2)
    #         self.ned.move_to_home_pose()
    #         time.sleep(3)

    def move_command_handling(self, command):
        angles = ((command[1].split("("))[1].split(")")[0]).split(",")
        anglesToInt = (float(angles[0]),float(angles[1]),float(angles[2]),float(angles[3]),float(angles[4]),float(angles[5]))
        self.move(anglesToInt) #to float after modif^^


    def assemblingCmdHandling(self, command):
        ws = command[1]
        rotationZero = 0
        Zdown = 0.4
        facultative = []
        for s in command: # searching if there is in the command the facultative parameter translation
            if(("-rotationZero" in s)or("-Zdown" in s)):
                facultative.append(s)

        if (len(facultative) > 0):
            for i in facultative: #treatement of the facultative parameters
                if("-rotationZero" in i):
                    rotationZero = bool(int((i.split("Zero("))[1].split(")")[0]))
                if("-Zdown" in i):
                    Zdown = float((i.split("Zdown("))[1].split(")")[0])
        print("RotationtoZero=", rotationZero)
        print("zdown = ", Zdown)
        self.assembling(ws, rotationZero, Zdown)


    def pickCmdHandling(self, command):
        ws = command[1]
        facultative = []
        translation = ()
        for s in command: # searching if there is in the command the facultative parameter translation
            if("-translation" in s):
                facultative.append(s)
        print(facultative)
        if (len(facultative)>0):
            translation = facultative.pop(0).split("-translation(")[1].split(")")[0].split(",")#if there is a translation we extract the coords xyz from it
            print(translation)
            self.pickCmd(ws, float(translation[0]), float(translation[1]), float(translation[2]))
        else:
            self.pickCmd(ws)
    
    def changeColorCmdHandling(self, command):
        c = command[-1]
        if(c =="red"):
            self.color = pyniryo.ObjectColor.RED
        elif(c =="green"):
            self.color = pyniryo.ObjectColor.GREEN
        elif(c =="blue"):
            self.color = pyniryo.ObjectColor.BLUE
        elif(c =="any"):
            self.color = pyniryo.ObjectColor.ANY

    def changeShapeCmdHandling(self, command):
        s = command[-1]
        if(s =="square"):
            self.shape = pyniryo.ObjectShape.SQUARE
        elif(s =="circle"):
            self.shape = pyniryo.ObjectShape.CIRCLE
        elif(s =="any"):
            self.shape = pyniryo.ObjectShape.ANY

    def conveyorCmdHandling(self, command):
        speed = int(command[1])
        direction = int(command[2])
        self.conveyorUpdate(speed, direction)
    
    def translationCmdHandling(self, command):
        x = command[1]
        y = command[2]
        z = command[3]
        self.Translation(float(x),float(y),float(z))
    
    def waitHandling(self, x):
        time.sleep(x)

    def cmdReleaseHandling(self):
        self.ned.release_with_tool()

    def cmdGraspHandling(self):
        self.ned.grasp_with_tool()
    
    def cmdRegisteredPose(self, posename):
        pose = PoseObject.to_list(self.ned.get_pose_saved(posename))
        self.ned.move_pose(pose)


    
    def get_rel_pose(self, coords, img):
        x_rel = float(coords[0]) / img.shape[1]
        y_rel = float(coords[1]) / img.shape[0]
        return(x_rel, y_rel)

    def cmdMaxSpeed(self,percentage):
        self.ned.set_arm_max_velocity(percentage)
        