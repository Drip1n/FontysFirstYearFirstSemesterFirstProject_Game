# input_handler.py
# This module handles all physical button inputs.
# It includes debouncing logic to ensure reliable press detection.

import machine
import utime
import config

class InputHandler:
    # Manages button states and provides a clean way to check for presses.

    def __init__(self):
        # Initializes the GPIO pins for all buttons defined in the config file.
        # A dictionary comprehension is used to create Pin objects for each button.
        # They are configured as inputs with an internal pull-up resistor.
        self.buttons = {name: machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for name, pin in config.BUTTON_PINS.items()}
        print("Input Handler --> Ready")
        
        # Stores the timestamp of the last registered button press for debouncing.
        self.last_press_time = 0

    def check_press(self):
        # Checks if any button has been pressed since the last check.
        # This method includes a debounce delay to prevent multiple readings from a single press.
        current_time = utime.ticks_ms()
        
        # If the time since the last press is less than the debounce delay, ignore any new press.
        # This prevents electrical noise from registering as multiple rapid presses.
        if utime.ticks_diff(current_time, self.last_press_time) < config.DEBOUNCE_DELAY_MS:
            return None

        # Iterate through all configured buttons.
        for name, pin in self.buttons.items():
            # With a pull-up resistor, the pin's value is 0 (LOW) when the button is pressed.
            if pin.value() == 0:
                # If a press is detected, update the last press time.
                self.last_press_time = current_time
                # And return the name of the pressed button (e.g., "CONFIRM").
                return name
                
        # If no button is pressed, return None.
        return None

    def is_button_held(self, button_name):
        # Checks if a specific button is being held down at this exact moment.
        # This is a direct check of the pin's state without any debouncing.
        if button_name in self.buttons:
            pin = self.buttons[button_name]
            # Return True if the button is pressed (pin value is 0), otherwise False.
            return pin.value() == 0
            
        return False