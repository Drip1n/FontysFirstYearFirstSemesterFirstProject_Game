# main.py
import utime
import hardware_manager as hw

# --- Inicializácia Všetkých Objektov ---
display = hw.Display()
buzzer = hw.Buzzer()
leds = hw.LEDs()
inputs = hw.InputHandler()

# --- Premenné pre Správu Stavu ---
current_screen = "MENU" 
last_pressed_button = None # Budeme si pamätať posledné stlačené tlačidlo pre UI
input_counts = {
    "Bit 0": 0, "Bit 1": 0, "Bit 2": 0, "Bit 3": 0
}

# --- Funkcie ---
def run_startup_sequence():
    """Spustí úvodnú sekvenciu."""
    display.draw_main_menu()
    buzzer.play_startup_sound()
    leds.blink_all()

def reset_counts():
    """Vynuluje počítadlá a prekreslí obrazovku."""
    global last_pressed_button
    last_pressed_button = None
    for key in input_counts:
        input_counts[key] = 0
    # Prekreslíme s vynulovanými hodnotami
    display.draw_counter_screen(input_counts, last_pressed_button, True)

# --- Spustenie Programu ---
run_startup_sequence()

# --- Hlavná Nekonečná Slučka ---
while True:
    pressed_button = inputs.check_press()
    
    if pressed_button:
        # --- LOGIKA PRE OBRAZOVKU MENU ---
        if current_screen == "MENU":
            if pressed_button == "Confirm":
                current_screen = "COUNTER_TEST"
                reset_counts() # Resetuje a zároveň prekreslí prvú obrazovku
        
        # --- LOGIKA PRE OBRAZOVKU TESTOVANIA POČÍTADIEL ---
        elif current_screen == "COUNTER_TEST":
            
            if pressed_button in input_counts:
                input_counts[pressed_button] += 1
                last_pressed_button = pressed_button # Uložíme posledný vstup
                # Prekreslíme obrazovku s novými dátami
                display.draw_counter_screen(input_counts, last_pressed_button, False)
            
            elif pressed_button == "Cancel":
                all_zero = all(count == 0 for count in input_counts.values())
                
                if all_zero:
                    current_screen = "MENU"
                    run_startup_sequence()
                else:
                    reset_counts()

    utime.sleep(0.01)