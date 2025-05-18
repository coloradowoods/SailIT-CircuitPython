import math
#from math import sin, cos, sqrt, atan2, radians, degrees
import time

class calibrate_api():
    def __init__(self, samples):
        self._minx = 0
        self._maxx = 0
        self._miny = 0
        self._maxy = 0
        self._minz = 0
        self._maxz = 0
        self._values = 0
        self._count = 0
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)
        self._samples = samples
    
    @property
    def count(self) -> int:
        """Countdown for calibration"""
        return self._count
    
    @count.setter
    def count(self, value):
        self._count = value

    @property
    def samples(self) -> int:
        """Number of samples taken for calibration"""
        return self._samples
    
    @samples.setter
    def samples(self, value):
        self._samples = value
    
    @property
    def offset(self) -> float:
        """Number of samples taken for calibration"""
        return self._offset

    @property
    def scale(self) -> float:
        """Number of samples taken for calibration"""
        return self._scale
    
    def save(self, filename):
        with open(filename, "w") as file:
            file.write(f"{self._offset[0]},{self._offset[1]},{self._offset[2]},{self._scale[0]},{self._scale[1]},{self._scale[2]}\n")
            file.flush()
    
    def load(self, filename):
        try:
            values = []
            with open(filename, "r") as file:
                print(filename + " opened successfully")
                mylist = file.read().splitlines()
                for line in mylist:
                    values = line.split(",")
                    self._offset = float(values[0]), float(values[1]), float(values[2])
                    self._scale = float(values[3]), float(values[4]), float(values[5])
            print(filename + "successfully loaded")  
        except:
            print(filename + "load load failed.  Reverting to defaults.")
            self._offset = (0, 0, 0)
            self._scale = (1, 1, 1)
    def reset(self, reading):
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)
        self._minx = self._maxx = reading[0]
        self._miny = self._maxy = reading[1]
        self._minz = self._maxz = reading[2]   
        self._count = self._samples
        
    def record(self, reading):
        self._minx = min(self._minx, reading[0])
        self._maxx = max(self._maxx, reading[0])
        self._miny = min(self._miny, reading[1])
        self._maxy = max(self._maxy, reading[1])
        self._minz = min(self._minz, reading[2])
        self._maxz = max(self._maxz, reading[2])
        # Hard iron correction
        self._offset = ((self._maxx + self._minx) / 2, (self._maxy + self._miny) / 2, (self._maxz + self._minz) / 2)

        # Soft iron correction
        avg_delta_x = (self._maxx - self._minx) / 2
        avg_delta_y = (self._maxy - self._miny) / 2
        avg_delta_z = (self._maxz - self._minz) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3
        
        scale_x, scale_y, scale_z = 1,1,1

        if avg_delta_x != 0:
            scale_x = avg_delta / avg_delta_x
        if avg_delta_y != 0:    
            scale_y = avg_delta / avg_delta_y
        if avg_delta_z != 0:    
            scale_z = avg_delta / avg_delta_z

            self._scale = (scale_x, scale_y, scale_z)
        self._count -= 1
        return reading[0], self._minx, self._maxx, reading[1], self._miny, self._maxy, reading[2], self._minz, self._maxz, self._count
