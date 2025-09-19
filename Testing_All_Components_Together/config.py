# config.py - Central pin and hardware settings

# I2C Display (OLED 128x64)
PIN_SCL = 1
PIN_SDA = 0
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
I2C_ADDRESS = 0x3C

# Buttons
BUTTON_PINS = {
    "Bit 0": 2,
    "Bit 1": 3,
    "Bit 2": 4,
    "Bit 3": 5,
    "Confirm": 6,
    "Cancel": 7
}

# Outputs
BUZZER_PIN = 10
GREEN_LED_PIN = 14
RED_LED_PIN = 15

# Settings
DEBOUNCE_DELAY_MS = 200