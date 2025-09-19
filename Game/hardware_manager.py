# hardware_manager.py
# This module is responsible for controlling the hardware components
# like LEDs, abstracting the low-level pin operations.

import machine
import utime
import config

class LEDs:
    # Manages the operation of the green and red status LEDs.

    def __init__(self):
        # Sets up the GPIO pins for the green and red LEDs as outputs.
        self.green = machine.Pin(config.GREEN_LED_PIN, machine.Pin.OUT)
        self.red = machine.Pin(config.RED_LED_PIN, machine.Pin.OUT)
        print("Hardware Manager --> Ready")

    def blink_all(self, times=3, delay=0.2):
        # Blinks both LEDs simultaneously for a specified number of times.
        # 'times': The number of blinks.
        # 'delay': The duration in seconds for the on and off states.
        for _ in range(times):
            # Turn both LEDs on.
            self.green.on()
            self.red.on()
            utime.sleep(delay)
            # Turn both LEDs off.
            self.green.off()
            self.red.off()
            utime.sleep(delay)