# config.py - Centrálne nastavenia pinov a hardvéru

# I2C Displej (OLED 128x32)
PIN_SCL = 1
PIN_SDA = 0
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
I2C_ADDRESS = 0x3C

# Tlačidlá
BUTTON_PINS = {
    "Bit 0": 2,
    "Bit 1": 3,
    "Bit 2": 4,
    "Bit 3": 5,
    "Confirm": 6,
    "Cancel": 7
}

# Výstupy
BUZZER_PIN = 10
GREEN_LED_PIN = 14
RED_LED_PIN = 15

# Nastavenia
DEBOUNCE_DELAY_MS = 200