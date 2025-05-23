import math
import time
import busio
import board
import sail_motion
import adafruit_bno055



### i2c
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

sensor = adafruit_bno055.BNO055_I2C(i2c)

# Set the sensor to NDOF_MODE
sensor.mode = adafruit_bno055.NDOF_MODE
motion = sail_motion.motion_api()
"""
sensor.offsets_accelerometer = -11, 5, -38
sensor.offsets_gyroscope = -1, -3, 0
sensor.offsets_magnetometer = 210, 499, -217
print(sensor.calibrated, sensor.calibration_status)
"""
while True:
    #values = sensor.magnetic
    #print("Heading: " + str(180 + math.atan2(values[1], values[0]) * 180 / math.pi))
    print(motion.get_angles(sensor.acceleration, sensor.gyro, sensor.magnetic))
    print(f"Temperature: {motion.temperature(sensor.temperature)} degrees C")
    print(f"Accelerometer (m/s^2): {sensor.acceleration}")
    print(f"Magnetometer (microteslas): {sensor.magnetic}")
    print(f"Gyroscope (rad/sec): {sensor.gyro}")
    print(f"Euler angle: {sensor.euler}")
    print(f"Quaternion: {sensor.quaternion}")
    print(f"Linear acceleration (m/s^2): {sensor.linear_acceleration}")
    print(f"Gravity (m/s^2): {sensor.gravity}")
    print()
    time.sleep(.2)
