# test_LED.py
import machine
import utime

# Set GP14 and GP15 as output pins
led_red = machine.Pin(15, machine.Pin.OUT)
led_green = machine.Pin(14, machine.Pin.OUT)

print("Starting LED test... It should be blinking.")

# Infinite loop that will blink the LEDs
while True:
    led_red.on()
    led_green.on()   # Turn on the LEDs
    utime.sleep(1)   # Wait for 1 second
    led_red.off()
    led_green.off()  # Turn off the LEDs
    utime.sleep(1)   # Wait for 1 second