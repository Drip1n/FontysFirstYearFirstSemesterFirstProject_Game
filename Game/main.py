# main.py
# The main script that integrates all modules, controls the game loop, 
# and manages the state machine.

import utime
# Explicit imports for better clarity
import display_manager
import audio_manager
import hardware_manager # Needed for LEDs
import input_handler
import game_state as gs
import game_logic as gl
import config

# Filename for storing the high score
HIGHSCORE_FILENAME = "highscore.txt"

print("--- Starting Main Program: Binary Breaker ---")

# --- Step 1: Initialize All Objects ---
print("Initializing modules...")
try:
    display = display_manager.Display()
    audio = audio_manager.AudioManager()
    leds = hardware_manager.LEDs()
    inputs = input_handler.InputHandler()
    state = gs.GameState()
    logic = gl.GameLogic()
    print("All modules initialized successfully.")
except Exception as e:
    print(f"Error during initialization: {e}")
    while True:
        pass
print("-" * 20)

# --- New Functions for High Score ---
def load_high_score():
    """Loads the high score from a file."""
    try:
        with open(HIGHSCORE_FILENAME, "r") as f:
            score = int(f.read())
            state.high_score = score
            print(f"High score loaded: {score}")
    except (OSError, ValueError):
        # If the file doesn't exist or is corrupted, start with zero.
        state.high_score = 0
        print("High score file not found, starting from 0.")

def save_high_score():
    """Checks and saves the new high score."""
    is_new_record = False  # Start by assuming no new record
    if state.score > state.high_score:
        print(f"New high score! Saving score: {state.score}")
        state.high_score = state.score
        is_new_record = True # A new record was set!
        try:
            with open(HIGHSCORE_FILENAME, "w") as f:
                f.write(str(state.high_score))
        except OSError as e:
            print(f"Error saving high score: {e}")
    return is_new_record # Return the result

# Load the high score right after initialization
load_high_score()

# --- Step 2: Helper Functions for Game Control ---
def run_startup_sequence():
    """Runs the startup sequence at the start or restart of the game."""
    print("Running startup sequence...")
    current_high_score = state.high_score # We remember the high score
    state.reset()
    state.high_score = current_high_score # Restore it after the reset
    display.draw_main_menu()
    audio.play_startup()
    leds.blink_all(times=3, delay=0.1)
    print("Startup sequence complete. Waiting for player.")

def start_new_game():
    """Starts a brand new game from level 1."""
    print("Starting new game...")
    current_high_score = state.high_score
    state.reset()
    state.high_score = current_high_score
    start_new_level()

def start_new_level():
    """Prepares and displays a new game round."""
    print(f"Preparing Level {state.level}...")
    state.current_screen = "GAME"
    state.player_input_str = "0000"
    state.player_sum = 0
    
    task, mode, time = logic.generate_new_task(state.level)
    
    state.current_task = task
    state.current_mode = mode
    state.time_left = time
    
    if time > 0:
        state.timer_start_time = utime.ticks_ms()
        
    display.draw_game_hud(state)
    print(f"Task: {mode} {task}")

# --- Step 3: Program Start ---
run_startup_sequence()


# --- Step 4: The Main Infinite Loop (The Heart of the Program) ---
cancel_hold_start_time = 0
long_press_cheat_active = False
CHEAT_HOLD_DURATION_MS = 3000

