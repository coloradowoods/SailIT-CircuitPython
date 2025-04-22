import math
from math import sin, cos, sqrt, atan2, radians, degrees

class locations_api():
    def __init__(self):
        self.locations = []

    def save(self):
        with open("/data.csv", "w") as file:
            for location in self.locations:
                file.write(f"{location[0]},{location[1]},{location[2]}\n")
            file.flush()
    
    def load(self):
        locations = []
        with open("/data.csv", "r") as file:
            mylist = file.read().splitlines()
            for location in mylist:
                location = location.split(",")
                location[1] = float(location[1])
                location[2] = float(location[2])
                locations.append(location)
        self.locations = locations

    def get_location(self,bouy):
        for location in self.locations:
            if bouy == location[0]:
                return location[1],location[2]

    def set_location(self, bouy, location):
        for location in locations:
            if bouy == location[0]:
                return location[1],location[2]
            
    # Rough Calculation of distance (in meters)
    # https://janakiev.com/blog/gps-points-distance-python/
    def distance(self, coord1, coord2):
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        phi1, phi2 = math.radians(lat1), math.radians(lat2) 
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))*3.2808399
    
    def compass_bearing(self, magnetic):
        x, y, z = magnetic
        return math.atan2(y, x) * 180 / math.pi

    def angles(self, accelerometer):
        x, y, z = accelerometer
        x = x/12
        y = y/12
        z = z /12
        
        if x > 1:
            x = 1
        if y > 1:
            y = 1
        if z > 1:
            z = 1
        return (math.acos(z)/2/math.pi*360, math.atan(x/z)/2/math.pi*360, math.atan(y/z)/2/math.pi*360)
    
    # Awesome public domain compass bearing code from Jérôme Renard
    # https://gist.github.com/jeromer/2005586
    def bearing(self, pointA, pointB):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                      cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing
