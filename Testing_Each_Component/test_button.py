# test_button.py
import machine
import utime

# Set GP13 as an input pin
# PULL_DOWN means that when the button is not pressed, the pin reads a low level (0)
button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)

print("Starting button test... Press the button and watch the console.")

while True:
    if button.value() == 1:
        # If the button is pressed, the value is 1
        print("Button is pressed!")
        utime.sleep(0.2) # Simple protection against multiple prints (debounce)