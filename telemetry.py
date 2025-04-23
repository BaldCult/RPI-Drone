import time
import board
import adafruit_mpu6050
import asyncio

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mpu = adafruit_mpu6050.MPU6050(i2c)

#while True:
 #   accTuple = (mpu.acceleration[0], mpu.acceleration[1], ((float)(mpu.acceleration[2]))+2.0)

#    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accTuple))
 #   print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
  #  print("Temperature: %.2f C" % mpu.temperature)
   # print("")
    #time.sleep(1)

latest_values = {
    "temperature": 0
}

async def read_gyro_data():
   while True:
        accTuple = (mpu.acceleration[0], mpu.acceleration[1], ((float)(mpu.acceleration[2]))+2.0)
        sensor_data = {
           "acceleration": {"x": accTuple[0], "y": accTuple[1], "z": accTuple[2]},
           "gyro": {"x": mpu.gyro[0], "y": mpu.gyro[1], "z": mpu.gyro[2]},
           "temperature": mpu.temperature
        }
        latest_values["temperature"] = mpu.temperature
        time.sleep(1)
