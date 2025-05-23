import math
#from math import sin, cos, sqrt, atan2, radians, degrees
import time

"""
Offsets_Magnetometer:  (210, 499, -217)
Offsets_Gyroscope:     (-1, -3, 0)
Offsets_Accelerometer: (-11, 5, -38)
"""  

class motion_api():
    def __init__(self):
        self._theta = 0  # pitch
        self._theta_new = 0
        self._theta_old = 0
        self._theta_g = 0
        
        self._phi = 0 # roll
        self._phi_new = 0
        self._phi_old = 0
        self._phi_g = 0
        
        self._mag_x = 0 # x magnetometer
        self._mag_y = 0 # y magnetometer
        self._psi = 0 # yaw or angle

        self._min = 0
        self._max = 0
        
        self._dt = 0
        self._millis_old = 0
        
        self._last_val = 0xFFFF
        
    def millis(self):
        return int(time.time() * 1000)
    
    def temperature(self, temperature):
        result = temperature
        if abs(result - self._last_val) == 128:
            result = temperature
            if abs(result - self._last_val) == 128:
                return 0b00111111 & result
        self._last_val = result
        return result

    def get_angles(self, acc, gyro, mag):
        acc_x, acc_y, acc_z = acc
        gyro_x, gyro_y, gyro_z = gyro
        mag_x, mag_y, mag_z = mag
        
        g = 9.81
        
        acc_x = acc_x / g
        if acc_x > 1:
            acc_x = 1
        
        acc_y = acc_y / g
        if acc_y > 1:
            acc_y = 1
        
        acc_z = acc_z / g
        if acc_z > 1:
            acc_z = 1

        # Lesson 6
        theta_rad = math.atan2(acc_x,  acc_z)
        self._theta = math.degrees(theta_rad)
        phi_rad = math.atan2(acc_y, acc_z)
        self._phi = math.degrees(phi_rad)

        self._phi_new=.95 * self._phi_old + .05 * self._phi;
        self._theta_new=.95 * self._theta_old + .05 * self._theta;

        self._dt=(self.millis()-self._millis_old)/1000.;
        self._millis_old = self.millis()

        self._theta = (self._theta + gyro_y * self._dt) * .95 + self._theta * .05
        self._phi = (self._phi - gyro_x * self._dt) * .95 + self._phi * .05
        
        self._theta_g = self._theta_g + gyro_y * self._dt
        self._phi_g = self._phi_g - gyro_x * self._dt

        m_x = mag_x * math.cos(theta_rad) - mag_y * math.sin(phi_rad) * math.sin(theta_rad) + mag_z * math.cos(phi_rad) * math.sin(theta_rad)
        m_y = mag_y * math.cos(phi_rad) + mag_z * math.sin(phi_rad)
 
        self._psi = math.degrees(math.atan2(m_y, m_x))
        return(self._theta, self._phi, self._psi)