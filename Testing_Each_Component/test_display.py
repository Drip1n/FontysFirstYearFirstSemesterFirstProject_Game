# test_display.py
import machine
from ssd1306 import SSD1306_I2C

# Initialize I2C communication. We're using I2C channel 0, SDA=GP0, SCL=GP1
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
# Create the display object. The resolution is 128x32 pixels.
oled = SSD1306_I2C(128, 32, i2c)

print("Starting display test... Check the screen.")

# Clear the screen (all pixels to 0)
oled.fill(0)

# Write text at positions (x, y)
oled.text("Display Test:", 0, 0)
oled.text("Everything works!", 0, 12)
oled.text("Great!", 0, 24)

# Command to show what we've "drawn" into memory
oled.show()