import evdev, asyncio, os, time
from evdev import InputDevice, categorize, ecodes
from RpiMotorLib import RpiMotorLib

mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

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
        GpioPins = [4, 17, 27, 22]
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                left_x_raw = event.value
                left_X = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_Y:
                left_X_raw = event.value
                left_Y = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_Z:
                right_X_raw = event.value
                right_X = round(normalize(event.value), 2)
            elif event.code == ecodes.ABS_RZ:
                right_Y_raw = event.value
                right_Y = round(normalize(event.value), 2)

        #print(f"Left Joystick X: {left_X}") #event.code == ecodes.ABS_X
        #print(f"Left Joystick Y: {left_Y}") #event.code == ecodes.ABS_Y
        #print(f"Right Joystick X: {right_X}") #event.code == ecodes.ABS_Z
        #print(f"Right Joystick Y: {right_Y}") #event.code == ecodes.ABS_RZ

        #asyncio.sleep(0.25)

async def main():
    gamepad = find_gamepad_device()
    
    await analog_inputs(gamepad)
asyncio.run(main())
