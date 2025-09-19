# config.py
# Centrálny súbor s nastaveniami. Definuje všetky hardvérové piny a herné konštanty.

# I2C Displej (OLED 128x64)
PIN_SCL = 1
PIN_SDA = 0
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
I2C_ADDRESS = 0x3C

# Tlačidlá (podľa tvojej dokumentácie)
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
GREEN_LED_PIN = 14  # Pre budúce použitie
RED_LED_PIN = 15    # Pre budúce použitie

# Herné Nastavenia
DEBOUNCE_DELAY_MS = 200 # Pauza medzi stlačeniami v milisekundách
FEEDBACK_DURATION_MS = 1500 # Ako dlho sa zobrazí obrazovka "Správne/Nesprávne"
