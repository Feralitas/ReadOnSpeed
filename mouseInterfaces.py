#!/usr/bin/env python

import logidevmon
import subprocess
import time
import json
import sys
import threading
import asyncio
from kivy.logger import Logger


time_message = time.time_ns()
velocity = 0
mouse_event_listener_thread_handle = None

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



def init_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

def mouse_event_listener_thread():
    Logger.info("logidev: starting logi-devmon.exe")
    server_process = subprocess.Popen(["logi-devmon.exe"], stdout=subprocess.DEVNULL)
    sys.stdout.flush()
    time.sleep(1)
    Logger.info("logidev: logi-devmon.exe started")
    sys.stdout.flush()

    init_event_loop()
    Logger.info("logidev: Event loop initiated")

    mouseUnitId = 0
    keyboardUnitId = 0

    logidevmon.list_devices()
    Logger.info("logidev: Devices listed")
    logtech_devices = logidevmon.LOGITECH_DEVICES
    if not isinstance(logtech_devices, list):
        logtech_devices = [logtech_devices]
    Logger.info(f"logidev: Devices: {logtech_devices}")

    for device in logtech_devices:
        if (device["type"] == "keyboard"):
            keyboardUnitId = device['unitId']

        if (device["type"] == "mouse"):
            mouseUnitId = device['unitId']

    if mouseUnitId == 0:
        Logger.error("logidev: No mouse device found.")
        exit()

    Logger.info("logidev: Get Device info")
    devinfo = logidevmon.get_device_info(mouseUnitId)
    Logger.info(f"logidev: {devinfo}")
    sys.stdout.flush()

    if not devinfo["isConnected"]:
        Logger.error("logidev: Mouse is not connected.")
        exit()

    logidevmon.set_specialKey_config(mouseUnitId, 86, True)
    logidevmon.set_specialKey_config(mouseUnitId, 83, True)
    logidevmon.set_wheel_config(mouseUnitId, divert=True, hires=True, invert=False)
    #logidevmon.set_spyConfig(mouseUnitId, spyButtons=False, spyKeys=False, spyPointer=False, spyThumbWheel=False, spyWheel=True)
    logidevmon.read_events(processEvents)

    server_process.kill()
    server_process.wait(2)
    Logger.info(f"logidev: logi-devmon.exe exited with returncode {server_process.returncode}")
    Logger.info(f"logidev: Mouse Event Listener Thread Ended")



def start_mouse_event_listener_thread():
    global mouse_event_listener_thread_handle
    mouse_event_listener_thread_handle = threading.Thread(target=mouse_event_listener_thread, name="MouseListenerThread")
    mouse_event_listener_thread_handle.start()

def stop_mouse_event_listener_thread():
    global mouse_event_listener_thread_handle
