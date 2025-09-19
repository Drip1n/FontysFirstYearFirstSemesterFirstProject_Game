# game_state.py
# This module acts as the central data store for the game.
# It holds all the dynamic information about the current session,
# such as score, level, and player input, but contains no game logic itself.

class GameState:
    # A class that represents the complete state of the game at any moment.

    def __init__(self):
        # When a new game state is created, it immediately resets to default values.
        self.reset()

    def reset(self):
        # Resets all game variables to their initial, default values.
        # This is used when starting a new game.
        self.current_screen = "MENU"        # Tracks which screen is active (e.g., "MENU", "GAME").
        self.level = 1                      # The player's current level.
        self.score = 0                      # The player's current score.
        self.high_score = 0                 # All time high score
        self.time_left = 0                  # Time limit for the current task in seconds (0 means infinite).
        self.timer_start_time = 0           # Timestamp (in ms) when the timer for a task started.
        self.current_mode = None            # The current game mode, either "CLASSIC" or "REVERSE".
        self.current_task = None            # The current question or number the player needs to solve.
        self.player_input_str = "0000"      # The player's 4-bit binary input as a string (for "CLASSIC" mode).
        self.player_sum = 0                 # The player's calculated decimal sum (for "REVERSE" mode).
        self.last_feedback_correct = False  # Stores if the last answer was correct, for display purposes.
        self.feedback_start_time = 0        # Timestamp for when a feedback screen (correct/wrong) was shown.
        print("Game state has been reset and is ready.")

    def toggle_player_input_bit(self, bit_index):
        # Toggles a specific bit (0 to 1 or 1 to 0) in the player's input string.
        # The bit_index is assumed to be 0-3 from right to left.
        
        # We convert the string to a list to make it mutable.
        input_list = list(self.player_input_str)
        
        # The mapping `3 - bit_index` is used because the string index is left-to-right,
        # while the bit index is conceptually right-to-left (bit 0 is the rightmost).
        current_value = input_list[3 - bit_index]
        
        # Flip the value of the bit.
        new_value = "1" if current_value == "0" else "0"
        input_list[3 - bit_index] = new_value
        
        # Join the list back into a string and update the state.
        self.player_input_str = "".join(input_list)

