# hardware_manager.py
import machine
import utime
from ssd1306 import SSD1306_I2C
import config

class Display:
    def __init__(self):
        i2c = machine.I2C(0, scl=machine.Pin(config.PIN_SCL), sda=machine.Pin(config.PIN_SDA))
        self.oled = SSD1306_I2C(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c, config.I2C_ADDRESS)
        print("Display (128x64) inicializovany.")

    def draw_main_menu(self):
        self.oled.fill(0)
        
        # Názov hry na dva riadky pre lepšiu čitateľnosť a centrovanie
        title1 = "BINARY CODE"
        title2 = "BREAKER"
        
        # Vypočítame pozíciu x pre vycentrovanie každého riadku
        # (Šírka displeja - (počet znakov * 8 pixelov na znak)) / 2
        x1 = (config.DISPLAY_WIDTH - (len(title1) * 8)) // 2
        x2 = (config.DISPLAY_WIDTH - (len(title2) * 8)) // 2
        
        self.oled.text(title1, x1, 5)
        self.oled.text(title2, x2, 15)
        
        # Rámček okolo tlačidla štart
        self.oled.rect(18, 40, 92, 14, 1) 
        self.oled.text("< Start >", 30, 43)
        
        self.oled.show()

    def draw_counter_screen(self, counts, last_pressed, all_zero):
        self.oled.fill(0)
    
        # Vytvoríme mapovanie pre krajšie názvy a pridanie pinov
        button_labels = {
            "Bit 0": "Bit 0",
            "Bit 1": "Bit 1",
            "Bit 2": "Bit 2",
            "Bit 3": "Bit 3"
        }
    
        # Vycentrovaný titulok
        title = "Button Test"
        x_title = (config.DISPLAY_WIDTH - (len(title) * 8)) // 2
        self.oled.text(title, x_title, 2)
    
        # --- ZMENA #1: Garantované poradie ---
        # Vytvoríme si zoznam (list), ktorý má pevne dané poradie.
        # Slučka teraz pôjde podľa tohto zoznamu, nie podľa slovníka.
        display_order = ["Bit 0", "Bit 1", "Bit 2", "Bit 3"]
    
        # --- ZMENA #2: Upravené rozostupy ---
        # Zmenšíme medzery medzi riadkami, aby sa všetko zmestilo.
        y_pos = 14 # Začneme o kúsok nižšie
        for name in display_order:
            selector = "> " if name == last_pressed else "  " # Pridaná medzera pre zarovnanie
        
            full_label = button_labels.get(name)
            count = counts.get(name)
        
            self.oled.text(f"{selector}{full_label}: {count}", 5, y_pos)
            y_pos += 10 # Zmenšili sme krok z 12 na 10

        # Vycentrovaná dynamická nápoveda
        if all_zero:
            prompt = "Cancel pre MENU"
        else:
            prompt = "Cancel pre RESET"
        
        x_prompt = (config.DISPLAY_WIDTH - (len(prompt) * 8)) // 2
        self.oled.text(prompt, x_prompt, 54) # Táto pozícia je teraz v poriadku
            
        self.oled.show()

# Ostatné triedy (Buzzer, LEDs, InputHandler) zostávajú rovnaké ako v predošlej verzii
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