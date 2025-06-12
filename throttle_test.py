import evdev, asyncio, os, time, pigpio
from evdev import InputDevice, categorize, ecodes

# Define ESC GPIO pins
ESC_GPIO1 = 17
ESC_GPIO2 = 27
ESC_GPIO3 = 22
ESC_GPIO4 = 4

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    exit("Could not connect to pigpio daemon")

# Find Xbox controller device
def find_gamepad_device():
    for device_path in evdev.list_devices():
        device = evdev.InputDevice(device_path)
        if "Xbox" in device.name:
            print(f"Found gamepad: {device.path} - {device.name}")
            return device
    raise Exception("No Xbox Wireless Controller found")

# Normalize raw joystick input to range -1.0 to 1.0
def normalize(value):
    return (value - 32768) / 32768.0

# Map analog stick input to ESC pulse width (in µs)
def map_to_pwm(value):
    # value is from 0 to 65535
    pwm = ((1000 * value) / 65535) + 1000  # ~1000 to 2000 µs
    return max(1000, min(2000, pwm))       # clamp just in case

# Handle joystick inputs
async def joysticks(gamepad):
    left_X = 0
    left_Y = 0
    right_X = 0
    right_Y = 0

    async for event in gamepad.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                left_x_raw = event.value
                left_X = round(normalize(event.value), 2)

            elif event.code == ecodes.ABS_Y:
                left_y_raw = event.value
                left_Y = round(normalize(event.value), 2)

                pwm = map_to_pwm(event.value)

                # Send same PWM to all ESCs for now
                pi.set_servo_pulsewidth(ESC_GPIO1, -1*pwm)
                pi.set_servo_pulsewidth(ESC_GPIO2, -1*pwm)
                pi.set_servo_pulsewidth(ESC_GPIO3, -1*pwm)
                pi.set_servo_pulsewidth(ESC_GPIO4, -1*pwm)

            elif event.code == ecodes.ABS_Z:
                right_X_raw = event.value
                right_X = round(normalize(event.value), 2)

            elif event.code == ecodes.ABS_RZ:
                right_Y_raw = event.value
                right_Y = round(normalize(event.value), 2)

        # Optional: print debug info
        print(f"Left Y: {left_Y}  | PWM: {map_to_pwm(event.value):.2f}")

        # Prevent flooding
        await asyncio.sleep(0.025)  # Faster response but still safe

# Async wrapper
async def analog_inputs(gamepad):
    await joysticks(gamepad)

# Main async entry point
async def main():
    gamepad = find_gamepad_device()
    await analog_inputs(gamepad)

# Run the program
asyncio.run(main())
