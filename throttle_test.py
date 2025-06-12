# gamepad_test.py

import asyncio
import time
import pigpio
import evdev
from evdev import InputDevice, ecodes

ESC_GPIO1 = 17  # GPIO pin connected to ESC signal wire
ESC_GPIO2 = 27
ESC_GPIO3 = 22
ESC_GPIO4 = 4

pi = pigpio.pi()  # Connect to local pigpio daemon
if not pi.connected:
    exit()

# Shared variable that can be imported
latest_values = {
    "left_X": 0,
    "left_Y": 0,
    "right_X": 0,
    "right_Y": 0
}

def find_gamepad_device():
    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        if "Xbox" in device.name:
            return device
    raise Exception("No Xbox Wireless Controller found")

def normalize(value):
    return (value - 32768) / 32768.0  # Normalize to range -1 to 1

async def read_joystick_values():
    gamepad = find_gamepad_device()
    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                latest_values["left_X"] = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_Y:
                latest_values["left_Y"] = round(normalize(event.value), 2)
                if event.value in range (-32767, 32767):
                    pi.set_servo_pulsewidth(ESC_GPIO1, event.value)
                    pi.set_servo_pulsewidth(ESC_GPIO2, event.value)
                    pi.set_servo_pulsewidth(ESC_GPIO3, event.value)
                    pi.set_servo_pulsewidth(ESC_GPIO4, event.value)
            elif event.code == ecodes.ABS_Z:
                latest_values["right_X"] = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_RZ:
                latest_values["right_Y"] = round(normalize(event.value), 2)
