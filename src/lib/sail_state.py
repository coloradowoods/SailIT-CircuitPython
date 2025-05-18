import time

class state_api():
    def __init__(self):
        self._mode = ["Course", "Start", "Race", "Sail", "Bouys", "GPS", "Compass"]
        self._mode_index = 0
        self._old_mode_index = 0
        
        self._sub_mode = ""
        
        self._course_bouys = ["G", "<-", "Clear", "F", "7", "6", "5", "4", "3", "2", "1"]
        self._course_bouy_index = 0
        self._last_course_bouy_index = 1

        self._bouys = ["G", "F", "7", "6", "5", "4", "3", "2", "1"]
        self._bouy_index = 0

        self._course = "2G2G5F"
        self._race_index = 0
        
        self._start_time = 295
        self._m=5
        self._s=0
        self._display_time=""
        self._old_display_time = ""
        self._now = 0
        self._start = time.time()
        self._time_offset = 0
        
        self._calibration_count = 0
        self._calibration_values = 0
    
        self._compass = 0
        self._pitch = 0
        self._roll = 0
        self._speed = 0 
        
        self._option = ""
        self._last_option = ""
        
        self._latitude = 0
        self._longitude = 0
        self._bearing = 0
        self._distance = 0
        self._gps_satellites = 0
        
        self._starting = False
        self._selection = 0

    def save(self):
        with open("/state.csv", "w") as file:
            file.write(f"{self._course},{location[1]},{location[2]}\n")
            file.flush()
    
    def load(self):
        locations = []
        with open("/state.csv", "r") as file:
            mylist = file.read().splitlines()
            for settings in mylist:
                setting = settings.split(",")

    @property
    def gps_satellites(self) -> int:
        """Description"""
        return self._gps_satellites
    
    @gps_satellites.setter
    def gps_satellites(self, value):
        self._gps_satellites = value
    
    @property
    def course(self) -> str:
        """Description"""
        return self._course
    
    @course.setter
    def course(self, value):
        self._course = value

    @property
    def starting(self) -> bool:
        """Description"""
        return self._starting
    
    @starting.setter
    def starting(self, value):
        self._starting = value
        if self._starting == False:
            self._time_offset = 0
            self._now = 0
            self._display_time = ""
        
    @property
    def selection(self) -> int:
        """Description"""
        return self._selection
    
    @selection.setter
    def selection(self, value):

        if self.mode == "Course":
            if value > 10:
                self._selection = 0
            elif value < 0:
                self._selection = 10
            else:
                self._selection = value
            self._course_bouy_index = self._selection
        elif self.mode == "Bouys":
            if self.sub_mode == "":
                if value > 8:
                    self._selection = 0
                elif value < 0:
                    self._selection = 8
                else:
                    self._selection = value
                self._bouy_index = self._selection
            elif self.sub_mode == "yesno":
                if value < 1:
                    self._selection = 2
                elif value > 2:
                    self._selection = 1
                else:
                    self._selection = value            
        elif self.mode == "Start":
            self._selection = value
            self._time_offset = self._selection
        elif self.mode == "Race":
            if value >= len(self._course):
                self._selection = 0
            elif value < 0:
                self._selection = len(self._course) - 1
            else:
                self._selection = value
            self._race_index = self._selection
        elif self.mode == "Compass":
            if self.sub_mode == "yesno":
                if value < 1:
                    self._selection = 2
                elif value > 2:
                    self._selection = 1
                else:
                    self._selection = value
        
    @property
    def race_bouy(self) -> str:
        """Description"""
        if self._race_index == 0:
            return self._course[self._race_index: self._race_index + 1]
        else:
            return self._course[len(self._course)-self._race_index: len(self._course)-self._race_index + 1]

    @property
    def bouy_index(self) -> int:
        """Description"""
        return self._bouy_index

    @property
    def bouy(self) -> str:
        """Description"""
        return self._bouys[self._bouy_index]

    @property
    def course_bouy_index(self) -> int:
        """Description"""
        return self._course_bouy_index

    @property
    def course_bouy(self) -> str:
        """Description"""
        return self._course_bouys[self._course_bouy_index]
    
    @property
    def display_time(self) -> str:
        """Description"""
        return self._display_time
    
    @property
    def mode_index(self) -> int:
        """Description"""
        return self._mode_index
    
    @mode_index.setter
    def mode_index(self, value):
        if self._old_mode_index != value:
            self.sub_mode = ""
            self._old_mode_index = self._mode_index
            if value > 6:
                self._mode_index = 0
            elif value < 0:
                self._mode_index = 6
            else:
                self._mode_index = value
    
    @property
    def has_mode_changed(self) -> bool:
        """Description"""
        return self._mode_index != self._old_mode_index

    @property
    def sub_mode(self) -> str:
        """Description"""
        return self._sub_mode
    
    @sub_mode.setter
    def sub_mode(self, value):
        self._sub_mode = value

    @property
    def calibration_count(self) -> str:
        """Description"""
        return self._calibration_count
    
    @calibration_count.setter
    def calibration_count(self, value):
        self._calibration_count = value


    @property
    def calibration_values(self) -> str:
        """Description"""
        return self._calibration_values
    
    @calibration_values.setter
    def calibration_values(self, value):
        self._calibration_values = value


    @property
    def latitude(self) -> float:
        """Description"""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        self._latitude = value
        
    @property
    def longitude(self) -> float:
        """Description"""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        self._longitude = value
        
    @property
    def bearing(self) -> float:
        """Description"""
        return self._bearing
    
    @bearing.setter
    def bearing(self, value):
        self._bearing = value
        
    @property
    def distance(self) -> float:
        """Description"""
        return self._distance
    
    @distance.setter
    def distance(self, value):
        self._distance = value
    
    @property
    def compass(self) -> float:
        """Description"""
        return self._compass
    
    @compass.setter
    def compass(self, value):
        self._compass = value
    
    @property
    def pitch(self) -> float:
        """Description"""
        return self._pitch
    
    @pitch.setter
    def pitch(self, value):
        self._pitch = value

    @property
    def roll(self) -> float:
        """Description"""
        return self._roll
    
    @roll.setter
    def roll(self, value):
        self._roll = value

    @property
    def speed(self) -> float:
        """Description"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = value
        
    def update_time(self):
        """Description"""
        self._old_dispay_time = self._display_time
        self._now = self._start_time - (time.time()-self._start) + self._time_offset
        if self._now < 0:
            self._now = 0
            self._starting = False
            self._mode_index = 2
        # Calculate min seconds
        self._m,self._s = divmod(self._now,60)

        self._display_time = "%01d:%02d" % (self._m,self._s)
        return self._now

    @property
    def option(self) -> str:
        """Description"""
        return self._option
    
    @property
    def m(self) -> str:
        """Description"""
        return self._m
    
    @property
    def mode(self) -> str:
        """Description"""
        return self._mode[self._mode_index]

    @property
    def time_offset(self) -> str:
        """Description"""
        return self._time_offset
    
    def start_timer(self):
        self._old_mode_index = self._mode_index
        self._mode_index = 1
        self._start = time.time()
        selection = 0
        self._starting = True

    @property
    def has_time_changed(self) -> bool:
        """Description"""
        return self._display_time != self._old_display_time

    def update_course(self):
        if self.course_bouy == "Clear":
            self._course = ""
        elif self.course_bouy == "<-":
            self._course = self._course[:-1]
        elif self._last_course_bouy_index != self._course_bouy_index:
            self._course += self.course_bouy
            self._last_course_bouy_index = self._course_bouy_index
