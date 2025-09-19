# game_logic.py
# This module contains all the game's "rules" and logic calculations.

import random

class GameLogic:
    # Handles the core mechanics of the game, such as task generation and answer validation.

    def __init__(self):
        # Defines the decimal values for each of the 4 bits (from right to left).
        self.bit_values = [1, 2, 4, 8]
        print("Game Logic --> Ready")

    def decimal_to_binary(self, n):
        # Converts a decimal number into a 4-digit binary string with leading zeros.
        binary_str = bin(n)[2:]
        padding = '0' * (4 - len(binary_str))
        return padding + binary_str

    def binary_to_decimal(self, b):
        # Converts a binary string into its decimal integer equivalent.
        return int(b, 2)

    def generate_new_task(self, level):
        # Generates a new task, game mode, and time limit based on the player's current level.
        # This function defines the game's difficulty progression.
        
        # First, select a random number between 3 and 15 for the task.
        task = random.randint(3, 15)
        # Initialize time limit to 0 (meaning no limit by default).
        time = 0
        
        if level < 4:
            # Levels 1-3: Only Classic mode (Decimal -> Binary).
            mode = "CLASSIC"
        elif level < 7:
            # Levels 4-6: Only Reverse mode (Binary -> Decimal).
            mode = "REVERSE"
        elif level < 13:
            # Levels 7-12: A mix of both modes to increase variety.
            mode = random.choice(["CLASSIC", "REVERSE"])
        else:
            # Levels 13 and higher: Mix of modes with an added time limit for pressure.
            mode = random.choice(["CLASSIC", "REVERSE"])
            # The time limit starts at 15 seconds for level 13 and decreases
            # by 1 second for each subsequent level, with a minimum of 5 seconds.
            time = max(5, 15 - (level - 13))
        
        if mode == "REVERSE":
            # For REVERSE mode, the task must be presented to the player as a binary string.
            # The randomly generated decimal number is converted for this purpose.
            task = self.decimal_to_binary(task)
            
        return task, mode, time

    def check_answer(self, state):
        # Validates the player's input against the correct answer based on the current game mode.
        if state.current_mode == "CLASSIC":
            # In CLASSIC mode, compare the player's binary string input with the correct one.
            correct_answer_str = self.decimal_to_binary(state.current_task)
            return state.player_input_str == correct_answer_str
        elif state.current_mode == "REVERSE":
            # In REVERSE mode, compare the player's calculated sum with the correct decimal value.
            correct_answer_dec = self.binary_to_decimal(state.current_task)
            return state.player_sum == correct_answer_dec
        
        # Fallback, should not be reached in normal gameplay.
        return False