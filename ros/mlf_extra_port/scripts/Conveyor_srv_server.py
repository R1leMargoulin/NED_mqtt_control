import socket
import pickle

max_length = 65000
UDP_IP = '192.168.0.102'
UDP_PORT = 5004

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, UDP

def main():
    message={'id':12,'control_on': True, 'speed' : 0, 'direction' : -1}
    s.sendto(pickle.dumps(message, protocol=2), (UDP_IP, UDP_PORT))
    print("sent")


if __name__ == '__main__':
    main()
