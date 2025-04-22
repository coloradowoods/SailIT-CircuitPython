import math
#from math import sin, cos, sqrt, atan2, radians, degrees
import time

class motion_api():
    def __init__(self):
        
        self._theta_m = 0
        self._phi_m = 0
        self._theta_f_old = 0
        self._theta_f_new = 0
        
        self._theta = 0  # pitch
        self._phi = 0 # roll
        
        self._phi_f_new = 0
        self._phi_f_old = 0
        
        self._theta_g = 0
        self._phi_g = 0
        
        self._mag_x = 0 # x magnetometer
        self._mag_y = 0 # y magnetometer
        self._psi = 0 # yaw or angle
        
        self._dt = 0
        self._millis_old = self.millis()
        self._gyro_offset = -3.2971954345703125, 1.785430908203125, -0.41400909423828125
        self._acc_offset = -.36, -.30, -2.05
        self._acc_scale = 1/10.5, 1/10.5, 1/9.91
        self._min = 0
        self._max = 0
    def millis(self):
        return int(time.time() * 1000)
    
    def get_angles(self, acc, gyro, mag):
        acc_x, acc_y, acc_z = acc
        acc_x = round((acc_x + self._acc_offset[0]) * self._acc_scale[0], 1)
        acc_y = round((acc_y + self._acc_offset[1]) * self._acc_scale[1], 1)
        acc_z = round((acc_z + self._acc_offset[2]) * self._acc_scale[2], 1)

        if acc_x > 1:
            acc_x = 1
        if acc_y > 1:
            acc_y = 1
        if acc_z > 1:
            acc_z = 1
        gyro_x, gyro_y, gyro_z = gyro
        gyro_x += -self._gyro_offset[0]
        gyro_y += -self._gyro_offset[1]
        gyro_z += -self._gyro_offset[2]
        
        mag_x, mag_y, mag_z = mag

        # Lesson 7
        self._theta_m = round(-math.degrees(math.atan2(acc_x,  acc_z)),1)
        self._phi_m = round(-math.degrees(math.atan2(acc_y, acc_z)),1)
        self._phi_f_new = .95 * self._phi_f_old + .05 * self._phi_m
        self._theta_f_new = .95 * self._theta_f_old + .05 * self._theta_m
        
        # Lesson 8
        self._dt = (self.millis() - self._millis_old) / 1000
        self._millis_old = self.millis()

        # Lesson 9
        self._theta = (self._theta + gyro_y * self._dt) * .95 + self._theta_m * .05
        self._phi = (self._phi - gyro_x * self._dt) * .95 + self._phi_m * .05
        
        # Lesson 8
        self._theta_g = self._theta_g + (gyro_y * self._dt)
        self._phi_g = self._phi_g - (gyro_x * self._dt)



        self._psi = math.degrees(math.atan2(mag_y, mag_x))
        val = mag_y
        if self._min == 0:
            self._min = val
            self._max = val
        if val < self._min:
            self._min = val
        if val > self._max:
            self._max = val
        #print(val, self._min, self._max)
        print(self._psi, mag_x, mag_y)
        
        #print(gyro_x, gyro_y, gyro_z)
        #print(self._theta_m, self._phi_m, self._theta_g, self._phi_g, self._theta, self._phi)
        #print(self._theta_m, self._phi_m)
        #print(self._dt, acc_x / 9.8, acc_y / 9.8, acc_z / 9.8, self._theta_m, self._phi_m, self._theta_f_new, self._phi_f_new, self._theta_g, self._phi_g, self._theta, self._phi) 
        
        
        #print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*acc))
        #print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*mag))
        #print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*gyro))
        
        self._phi_f_old = self._phi_f_new
        self._theta_f_old = self._theta_f_new
