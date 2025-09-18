# test_buzzer.py
import machine
import utime

# PWM (Pulse Width Modulation) allows us to play tones of different frequencies
# We'll connect it to pin GP12
buzzer_pwm = machine.PWM(machine.Pin(10))

# Function to play a tone
def play_tone(frequency, duration):
    buzzer_pwm.freq(frequency)    # Set the tone frequency
    buzzer_pwm.duty_u16(32768)    # Set the volume (approx. 50%)
    utime.sleep(duration)         # Play for the given duration
    buzzer_pwm.duty_u16(0)        # Turn off the tone

print("Starting buzzer test... You should hear some tones.")

# Play a simple melody
play_tone(262, 0.2) # C4 tone
utime.sleep(0.05)
play_tone(330, 0.2) # E4 tone
utime.sleep(0.05)
play_tone(392, 0.2) # G4 tone

print("Test complete.")