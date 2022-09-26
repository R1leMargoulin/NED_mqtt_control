import imp
from pyniryo import *
import NedThreadCommand
import ConveyorThread

conveyor = ConveyorThread.Conveyor("127.0.0.1")
ned = NiryoRobot("127.0.0.1")
nedthread = NedThreadCommand.NedCMD("127.0.0.1", ned, conveyor)
nedthread.start()