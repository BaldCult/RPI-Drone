import evdev, asyncio, os
from evdev import InputDevice, categorize, ecodes

def find_gamepad_device():
    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        # Match the device name exactly or partially
        if "Xbox" in device.name:
            print(f"Found gamepad: {device.path} - {device.name}")
            return device
    raise Exception("No Xbox Wireless Controller found")
    
async def analog_inputs(gamepad):
    await joysticks(gamepad)

async def joysticks(gamepad):
    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            os.system("clear")
            if event.code == ecodes.ABS_X:
                print(f"Left Joystick X: {event.value}")
            elif event.code == ecodes.ABS_Y:
                print(f"Left Joystick Y: {event.value}")
            elif event.code == ecodes.ABS_Z:
                print(f"Right Joystick X: {event.value}")
            elif event.code == ecodes.ABS_RZ:
                print(f"Right Joystick Y: {event.value}")

async def right_joystick(gamepad):
    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_Z:
                print(f"Right Joystick X: {event.value}")
            elif event.code == ecodes.ABS_RZ:
                print(f"Right Joystick Y: {event.value}")

async def main():
    gamepad = find_gamepad_device()
    
    await analog_inputs(gamepad)
asyncio.run(main())
