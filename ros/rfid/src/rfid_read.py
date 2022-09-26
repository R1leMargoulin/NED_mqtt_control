#!/usr/bin/env python
import rospy
import serial
from std_msgs.msg import String


def publisher():
    pub = rospy.Publisher('rfid', String, queue_size = 10)
    rospy.init_node('rfid_reader', anonymous=True)
    rate = rospy.Rate(10)

    ser = serial.Serial('/dev/ttyACM0')

    while not rospy.is_shutdown():
        ridden = ""
        for line in ser.readline():
            ridden += line
        if("Card UID" in ridden):
            ridden = ridden.split(": ")
            pub.publish(ridden[1].split("\r")[0])
            rate.sleep()
if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
