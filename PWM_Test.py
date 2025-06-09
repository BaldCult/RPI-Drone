import time
import pigpio

ESC_GPIO1 = 17  # GPIO pin connected to ESC signal wire
ESC_GPIO2 = 27
ESC_GPIO3 = 22
ESC_GPIO4 = 4

pi = pigpio.pi()  # Connect to local pigpio daemon
if not pi.connected:
    exit()

# Initialize ESC to minimum throttle
pi.set_servo_pulsewidth(ESC_GPIO1, 1000)  # 1000 µs pulse = minimum throttle
pi.set_servo_pulsewidth(ESC_GPIO2, 1000)
pi.set_servo_pulsewidth(ESC_GPIO3, 1000)
pi.set_servo_pulsewidth(ESC_GPIO4, 1000)
time.sleep(2)  # Wait 2 seconds to arm the ESC

# Gradually increase throttle from 1000 to 1500
for throttle in range(1000, 1501, 10):
    pi.set_servo_pulsewidth(ESC_GPIO1, throttle)
    pi.set_servo_pulsewidth(ESC_GPIO2, throttle)
    pi.set_servo_pulsewidth(ESC_GPIO3, throttle)
    pi.set_servo_pulsewidth(ESC_GPIO4, throttle)
    time.sleep(0.02)  # 20 milliseconds delay

time.sleep(2)  # Hold max throttle for 2 seconds

# (Optional) Stop the ESC (if desired)
pi.set_servo_pulsewidth(ESC_GPIO1, 1000)
pi.set_servo_pulsewidth(ESC_GPIO2, 1000)
pi.set_servo_pulsewidth(ESC_GPIO3, 1000)
pi.set_servo_pulsewidth(ESC_GPIO4, 1000)
time.sleep(2)  # Hold min throttle for 2 seconds

# Cleanup
pi.set_servo_pulsewidth(ESC_GPIO1, 0)  # Disable PWM
pi.set_servo_pulsewidth(ESC_GPIO2, 0)
pi.set_servo_pulsewidth(ESC_GPIO3, 0)
pi.set_servo_pulsewidth(ESC_GPIO4, 0)
pi.stop()
