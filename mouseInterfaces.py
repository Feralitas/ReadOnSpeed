#!/usr/bin/env python

import logidevmon
import subprocess
import time
import json
import sys

server_process = subprocess.Popen(["logi-devmon.exe"], stdout=subprocess.DEVNULL)
time.sleep(1)
print("Server started")

time_message2 = time.time_ns()

def processEvents(message):
    global time_message2
    #print(f"{message}")
    message = json.loads(message)
    if message["path"] == "wheel" and message["success"]:
        time_message1 = time.time_ns()
        time_message2 = time_message1
        velocity = message['value']['delta'] * 1.0
        print(f"{message['value']['delta']: 5}, {velocity: 15.4}, {time_message1}", end="")
        print(f"{message['value']['hires']: 5}, {message['value']['periods']: 5}")
        sys.stdout.flush()
    if message["path"] == "divertedButtons" and message["value"]["cid1"] == 83:
        return False
    else:
        return True

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

print("End")