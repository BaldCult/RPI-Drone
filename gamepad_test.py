# gamepad_test.py

import evdev
import asyncio
from evdev import InputDevice, ecodes

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
            elif event.code == ecodes.ABS_Z:
                latest_values["right_X"] = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_RZ:
                latest_values["right_Y"] = round(normalize(event.value), 2)
