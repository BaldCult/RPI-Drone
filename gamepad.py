import evdev
import asyncio
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event5')
print(gamepad)
