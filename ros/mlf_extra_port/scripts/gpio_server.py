import socket
import pickle

max_length = 65000

HOST='localhost'
PORT = 5002

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, UDP
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')

print("-> waiting for connection")

while True:
    data, address = s.recvfrom(max_length)

    frame_info = pickle.loads(data)

    print(frame_info)
    

