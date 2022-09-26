import socket
import pickle
import threading
import time
import os

class Conveyor(threading.Thread):
    def __init__(self, ip): #init of the conveyor threads and hi defaults values
        threading.Thread.__init__(self)
        self.max_length = 65000
        gw = os.popen("/sbin/ifconfig eth0 | grep inet |awk '{ print $2}'").read().split()
        self.UDP_IP = gw[0] #ned IP
        self.UDP_PORT = 5004 
        self.currentSpeed = 0 #set speed to 0
        self.currentDirection = 1 #default direction = 1
        self.wantedSpeed = 100 #wanted speed and wanted direction verify that we dont send useless messages if the current speed and direction are se same that our wanted ones
        self.wantedDirection = 1
        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, UDP
        print("connect to conv")
    
    def run(self):
        while True: #we verify that wanted speed and direction are not the same than our current ones
            if(self.wantedSpeed != self.currentSpeed or self.wantedDirection != self.currentDirection):
                self.send(self.wantedSpeed, self.wantedDirection)
                print("aaah")
    
    #send new speed and direction and set them as current ones
    def send(self, speed, direction): #speed between 0 and 100 and direction is 1 or -1
        message={'id':12,'control_on': True, 'speed' : speed, 'direction' : direction}
        self.s.sendto(pickle.dumps(message, protocol=2), (self.UDP_IP, self.UDP_PORT))
        self.currentSpeed = speed
        self.currentDirection = direction
    
    def update(self, speed, direction): #update of wanted speed and direction
        self.wantedSpeed = speed
        self.wantedDirection = direction
           # self.send(speed,direction)
