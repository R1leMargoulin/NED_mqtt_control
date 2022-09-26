import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib

max_length = 65000

HOST='10.10.10.10'
PORT = 5001

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, UDP
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')

frame_info = None
buffer = None
frame = None

print("-> waiting for connection")

while True:
    data, address = s.recvfrom(max_length)
    
    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            nums_of_packs = frame_info["packs"]

            for i in range(nums_of_packs):
                data, address = s.recvfrom(max_length)

                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)

            frame = cv2.imdecode(frame, 1)
            #frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
            #frame = cv2.flip(frame, 1)
            
            if frame is not None and type(frame) == np.ndarray:
                cv2.imshow("Stream", frame)
                if cv2.waitKey(1) == 27:
                    break