while True:
    # --- DEV CHEAT: Skip Level ---
    current_time_for_cheat = utime.ticks_ms()
    if inputs.is_button_held("Cancel"):
        if cancel_hold_start_time == 0:
            cancel_hold_start_time = current_time_for_cheat
        else:
            hold_duration = utime.ticks_diff(current_time_for_cheat, cancel_hold_start_time)
            if hold_duration > CHEAT_HOLD_DURATION_MS and not long_press_cheat_active:
                print("CHEAT ACTIVATED: Skipping level...")
                long_press_cheat_active = True
                if state.level >= 18: new_level = 20
                else: new_level = state.level + 3
                state.level = min(20, new_level)
                audio.play_confirm()
                leds.blink_all(times=1, delay=0.1)
                if state.current_screen in ["GAME", "FEEDBACK"]:
                    start_new_level()
    else:
        cancel_hold_start_time = 0
        long_press_cheat_active = False

    pressed_button = inputs.check_press()
    
    # --- Process logic based on the active screen (State Machine) ---
    
    # --- A. GAME SCREEN LOGIC ---
    if state.current_screen == "GAME":
        if state.level > 20:
            state.current_screen = "WIN"
            audio.play_startup()
            is_new_record = save_high_score() # Check for a new record and save it
            display.draw_win_screen(state.score, state.high_score, is_new_record) # Pass the result to the screen
            continue

        if state.time_left > 0:
            elapsed_seconds = utime.ticks_diff(utime.ticks_ms(), state.timer_start_time) // 1000
            if elapsed_seconds > 0 and pressed_button:
                display.draw_game_hud(state)
            
            if state.time_left - elapsed_seconds <= 0:
                audio.play_error()
                leds.red.on()
                state.score = max(0, state.score - 5)
                state.last_feedback_correct = False
                display.draw_feedback_screen(False, -5, "TIME'S UP")
                state.current_screen = "FEEDBACK"
                state.feedback_start_time = utime.ticks_ms()
                continue
        
        if pressed_button:
            audio.play_press()
            if "Bit" in pressed_button:
                bit_index = int(pressed_button.split(' ')[1])
                if state.current_mode == "CLASSIC": state.toggle_player_input_bit(bit_index)
                else: state.player_sum += logic.bit_values[bit_index]
            elif pressed_button == "Cancel":
                audio.play_reset()
                if state.current_mode == "CLASSIC": state.player_input_str = "0000"
                else: state.player_sum = 0
            elif pressed_button == "Confirm":
                is_correct = logic.check_answer(state)
                state.last_feedback_correct = is_correct
                if is_correct:
                    state.score += 10
                    audio.play_confirm()
                    leds.green.on()
                    display.draw_feedback_screen(True, 10)
                else:
                    state.score = max(0, state.score - 5)
                    audio.play_error()
                    leds.red.on()
                    display.draw_feedback_screen(False, -5)
                state.current_screen = "FEEDBACK"
                state.feedback_start_time = utime.ticks_ms()

            if state.current_screen == "GAME":
                display.draw_game_hud(state)

    # --- B. MENU SCREEN LOGIC ---
    elif state.current_screen == "MENU":
        if pressed_button == "Confirm":
            audio.play_confirm()
            start_new_game()
            
    # --- C. FEEDBACK SCREEN LOGIC ---
    elif state.current_screen == "FEEDBACK":
        if utime.ticks_diff(utime.ticks_ms(), state.feedback_start_time) > config.FEEDBACK_DURATION_MS:
            leds.green.off()
            leds.red.off()

            show_info_screen = False
            if state.last_feedback_correct:
                state.level += 1
                # Check if the new level unlocks a feature
                if state.level == 4:
                    display.draw_info_screen("NEW MODE", "Unlocked:", "REVERSE Mode")
                    show_info_screen = True
                elif state.level == 7:
                    display.draw_info_screen("NEW MODE", "Unlocked:", "MIXED Modes")
                    show_info_screen = True
                elif state.level == 13:
                    display.draw_info_screen("CHALLENGE!", "Added:", "TIME LIMIT!")
                    show_info_screen = True
            
            if show_info_screen:
                state.current_screen = "INFO" # Switch to the new screen
            else:
                # If there's nothing to unlock, continue normally
                if state.last_feedback_correct == False:
                    start_new_level()
                else:
                    start_new_level()
            
    # --- D. GAME OVER SCREEN LOGIC ---
    elif state.current_screen == "GAME_OVER":
        if pressed_button == "Confirm":
            run_startup_sequence()

    # --- E. WIN SCREEN LOGIC ---
    elif state.current_screen == "WIN":
        if pressed_button == "Confirm":
            run_startup_sequence()

    # --- F. INFO SCREEN LOGIC ---
    elif state.current_screen == "INFO":
        if pressed_button == "Confirm":
            audio.play_confirm()
            start_new_level() # After confirmation, start the new level

    utime.sleep(0.01)
