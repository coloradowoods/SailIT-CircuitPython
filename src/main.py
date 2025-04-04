import displayio
import rgbmatrix
import board
import framebufferio
from digitalio import DigitalInOut,Direction,Pull
import rotaryio
import adafruit_display_text.label
import terminalio
#from adafruit_bitmap_font import bitmap_font
import time
#from math import sin
import busio
import adafruit_mpu6050

bit_depth_value = 6
unit_width = 64
unit_height = 64
chain_width = 1
chain_height = 1
serpentine_value = True

width_value = unit_width*chain_width
height_value = unit_height*chain_height

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width = width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins = [board.GP2, board.GP3, board.GP6, board.GP7, board.GP8, board.GP9],
    addr_pins = [board.GP10, board.GP15, board.GP14, board.GP20, board.GP22],
    clock_pin = board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile = chain_height, serpentine=serpentine_value,
    doublebuffer = True)

DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=True,rotation=0)

now = t0 =time.monotonic_ns()
append_flag = 0

class RGB_Api():
    def __init__(self):

        #Set text
        self.txt_str = "Sail IT"
        self.txt_color = 0x00ffff
        self.txt_x = 2
        self.txt_y = 32
        self.txt_font = terminalio.FONT
        self.txt_line_spacing = 1
        self.txt_scale = 1

        #Set scroll
        self.scroll_speed = 30

    
    #@brief:  Display a text in static mode
    #@param:  self
    #@retval: None
    def display_time(self, countdown, color, offset, pitch, course):
        countdown_display = adafruit_display_text.label.Label(
            self.txt_font,
            color = color,
            scale = 2,
            text = countdown,
            line_spacing = self.txt_line_spacing
            )
        countdown_display.x = 2
        countdown_display.y = 10
        
        if offset > 0:
            offset_display = adafruit_display_text.label.Label(
                self.txt_font,
                color = 0xffffff,
                scale = 1,
                text = str(offset),
                line_spacing = self.txt_line_spacing
                )
        elif offset < 0:
            offset_display = adafruit_display_text.label.Label(
                self.txt_font,
                color = 0xff0000,
                scale = 1,
                text = str(-offset),
                line_spacing = self.txt_line_spacing
                )
        if offset !=0:
            offset_display.x = 52
            offset_display.y =10

        course_display = adafruit_display_text.label.Label(
            self.txt_font,
            color = 0xffff00,
            scale = 1,
            text = course,
            line_spacing = self.txt_line_spacing
            )
        course_display.x = 2
        course_display.y =58


        aa = "{angle:.1f}".format(angle = pitch)
        pitch_display = adafruit_display_text.label.Label(
            self.txt_font,
            color = 0x0000ff,
            scale = 1,
            text = aa,
            line_spacing = self.txt_line_spacing
            )        
        pitch_display.x = 2
        pitch_display.y = 28

        
        GROUP = displayio.Group()
        GROUP.append(countdown_display)
        if offset !=0:
            GROUP.append(offset_display)
        GROUP.append(course_display)
        GROUP.append(pitch_display)
        DISPLAY.root_group = GROUP
        DISPLAY.refresh()


import adafruit_gps

if __name__ == '__main__':
    # Setup Time
    start_time = 295
    m=5
    s=0
    displaytime=""
    start = time.time()
    
    # Setup Encoder
    encoder = rotaryio.IncrementalEncoder( board.GP16, board.GP17 )
    button = DigitalInOut(board.GP18)
    button.pull = Pull.UP
    
    # Setup Accelerometer
    i2c = busio.I2C(scl=board.GP1, sda=board.GP0) # SCL, SDA
    mpu = adafruit_mpu6050.MPU6050(i2c)
    
    # Setup GPS
    #RX = board.GP1
    #TX = board.GP0
    
    #i2cgps = busio.I2C(scl=board.GP1, sda=board.GP0)
    #gps = adafruit_gps.GPS(i2cgps, True)
    #uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
    #uart.reset_input_buffer()
    #uart.write(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
#     uart.write(b'PMTK220,1000')
    #gps = adafruit_gps.GPS(uart, True)
    #gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    #gps.send_command(b'PMTK220,1000')
    last_print = time.monotonic()
    # Setup Display
    RGB = RGB_Api()
    GROUP = displayio.Group()
    oldDisplayTime = ""
    loc = ""
    
    while True:
        offset = encoder.position
        if button.value == False:
            start = time.time()
            encoder.position = 0
        
        #gps.update()
        #current = time.monotonic()
        #if uart.in_waiting > 0:
        #    received_data = uart.read(uart.in_waiting)
        #    print(f"Received: {received_data.decode()}")
        #if current - last_print >= 1.0 and False:
        #    last_print = current
        #    if not gps.has_fix:
        #        loc = 'No Sat'
        #        continue
        #    print('=' * 40)  # Print a separator line.
        #    loc = 'Lat: {0:.6f} degrees'.format(gps.latitude)
        #    print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        #print("Fix quality: {}".format(gps.fix_quality))
        dnow = start_time - (time.time()-start) + offset
        # Calculate hour min seconds
        m,s = divmod(dnow,60)
        h,m = divmod(m,60)
        displayTime = "%01d:%02d" % (m,s)
        if oldDisplayTime != displayTime:
            #print("Acceleration: tilt:%.2f, pitch: %.2f, roll: %.2f degrees" % (mpu.angles))
            color = 0x00ff00 #green
            if m < 4 and m > 1:
                color = 0xffff00 #green
            if m < 1:
                color = 0xff0000 #green
            RGB.display_time(displayTime, color, offset, mpu.angles[2], loc)
            print(displayTime)
            oldDisplayTime = displayTime
        time.sleep(.1)

