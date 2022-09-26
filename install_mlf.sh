#!/bin/bash
sudo chmod -R 777 ros
sudo chmod -R 777 pkg_python_self_api
cp -r ros/extra_port ~/catkin_ws/install/release/ned/share
cp -r ros/rfid ~/catkin_ws/install/release/ned/share
cp -r ros/mlf_mqtt ~/catkin_ws/install/release/ned/share
cp -r ros/mlf_vision_treatment ~/catkin_ws/install/release/ned/share/
cp -r pkg_python_self_api ~/
cp bootStart.sh ~/
cp ~/install_mlf/ros/launchBringup/niryo_robot_base_robot.launch.xml ~/catkin_ws/install/release/ned/share/niryo_robot_bringup/launch

#echo -e "source /home/niryo/catkin_ws/install/release/ned/setup.bash\nexport MLF_NAME=NED2\n\n#AUTOBOOT\nTerminal=`tty`\n        '/dev/tty1')\n                ~/bootStart.sh\n                ;;\nesac" >> ~/.bashrc


#adding self-api and virtual env
sudo apt update
sudo apt-get install mosquitto
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9-venv
mkdir ~/venv
python3.9 -m venv ~/venv/robotics
source ~/venv/robotics/bin/activate
pip install pyniryo
pip install paho-mqtt
deactivate

cd ~/catkin_ws
source /home/niryo/catkin_ws/install/release/ned/setup.bash
catkin_make