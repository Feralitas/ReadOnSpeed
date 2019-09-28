#!/usr/bin/env python

import logidevmon
import subprocess
import time
import json
import sys
import threading


time_message = time.time_ns()
velocity = 0

def processEvents(message):
    global time_message, velocity
    #print(f"{message}")
    message = json.loads(message)
    if message["path"] == "wheel" and message["success"]:
        time_message = time.time_ns()
        velocity = message['value']['delta'] * 1.0
        print(f"{message['value']['delta']: 5}, {velocity: 15.4}, {time_message1}", end="")
        print(f"{message['value']['hires']: 5}, {message['value']['periods']: 5}")
        sys.stdout.flush()
    if message["path"] == "divertedButtons" and message["value"]["cid1"] == 83:
        return False
    else:
        return True



def mouse_event_listener_thread():

    server_process = subprocess.Popen(["logi-devmon.exe"], stdout=subprocess.DEVNULL)
    print("logi-devmon.exe", end="")
    sys.stdout.flush()
    time.sleep(1)
    print(" started")
    sys.stdout.flush()

    mouseUnitId = 0
    keyboardUnitId = 0

    logidevmon.list_devices()
    logtech_devices = logidevmon.LOGITECH_DEVICES
    if not isinstance(logtech_devices, list):
        logtech_devices = [logtech_devices]
    print(logtech_devices)

    for device in logtech_devices:
        if (device["type"] == "keyboard"):
            keyboardUnitId = device['unitId']

        if (device["type"] == "mouse"):
            mouseUnitId = device['unitId']

    if mouseUnitId == 0:
        print("No mouse device found.")
        exit()

    print("Get Device info")
    devinfo = logidevmon.get_device_info(mouseUnitId)
    print(devinfo)
    sys.stdout.flush()

    if not devinfo["isConnected"]:
        print("Mouse is not connected")
        exit()

    logidevmon.set_specialKey_config(mouseUnitId, 86, True)
    logidevmon.set_specialKey_config(mouseUnitId, 83, True)
    logidevmon.set_wheel_config(mouseUnitId, divert=True, hires=True, invert=False)
    #logidevmon.set_spyConfig(mouseUnitId, spyButtons=False, spyKeys=False, spyPointer=False, spyThumbWheel=False, spyWheel=True)
    logidevmon.read_events(processEvents)

    server_process.kill()
    server_process.wait(2)
    print(server_process.returncode)

    print("Mouse Event Listener Thread Ended")


def start_mouse_event_listener_thread():
    t = threading.Thread(target=mouse_event_listener_thread) 

