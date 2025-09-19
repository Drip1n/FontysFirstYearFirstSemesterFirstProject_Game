# audio_manager.py
# This module handles all sound effects.

import machine
import utime
import config

class AudioManager:
    def __init__(self):
        self.pwm = machine.PWM(machine.Pin(config.BUZZER_PIN))
        print("Audio Manager --> Ready")

    def _play_tone(self, frequency, duration):
        if frequency > 0:
            self.pwm.freq(frequency)
            self.pwm.duty_u16(2000) # Volume
        utime.sleep(duration)
        self.pwm.duty_u16(0)

    def play_startup(self):
        self._play_tone(392, 0.1)
        self._play_tone(523, 0.1)
        self._play_tone(659, 0.15)

    def play_confirm(self):
        self._play_tone(659, 0.1)
        self._play_tone(784, 0.15)

    def play_error(self):
        self._play_tone(262, 0.2)
        
    def play_press(self):
        self._play_tone(1200, 0.02)
        
    def play_reset(self):
        self._play_tone(392, 0.05)
        self._play_tone(262, 0.1)