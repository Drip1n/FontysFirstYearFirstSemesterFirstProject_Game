# hardware_manager.py
import machine
import utime
from ssd1306 import SSD1306_I2C
import config

class Display:
    def __init__(self):
        i2c = machine.I2C(0, scl=machine.Pin(config.PIN_SCL), sda=machine.Pin(config.PIN_SDA))
        self.oled = SSD1306_I2C(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c, config.I2C_ADDRESS)
        print("Display (128x64) initialized.")

    def draw_main_menu(self):
        self.oled.fill(0)
        
        # Game title on two lines for better readability and centering
        title1 = "BINARY CODE"
        title2 = "BREAKER"
        
        # Calculate the x position to center each line
        # (Display width - (number of characters * 8 pixels per character)) / 2
        x1 = (config.DISPLAY_WIDTH - (len(title1) * 8)) // 2
        x2 = (config.DISPLAY_WIDTH - (len(title2) * 8)) // 2
        
        self.oled.text(title1, x1, 5)
        self.oled.text(title2, x2, 15)
        
        # Frame around the start button
        self.oled.rect(18, 40, 92, 14, 1) 
        self.oled.text("< Start >", 30, 43)
        
        self.oled.show()

    def draw_counter_screen(self, counts, last_pressed, all_zero):
        self.oled.fill(0)
    
        # Create a mapping for prettier names and pin numbers
        button_labels = {
            "Bit 0": "Bit 0",
            "Bit 1": "Bit 1",
            "Bit 2": "Bit 2",
            "Bit 3": "Bit 3"
        }
    
        # Centered title
        title = "Button Test"
        x_title = (config.DISPLAY_WIDTH - (len(title) * 8)) // 2
        self.oled.text(title, x_title, 2)
    
        # --- CHANGE #1: Guaranteed order ---
        # We create a list that has a fixed order.
        # The loop will now follow this list, not the dictionary.
        display_order = ["Bit 0", "Bit 1", "Bit 2", "Bit 3"]
    
        # --- CHANGE #2: Adjusted spacing ---
        # We reduce the space between lines to make everything fit.
        y_pos = 14 # Start a little lower
        for name in display_order:
            selector = "> " if name == last_pressed else "  " # Added space for alignment
        
            full_label = button_labels.get(name)
            count = counts.get(name)
        
            self.oled.text(f"{selector}{full_label}: {count}", 5, y_pos)
            y_pos += 10 # We reduced the step from 12 to 10

        # Centered dynamic prompt
        if all_zero:
            prompt = "Cancel for MENU"
        else:
            prompt = "Cancel for RESET"
        
        x_prompt = (config.DISPLAY_WIDTH - (len(prompt) * 8)) // 2
        self.oled.text(prompt, x_prompt, 54) # This position is now correct
            
        self.oled.show()

# The other classes (Buzzer, LEDs, InputHandler) remain the same as in the previous version
class Buzzer:
    def __init__(self):
        self.pwm = machine.PWM(machine.Pin(config.BUZZER_PIN))
    def play_tone(self, frequency, duration):
        self.pwm.freq(frequency)
        self.pwm.duty_u16(32768)
        utime.sleep(duration)
        self.pwm.duty_u16(0)
    def play_startup_sound(self):
        self.play_tone(392, 0.1)
        self.play_tone(523, 0.1)
        self.play_tone(659, 0.15)

class LEDs:
    def __init__(self):
        self.green = machine.Pin(config.GREEN_LED_PIN, machine.Pin.OUT)
        self.red = machine.Pin(config.RED_LED_PIN, machine.Pin.OUT)
    def blink_all(self, times=3, delay=0.2):
        for _ in range(times):
            self.green.on()
            self.red.on()
            utime.sleep(delay)
            self.green.off()
            self.red.off()
            utime.sleep(delay)
            
class InputHandler:
    def __init__(self):
        self.buttons = {name: machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for name, pin in config.BUTTON_PINS.items()}
        self.last_press_time = 0
    def check_press(self):
        current_time = utime.ticks_ms()
        if current_time - self.last_press_time < config.DEBOUNCE_DELAY_MS:
            return None
        for name, pin in self.buttons.items():
            if pin.value() == 0:
                self.last_press_time = current_time
                return name
        return None