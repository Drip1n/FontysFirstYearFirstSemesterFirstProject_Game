import machine
import time

# On the Pico W, the built-in LED is connected to the 'LED' pin
led = machine.Pin('LED', machine.Pin.OUT)

print("Program is running! The LED will blink.")

while True:
    led.on()       # Turn on the LED
    time.sleep(1)  # Wait for 1 second
    led.off()      # Turn off the LED
    time.sleep(1)  # Wait for 1 second