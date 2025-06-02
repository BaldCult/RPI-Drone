import RPi.GPIO as GPIO
from time import sleep

signal_pin = 18

def pinSetup():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(signal_pin, GPIO.OUT)

pinSetup()

esc_pwm = GPIO.PWM(signal_pin, 50)
esc_pwm.start(7.5)

while True:
  print("still loopin")
#sleep(2)
#esc_pwm.stop()
