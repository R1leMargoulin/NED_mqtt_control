#!/bin/bash

sleep 35
~/venv/robotics/bin/python ~/pkg_python_self_api/niryo_robot_command.py & roslaunch mlf_mqtt mqtt.launch

