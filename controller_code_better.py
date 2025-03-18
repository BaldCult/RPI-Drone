import evdev, asyncio
from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event6')

print(gamepad)

async def main(gamepad):
    async for ev in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                print(f"Left Joystick X: {event.value}")
            elif event.code == ecodes.ABS_Y:
                print(f"Left Joystick Y: {event.value}")
            elif event.code == ecodes.ABS_Z:
                print(f"Right Joystick X: {event.value}")
            elif event.code == ecodes.ABS_RZ:
                print(f"Right Joystick Y: {event.value}")
        #print(repr(ev))

asyncio.run(main(gamepad))

for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_X:
            print(f"Left Joystick X: {event.value}")
        elif event.code == ecodes.ABS_Y:
            print(f"Left Joystick Y: {event.value}")
        elif event.code == ecodes.ABS_Z:
            print(f"Right Joystick X: {event.value}")
        elif event.code == ecodes.ABS_RZ:
            print(f"Right Joystick Y: {event.value}")