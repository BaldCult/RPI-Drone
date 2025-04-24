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
    "acceleration": {"x": 0, "y": 0, "z": 0},
    "gyro": {"x": 0, "y": 0, "z": 0},
    "temperature": 0
}

async def read_gyro_data():
   while True:
        accTuple = (mpu.acceleration[0], mpu.acceleration[1], ((float)(mpu.acceleration[2]))+2.0)
    
        latest_values["acceleration"] = {"x": round(accTuple[0], 2), "y": round(accTuple[1], 2), "z": round(((float)(mpu.acceleration[2]))+2.0, 2)}
        latest_values["gyro"] = {"x": round(mpu.gyro[0], 2), "y": round(mpu.gyro[1], 2), "z": round(mpu.gyro[2], 2)}
        latest_values["temperature"] = round(mpu.temperature, 2)
        print("Updated latest_values:", latest_values)
        time.sleep(1)
