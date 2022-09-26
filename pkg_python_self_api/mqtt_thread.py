import paho.mqtt.client as mqtt
import ast
import sys
import time
import socket
import threading

class Gpio_pins():
    def __init__(self):
        self.pins = {'1A' : True, '1B' : True, '1C' : True, '2A' : True, '2B' : True, '2C' : True}
    def setpins(self, newpins):
        self.pins = newpins
    def getpins(self):
        return(self.pins)
    
# class  Gpio_Thread(threading.Thread):
#     def __init__(self, mlf_name): #demarrage et initialisation du thread
#         threading.Thread.__init__(self)
#         self.mlf_name = mlf_name
#         self.client = mqtt.Client(self.mlf_name+"_master")
#         self.client.connect("192.168.0.150")
#         self.client.on_message = self.on_msg
#         self.sub = ""
#         self.pins = Gpio_pins()

#     def run(self):
#         self.sub = "mlf/"+self.mlf_name+"/gpio"
#         self.client.subscribe(self.sub)
#         self.client.loop_forever()
    
#     def gpio_listen(self):
#         self.client.unsubscribe(self.sub)
#         self.sub = "mlf/"+self.mlf_name+"/gpio"
#         self.client.on_message = self.on_msg
#         self.client.subscribe(self.sub)

#     def on_msg(self, client, userdata, message):
#         self.pins.setpins(ast.literal_eval(str(message.payload.decode("utf-8"))))   

#     def getpins(self):
#         return(self.pins.getpins())

class Mqtt_Thread(threading.Thread):
    def __init__(self, ip, linkedRobotNumber): #demarrage et initialisation du thread
        threading.Thread.__init__(self)
        self.mlf_name = socket.gethostname()
        self.ip=ip
        if(linkedRobotNumber != 0):
            self.clientPair = mqtt.Client(self.mlf_name+"_pairmaster")
            self.clientPair.connect("192.168.0."+ str(100+linkedRobotNumber)) #linkedrobot est le robot auquel le robot est rattache
            self.clientPair.message_callback_add("finished", self.finishedForMe_incr)

        self.client = mqtt.Client(self.mlf_name+"_master")
        self.client.connect(self.ip) 

        #MQTT TOPICS CALLBACK DEFINE--------------------------------------------------------------
        self.client.message_callback_add("/command", self.command_handling)
        self.client.message_callback_add("gpio", self.on_msg_gpio)
        self.client.message_callback_add("rfid", self.on_msg_rfid)
        self.client.message_callback_add("/finished", self.finished_incr)
        self.client.message_callback_add("matrix/ans", self.on_msg_matrixAns)
        self.client.subscribe("#")

        #MQTT NEEDS-------------------------------------------------------------------------------
        self.finished = 0
        self.finishedForMe = 0
        self.commandList = []
        self.VerifRfidState = 0
        self.pins = Gpio_pins()
        self.poseFromMatrix = []

    def run(self):
        self.client.loop_forever()

    def command_handling(self, client, userdata, message):
        self.commandList.append(message.payload.decode("utf-8"))
    
    def getpins(self):
        return(self.pins.getpins())

    
    def finished_incr(self):
        self.finished += 1
    
    def finished_decr(self):
        self.finished = self.finished - 1

    def finishedForMe_incr(self):
        self.finishedForMe += 1
    
    def finishedForMe_decr(self):
        self.finishedForMe = self.finished - 1

    def on_msg_gpio(self, client, userdata, message):
        self.pins.setpins(ast.literal_eval(str(message.payload.decode("utf-8")))) 
        #print(".")
    
    def on_msg_rfid(self, client, userdata, message):
        self.rfid = str(message.payload.decode("utf-8"))
        self.VerifRfidState = 1
    
    def rfidDeleteVerif(self):
        self.VerifRfidState = 0

    def publish(self, msg):
        self.client.publish("/command",msg)
        time.sleep(0.1)

    def finishHandle(self):
        self.client.publish("finished","one more time")
    
    def send_ask_matrix_pose(self, workspace, x_rel, y_rel, angle, offset):
        self.client.publish("matrix/ask", (workspace + " " + str(x_rel) + " "+ str(y_rel)+" "+ str(angle)+" "+ str(offset)))
    
    def reset_poseFromMatrix(self):
        self.poseFromMatrix = []

    def on_msg_matrixAns(self, client, userdata, message):
        self.poseFromMatrix = str(message.payload.decode("utf-8"))
