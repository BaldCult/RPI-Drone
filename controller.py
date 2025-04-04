import evdev, asyncio, os, time
from evdev import InputDevice, categorize, ecodes
from RpiMotorLib import RpiMotorLib

joystick_values = {"left_X": 0.0, "left_Y": 0.0, "right_X": 0.0, "right_Y": 0.0}

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

def normalize(value):
    return (value - 32768) / 32768.0  # Normalize to range -1 to 1

async def joysticks(gamepad):
    left_X = 0
    left_Y = 0
    right_X = 0
    right_Y = 0
    
    async for event in gamepad.async_read_loop():  
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                left_X = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_Y:
                left_Y = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_Z:
                right_X = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_RZ:
                right_Y = round(normalize(event.value), 2)

def start_controller():
    def runner():
        gamepad = find_gamepad_device()
        asyncio.run(joysticks(gamepad))

    t = Thread(target=runner, daemon=True)
    t.start()
