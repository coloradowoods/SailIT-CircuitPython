import sail_display
import sail_location
import sail_state
import sail_motion
import sail_calibrate
import displayio
import rgbmatrix
import board

from digitalio import DigitalInOut,Direction,Pull
import rotaryio
import storage
#from adafruit_bitmap_font import bitmap_font
import time
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width = 64,
    height = 64,
    bit_depth = 3,
    rgb_pins = [board.GP2, board.GP3, board.GP6, board.GP7, board.GP8, board.GP9],
    addr_pins = [board.GP10, board.GP15, board.GP14, board.GP27, board.GP28],
    clock_pin = board.GP11,
    latch_pin=board.GP12,
    output_enable_pin=board.GP13,
    tile = 1,
    serpentine = False,
    doublebuffer = True)

import adafruit_gps

if __name__ == '__main__':
    # Setup
    state = sail_state.state_api()
    total_readings = 72
    locations = sail_location.locations_api()
    motion = sail_motion.motion_api()
    mag_cal = sail_calibrate.calibrate_api(total_readings)
    mag_cal.load("/mag_cal.csv")
    locations.load()
    
    # Setup Encoder
    select_encoder = rotaryio.IncrementalEncoder( board.GP20, board.GP21 )
    select_button = DigitalInOut(board.GP22)
    select_button.pull = Pull.UP

    mode_encoder = rotaryio.IncrementalEncoder( board.GP16, board.GP17 )
    mode_button = DigitalInOut(board.GP18)
    mode_button.pull = Pull.UP

    # Setup Accelerometer
    reading = 0,0,0
    i2c = busio.I2C(scl=board.GP1, sda=board.GP0) # SCL, SDA
    sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c, offset=mag_cal.offset, scale=mag_cal.scale)
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

    # Setup GPS
    uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    my_location = 0,0 #40.358752, -105.226105
    
    # Setup Didplay
    RGB = sail_display.RGB_Api(matrix)
    GROUP = displayio.Group()

    # Setup Remote Control
    remote_a_pin = DigitalInOut(board.GP19)
    remote_a_pin.direction = Direction.INPUT
    remote_a_pin.pull = Pull.UP

    remote_d_pin = DigitalInOut(board.GP26)
    remote_d_pin.direction = Direction.INPUT
    remote_d_pin.pull = Pull.UP
    selection = 0
    
    
    start_time = time.monotonic()
    
    
    while True:
        # Process Mode Encoder
        state.mode_index = mode_encoder.position
        mode_encoder.position = state.mode_index
        reading = sensor.read_magnetic()
        state.compass_bearing = locations.compass_bearing(reading)
        state.roll, state.pitch, state.compass = motion.get_angles(accel.acceleration, reading)
        state.roll = reading[0]
        state.pitch = reading[1]
        gps.update()
        if not gps.has_fix:
            state.speed = 0
            state.gps_satellites = gps.satellites
        else:
            state.speed = gps.speed_knots
            state.gps_satellites = gps.satellites
            my_location = gps.latitude, gps.longitude

        if remote_a_pin.value and state.sub_mode != "calibrating":
            state.start_timer()
            mode_encoder.position = state._mode_index
        

        # Process Value Encoder
        if state.has_mode_changed == True:
            print("mode changed - " + state.mode + " - " + state.sub_mode)
            if state.mode == "Course":
                select_encoder.position = state.course_bouy_index
            elif state.mode == "Start":
                print("Resetting selection")
                select_encoder.position = state.time_offset
                state.position = state.time_offset
            elif state.mode == "Bouys":
                select_encoder.position = state.bouy_index
                state.position = state.bouy_index
  
         # Get Selection Value
        state.selection = select_encoder.position 
        select_encoder.position = state.selection 
        
        if state.mode == "Start":
            if select_button.value == False or remote_a_pin.value:
                state.start_timer()
                mode_encoder.position = state._mode_index
            if mode_button.value == False or remote_d_pin.value:
                print("Mode Click")
                state.starting = False
                select_encoder.position = state.time_offset
        if state.mode == "Course":
            if select_button.value == False:
                print("Selection Click")
                state.update_course()
            if mode_button.value == False:
                state.course = ""
        if state.mode == "Bouys":
            bouy_location = locations.get_location(state.bouy)
            if state.sub_mode == "yesno" and state.selection == 1:
                state.latitude = my_location[0]
                state.longitude = my_location[1]        
            else:
                state.latitude = bouy_location[0]
                state.longitude = bouy_location[1]
            state.bearing = locations.bearing(my_location, bouy_location)
            state.distance = locations.distance(my_location, bouy_location)
            if mode_button.value == False:
                if state.sub_mode == "":
                    state.sub_mode = "yesno"
            if select_button.value == False:
                if state.sub_mode == "yesno" and state.selection == 2:
                    state.sub_mode = ""
                else:
                    print("Saving Location")
                    locations.set_location(state.bouy, my_location)
                    locations.save()
                    state.sub_mode = ""
        if state.mode == "GPS":
            state.latitude = gps.latitude
            state.longitude = gps.longitude       
        if state.mode == "Race":
            bouy_location = locations.get_location(state.race_bouy)
            
            state.latitude = bouy_location[0]
            state.longitude = bouy_location[1]
            state.bearing = locations.bearing(my_location, bouy_location)
            state.distance = locations.distance(my_location, bouy_location) 
        if state.mode == "Compass":
            if mode_button.value == False:
                if state.sub_mode == "":
                    state.sub_mode = "yesno"
            if select_button.value == False and state.sub_mode != "calibrating":
                if state.sub_mode == "yesno" and state.selection == 2:
                    state.sub_mode = ""
                else:
                    state.sub_mode = "calibrating"
                    sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c, offset=(0,0,0), scale=(1,1,1))
                    mag_cal.reset(reading)       
            if state.sub_mode == "calibrating":
                if select_button.value == False or remote_a_pin.value:
                    state.calibration_values = mag_cal.record(reading)
                else:
                    state.calibration_values = mag_cal.next_angle, reading[0], reading[1], reading[2]
               
                state.calibration_next_angle = mag_cal.next_angle
               
                if mag_cal.count > total_readings:
                    state.sub_mode = "complete"
                    mag_cal.save("/mag_cal.csv")
                    mag_cal.save_readings("/readings.csv")
                    print(mag_cal.offset, mag_cal.scale)
        RGB.display(state)
        time.sleep(.2)

