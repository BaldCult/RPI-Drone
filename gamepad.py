import evdev
import asyncio
from evdev import InputDevice, categorize, ecodes

for device_path in evdev.list_devices():
  device = evdev.InputDevice(device_path)
        # Match the device name exactly or partially
  print(device.name)
