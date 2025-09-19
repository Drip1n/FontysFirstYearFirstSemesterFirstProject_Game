# main.py
import utime
import hardware_manager as hw

# --- Initialize All Objects ---
display = hw.Display()
buzzer = hw.Buzzer()
leds = hw.LEDs()
inputs = hw.InputHandler()

# --- Variables for State Management ---
current_screen = "MENU" 
last_pressed_button = None # We'll remember the last pressed button for the UI
input_counts = {
    "Bit 0": 0, "Bit 1": 0, "Bit 2": 0, "Bit 3": 0
}

# --- Functions ---
def run_startup_sequence():
    """Runs the startup sequence."""
    display.draw_main_menu()
    buzzer.play_startup_sound()
    leds.blink_all()

def reset_counts():
    """Resets the counters and redraws the screen."""
    global last_pressed_button
    last_pressed_button = None
    for key in input_counts:
        input_counts[key] = 0
    # Redraw with reset values
    display.draw_counter_screen(input_counts, last_pressed_button, True)

# --- Program Start ---
run_startup_sequence()

# --- Main Infinite Loop ---
while True:
    pressed_button = inputs.check_press()
    
    if pressed_button:
        # --- LOGIC FOR THE MENU SCREEN ---
        if current_screen == "MENU":
            if pressed_button == "Confirm":
                current_screen = "COUNTER_TEST"
                reset_counts() # Resets and simultaneously redraws the first screen
        
        # --- LOGIC FOR THE COUNTER TEST SCREEN ---
        elif current_screen == "COUNTER_TEST":
            
            if pressed_button in input_counts:
                input_counts[pressed_button] += 1
                last_pressed_button = pressed_button # Save the last input
                # Redraw the screen with the new data
                display.draw_counter_screen(input_counts, last_pressed_button, False)
            
            elif pressed_button == "Cancel":
                all_zero = all(count == 0 for count in input_counts.values())
                
                if all_zero:
                    current_screen = "MENU"
                    run_startup_sequence()
                else:
                    reset_counts()

    utime.sleep(0.01)