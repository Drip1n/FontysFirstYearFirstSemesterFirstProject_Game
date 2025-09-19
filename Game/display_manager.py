# display_manager.py
# This module is responsible for handling all rendering operations on the OLED display.
# It manages the different screens of the game, such as the main menu, game HUD,
# and feedback screens, according to the UI design.

import utime
import machine
from ssd1306 import SSD1306_I2C
import config

class Display:
    # Manages the OLED display hardware and provides methods to draw game screens.

    def __init__(self):
        # Initializes the I2C communication and the SSD1306 OLED display driver.
        # Setup the I2C bus using the pins defined in the config file.
        i2c = machine.I2C(0, scl=machine.Pin(config.PIN_SCL), sda=machine.Pin(config.PIN_SDA))
        # Create an instance of the display driver.
        self.oled = SSD1306_I2C(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c, config.I2C_ADDRESS)
        print("Display Manager --> Ready")

    def _center_text(self, text, y):
        # A helper method to draw text horizontally centered on the screen at a given Y-coordinate.
        # It calculates the required X position based on the text length.
        # Calculate the starting X-coordinate to center the text. Each character is 8 pixels wide.
        x = (config.DISPLAY_WIDTH - (len(text) * 8)) // 2
        self.oled.text(text, x, y)

    def _draw_frame(self):
        # Draws a decorative border around the entire screen.
        self.oled.rect(0, 0, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, 1)

    def draw_main_menu(self):
        # Displays the initial welcome screen with the game title and a prompt to start.
        self.oled.fill(0)  # Clear the display buffer
        self._draw_frame()
        self._center_text("BINARY CODE", 10)
        self._center_text("BREAKER", 20)
        self._center_text(">Press Confirm<", 45)
        self.oled.show()  # Push the buffer to the display

    def draw_game_hud(self, state):
        # Renders the main game interface (Heads-Up Display).
        # It shows dynamic information like level, score, time, current task, and player input.
        self.oled.fill(0)
        self._draw_frame()
        
        # --- Top Status Bar ---
        # Display the current level on the top-left.
        self.oled.text(f"Lvl:{state.level}", 5, 5)
        
        # Display score and time on the top-right, stacked vertically.
        score_text = f"Score:{state.score}"
        score_x = config.DISPLAY_WIDTH - (len(score_text) * 8) - 5 # Position 5px from the right edge
        self.oled.text(score_text, score_x, 5)

        # Calculate and display the remaining time if the timer is active.
        if state.time_left > 0:
            elapsed_seconds = utime.ticks_diff(utime.ticks_ms(), state.timer_start_time) // 1000
            remaining_time = state.time_left - elapsed_seconds
            time_str = f"Time: {max(0, remaining_time)}" # Ensure time doesn't go below zero
            time_x = config.DISPLAY_WIDTH - (len(time_str) * 8) - 5
            self.oled.text(time_str, time_x, 15) # Display below the score

        # --- Task Information ---
        # Show the current game mode (Decimal to Binary or vice-versa).
        mode_str = "D->B" if state.current_mode == "CLASSIC" else "B->D"
        self.oled.text(f"Mode: {mode_str}", 5, 22)
        # Display the specific task (e.g., the number to convert).
        self.oled.text(f"Task: {state.current_task}", 5, 34)

        # --- Player Input Area ---
        # Display the player's current input, which varies by game mode.
        if state.current_mode == "CLASSIC": # Binary input
            self.oled.text(f"Input: {state.player_input_str}", 5, 50)
        else: # REVERSE Mode - Decimal input from binary bits
            self.oled.text(f"Sum: {state.player_sum}", 5, 50)
            
        self.oled.show()

    def draw_feedback_screen(self, is_correct, score_change, message=""):
        # Shows a temporary screen after the player submits an answer,
        # indicating if it was correct and the points awarded or deducted.
        self.oled.fill(0)
        self._draw_frame()
        
        # Display a custom message if provided, otherwise default to "CORRECT!" or "WRONG".
        if message:
            self._center_text(message, 20)
        elif is_correct:
            self._center_text("CORRECT!", 20)
        else:
            self._center_text("WRONG", 20)
            
        # Show how many points the player's score changed by.
        self._center_text(f"{score_change} points", 40)
        self.oled.show()
        
    def draw_game_over_screen(self, final_score):
        # Displays the game over message with the final score and a prompt to restart.
        self.oled.fill(0)
        self._draw_frame()
        self._center_text("GAME OVER", 15)
        self._center_text(f"Score: {final_score}", 30)
        self._center_text("> Restart <", 45)
        self.oled.show()

    # --- NEW FUNCTION ---
    def draw_warning_screen(self, line1, line2):
        # Displays a special notification screen for achievements like unlocking a new mode.
        self.oled.fill(0)
        self._draw_frame()
        self._center_text("! WARNING !", 10)
        self._center_text(line1, 28)
        self._center_text(line2, 40)
        self.oled.show()

    def draw_win_screen(self, final_score, high_score, is_new_record):
        # Displays the victory screen with scores and a prompt to play again.
        self.oled.fill(0)
        self._draw_frame()

        # Use the new boolean to decide which title to show
        if is_new_record:
            self._center_text("!!! NEW RECORD !!!", 8)
        else:
            self._center_text("!!! YOU WIN !!!", 8)

        # Display the player's final score.
        score_text = f"Your Score: {final_score}"
        self._center_text(score_text, 22)

        # Display the all-time high score.
        highscore_text = f"High Score: {high_score}"
        self._center_text(highscore_text, 32)
        
        # Prompt to play again.
        self._center_text("> Play Again <", 50)
        
        self.oled.show()

    def draw_info_screen(self, title, line1, line2=""):
        """Zobrazí oznamovaciu obrazovku pre nové funkcie."""
        self.oled.fill(0)
        self._draw_frame()
        self._center_text(f"!!! {title} !!!", 15)
        self._center_text(line1, 30)
        if line2:
            self._center_text(line2, 40)
        self._center_text("> Continue <", 52)
        self.oled.show()