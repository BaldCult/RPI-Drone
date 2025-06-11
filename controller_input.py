# controller_input.py

import asyncio
import pigpio
import time
from gamepad_test import latest_values, read_joystick_values
import threading

def motor_control_loop():
    try:
        while True:
            # Read latest joystick values
            lx = gamepad_test.latest_values.get("left_X", 0)
            ly = gamepad_test.latest_values.get("left_Y", 0)
            rx = gamepad_test.latest_values.get("right_X", 0)
            ry = gamepad_test.latest_values.get("right_Y", 0)

            pulsewidths = [
                joystick_to_pulsewidth(lx),
                joystick_to_pulsewidth(ly),
                joystick_to_pulsewidth(rx),
                joystick_to_pulsewidth(ry)
            ]

            for pin, pw in zip(ESC_PINS, pulsewidths):
                pi.set_servo_pulsewidth(pin, pw)

            time.sleep(0.05)  # 20 Hz update rate
    except KeyboardInterrupt:
        pass
    finally:
        for pin in ESC_PINS:
            pi.set_servo_pulsewidth(pin, 0)
        pi.stop()


# GPIO pins connected to ESC signal wires
ESC_PINS = [4, 17, 27, 22]

# Setup pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon. Run 'sudo pigpiod'")
    exit(1)

# Initialize ESCs to minimum throttle
for pin in ESC_PINS:
    pi.set_servo_pulsewidth(pin, 1000)
time.sleep(2)  # Arm ESCs

def joystick_to_pulsewidth(norm_val):
    # Map normalized joystick (-1 to 1) to ESC pulse width (1000 to 2000 µs)
    norm_val = max(-1, min(1, norm_val))  # Clamp to [-1, 1]
    return int(1500 + norm_val * 500)

async def motor_control_loop():
    while True:
        # Read latest joystick values and map to pulsewidths
        pulsewidths = [
            joystick_to_pulsewidth(latest_values["left_X"]),
            joystick_to_pulsewidth(latest_values["left_Y"]),
            joystick_to_pulsewidth(latest_values["right_X"]),
            joystick_to_pulsewidth(latest_values["right_Y"]),
        ]

        # Send PWM signals to ESCs
        for pin, pw in zip(ESC_PINS, pulsewidths):
            pi.set_servo_pulsewidth(pin, pw)

        # Optional: print debug info
        print(f"Pulsewidths: {pulsewidths}")

        await asyncio.sleep(0.05)  # 50 ms update rate

async def main():
    # Run joystick reading and motor control concurrently
    await asyncio.gather(
        read_joystick_values(),
        motor_control_loop()
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopping motors and cleaning up")
finally:
    for pin in ESC_PINS:
        pi.set_servo_pulsewidth(pin, 0)  # Stop PWM signals
    pi.stop()
