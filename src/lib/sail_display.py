import terminalio
import displayio
import adafruit_display_text.label
import framebufferio

class RGB_Api():
    def __init__(self, matrix):

        #Set text
        self.txt_str = "Sail IT"
        self.YELLOW = 0xffff00
        self.GREEN = 0x00ff00
        self.BLUE = 0x0000ff
        self.RED = 0xff0000
        self.WHITE = 0xffffff
        self.ORANGE = 0xffa500
        self.PURPLE = 0x800080
        self.txt_x = 2
        self.txt_y = 32
        self.txt_font = terminalio.FONT
        self.txt_line_spacing = 1
        self.txt_scale = 1

        #Set scroll
        self.scroll_speed = 30
        self.DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=True,rotation=180)

    def display_text(self, group, color, scale, text, x, y):
        display = adafruit_display_text.label.Label(
            self.txt_font,
            color = color,
            scale = scale,
            text = text,
            line_spacing = self.txt_line_spacing
            )
        display.x = x
        display.y = y
        group.append(display)
        return group
    
   
    def display(self, state):
        group = displayio.Group()
        group = self.display_text(group, self.WHITE, 1, state.mode, 2, 6)
        if state.mode == "Course":
            group = self.display_text(group, self.YELLOW, 1, state.course, 2, 20)
            group = self.display_text(group, self.BLUE, 2, state.course_bouy, 2, 38)
        if state.mode == "Start":
            color = self.GREEN #green
            if state.m < 4 and state.m > 1:
                color = self.YELLOW 
            if state.m < 1:
                color = self.RED #red
            group = self.display_text(group, color, 2, state.display_time, 2, 20)
            group = self.display_text(group, self.RED, 1, "", 52, 20)
            if state.time_offset > 0:
                group = self.display_text(group, self.WHITE, 1, str(state.time_offset), 52, 23)
            elif state.time_offset < 0:
                group = self.display_text(group, self.RED, 1, str(-state.time_offset), 52, 23)
            group = self.display_text(group, self.GREEN, 1, "{angle:.1f}".format(angle = state.compass_bearing), 2, 46)
            group = self.display_text(group, self.GREEN, 1, "o".format(angle = state.compass_bearing), 2+6*len(str("{angle:.1f}".format(angle = state.compass_bearing))), 42)
            group = self.display_text(group, self.PURPLE, 1, str(state.speed) + " kts", 2, 35)
            group = self.display_text(group, self.YELLOW, 1, state.course, 2, 56)
            group = self.display_text(group, self.YELLOW, 2, state.course[0:1], 52, 10)
        if state.mode == "Race":
            group = self.display_text(group, self.YELLOW, 2, state.race_bouy, 52, 10)
            group = self.display_text(group, self.YELLOW, 1, state.course, 2, 16) 
            group = self.display_text(group, self.GREEN, 1, "{angle:.1f}".format(angle = state.compass_bearing), 2, 27)
            group = self.display_text(group, self.GREEN, 1, "o".format(angle = state.compass_bearing), 2+6*len(str("{angle:.1f}".format(angle = state.compass_bearing))), 23)
            if state.distance > 5000:
                group = self.display_text(group, self.BLUE, 1, str("{distance:.1f} mi".format(distance = state.distance/5280)), 2, 38)
            else:
                group = self.display_text(group, self.RED, 1, str("{distance:.1f} ft".format(distance = state.distance)), 2, 38)
            group = self.display_text(group, self.PURPLE, 1, str(state.speed) + "kts", 2, 49)             
        if state.mode == "Sail":
            group = self.display_text(group, self.PURPLE, 1, str(state.speed) + "kts", 2, 20) 
            group = self.display_text(group, 0x0000ff, 1, "{angle:.1f} deg".format(angle = state.pitch), 2, 38)
        if state.mode == "Bouys":
            group = self.display_text(group, self.YELLOW, 2, state.bouy, 50, 10)
            group = self.display_text(group, self.GREEN, 1, str("{direction:.1f}".format(direction = state.bearing)), 2, 24)
            group = self.display_text(group, self.GREEN, 1, "o".format(angle = state.bearing), 2+6*len(str("{angle:.1f}".format(angle = state.bearing))), 19)
            if state.distance > 5000:
                group = self.display_text(group, 0x0000ff, 1, str("{distance:.1f} mi".format(distance = state.distance/5280)), 2, 34)
            else:
                group = self.display_text(group, 0x0000ff, 1, str("{distance:.1f} ft".format(distance = state.distance)), 2, 34)
            group = self.display_text(group, 0x0000ff, 1, str(state.latitude), 2, 44)
            group = self.display_text(group, 0xffa500, 1, str(state.longitude), 2, 57)
        if state.mode == "GPS":
            group = self.display_text(group, self.PURPLE, 1, str(state.speed) + "kts", 2, 17) 
            group = self.display_text(group, 0x0000ff, 1, str(state.gps_satellites) + " sats", 2, 28)
            group = self.display_text(group, 0x0000ff, 1, str(state.latitude), 2, 39)
            group = self.display_text(group, 0xffa500, 1, str(state.longitude), 2, 50)

        self.DISPLAY.root_group = group
