import time
import board
import adafruit_mpu6050

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    accTuple = (mpu.acceleration[0], mpu.acceleration[1], ((float)(accTuple[2]))-2.0)
    #accTuple[2] = ((float)(accTuple[2]))-2.0

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accTuple))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
    print("Temperature: %.2f C" % mpu.temperature)
    print("")
    time.sleep(1)
