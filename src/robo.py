"""
Example IMU Control
Robo HAT MM1
https://github.com/wallarug/circuitpython_mpu9250
"""
import board
import busio
from robohat_mpu9250.mpu9250 import MPU9250
from robohat_mpu9250.mpu6500 import MPU6500
from robohat_mpu9250.ak8963 import AK8963
import sail_location
import sail_motion

from time import sleep

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

mpu = MPU6500(i2c, address=0x68)
ak = AK8963(i2c_interface=i2c, offset=(13.18359375, -24.0966796875, -36.8408203125), scale=(0.99818535, 0.9983, 0.98792286))
#ak = AK8963(i2c_interface=i2c, offset=(4.71, -46.5896, 0), scale=(1, 1, 1))#1/25.5, 1/24, 1)
#print("calibrating")
#offset, scale = ak.calibrate(count=256, delay=.200)
#print(offset, scale)
#print("done")
sensor = MPU9250(mpu, ak)

print("Reading in data from IMU.")
print("MPU9250 id: " + hex(sensor.read_whoami()))

locations = sail_location.locations_api()
motion = sail_motion.motion_api()
while True:
    motion.get_angles(sensor.read_acceleration(), sensor.read_gyro(), sensor.read_magnetic())
    #print('Temperature: {0:0.3f}C'.format(sensor.read_temperature()))
    #print(locations.compass_bearing(sensor.read_magnetic()))
    #print(locations.angles(sensor.read_acceleration()))
    sleep(.5)