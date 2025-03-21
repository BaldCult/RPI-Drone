import evdev, asyncio
from evdev import InputDevice, categorize, ecodes

def find_gamepad_device():
    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        if 'event' in device.path and 'gamepad' in device.name.lower():
            print(f"Found gamepad: {device.path} - {device.name}")
            return device
    raise Exception("No gamepad found")

async def left_joystick(gamepad):
    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                print(f"Left Joystick X: {event.value}")
            elif event.code == ecodes.ABS_Y:
                print(f"Left Joystick Y: {event.value}")

async def right_joystick(gamepad):
    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_Z:
                print(f"Right Joystick X: {event.value}")
            elif event.code == ecodes.ABS_RZ:
                print(f"Right Joystick Y: {event.value}")

async def main():
    gamepad = find_gamepad_device()
    
    await asyncio.gather(left_joystick(gamepad), right_joystick(gamepad))

asyncio.run(main())
