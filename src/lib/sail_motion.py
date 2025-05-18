import math
#from math import sin, cos, sqrt, atan2, radians, degrees
import time

class motion_api():
    def __init__(self):
        self._theta = 0  # pitch
        self._phi = 0 # roll
        
        self._mag_x = 0 # x magnetometer
        self._mag_y = 0 # y magnetometer
        self._psi = 0 # yaw or angle

        self._acc_offset = .038, 1.1, -1.76
        self._acc_scale = 1/9.7, 1/9.81, 1/8.7
        self._min = 0
        self._max = 0
    def millis(self):
        return int(time.time() * 1000)
    
    def get_angles(self, acc, mag):
        acc_x, acc_y, acc_z = acc
        acc_x = round((acc_x + self._acc_offset[0]) * self._acc_scale[0], 3)
        acc_y = round((acc_y + self._acc_offset[1]) * self._acc_scale[1], 3)
        acc_z = round((acc_z + self._acc_offset[2]) * self._acc_scale[2], 3)
        #print(acc, acc_x, acc_y, acc_z)     

        if acc_x > 1:
            acc_x = 1
        if acc_y > 1:
            acc_y = 1
        if acc_z > 1:
            acc_z = 1
        
   
        
        mag_x, mag_y, mag_z = mag

        # Lesson 7
        theta_rad = math.atan2(acc_x,  acc_z) + math.radians(.9)
        self._theta = round(-math.degrees(theta_rad),1)
        phi_rad = math.atan2(acc_y, acc_z) - math.radians(7)
        self._phi = round(-math.degrees(phi_rad),1)
        
        self._psi = math.degrees(math.atan2(mag_y, mag_x))
        
        m_x = mag_x * math.cos(-theta_rad) - mag_y * math.sin(-phi_rad) * math.sin(-theta_rad) + mag_z * math.cos(-phi_rad) * math.sin(-theta_rad)
        m_y = mag_y * math.cos(-phi_rad) + mag_z * math.sin(-phi_rad)
 
        self._psi = math.degrees(math.atan2(m_y, m_x))
        
        
        
        val = mag_y
        if self._min == 0:
            self._min = val
            self._max = val
        if val < self._min:
            self._min = val
        if val > self._max:
            self._max = val


        
        
        #print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*acc))
        #print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*mag))
        
        return(self._theta, self._phi, self._psi)
