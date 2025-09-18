# debug_buttons.py
# Ciel: Jednoduchy skript na testovanie funkcnosti vsetkych 6 tlacidiel.
# Vystup sa bude zobrazovat iba v konzole (Shell / REPL).

import machine
import utime

# Definicia pinov podla tvojej dokumentacie
BUTTON_PINS = {
    "Bit 0": 2,
    "Bit 1": 3,
    "Bit 2": 4,
    "Bit 3": 5,
    "Confirm": 6,
    "Cancel": 7
}

# Vytvorime objekty Pin pre kazde tlacidlo s aktivovanym internym PULL_UP rezistorom
buttons = {name: machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for name, pin in BUTTON_PINS.items()}

# Slovnik na sledovanie predchadzajuceho stavu kazdeho tlacidla.
# Toto nam pomoze vypisat spravu iba RAZ pri stlaceni.
# Na zaciatku predpokladame, ze vsetky su nestlacene (stav 1).
last_states = {name: 1 for name in buttons.keys()}

print("--- Spustam test tlacidiel ---")
print("Stlacaj jednotlive tlacidla a sleduj vystup.")

# Nekonecna slucka na monitorovanie stavu
while True:
    # Prejdeme cez vsetky tlacitka v slovniku
    for name, pin in buttons.items():
        current_state = pin.value()
        
        # Zistime, ci sa stav zmenil z nestlaceneho (1) na stlaceny (0)
        if current_state == 0 and last_states[name] == 1:
            print(f"--> Tlacitko '{name}' bolo STLACENE")
            # Aktualizujeme posledny znamy stav
            last_states[name] = 0
            
        # Zistime, ci sa stav zmenil zo stlaceneho (0) na nestlaceny (1)
        elif current_state == 1 and last_states[name] == 0:
            print(f"<-- Tlacitko '{name}' bolo UVOLNENE")
            # Aktualizujeme posledny znamy stav
            last_states[name] = 1
            
    # Kratka pauza, aby sme nepreplnili konzolu a procesor
    utime.sleep(0.01)