BUTTON_A = 3
BUTTON_B = 53
BUTTON_C = 99
BUTTON_D = 141
BUTTON_E = 548

d = {BUTTON_C: None, BUTTON_D: None, BUTTON_E: None}

import radio
from microbit import *

radio.on()
is_pairing = False
controlling = None
while True:
    button = pin2.read_analog()
    if button == BUTTON_B:
        is_pairing = True
        char = ' '
        display.show('P')
    elif button == BUTTON_A:
        is_pairing = False
        controlling = None
        display.clear()
    
    if is_pairing:
        incoming = radio.receive()
        if incoming and incoming.startswith('pair'):
            char = incoming[4]
            display.show(char)
        if button in d:
            d[button] = char
            is_pairing = False
            display.clear()
    else:
        if button in d:
            controlling = d[button]
            
        if controlling:
            raw = pin0.read_analog()
            reading = raw / 204
            if reading > 4.0:
                pos = 4
            elif reading > 3.0:
                pos = 3
            elif reading > 2.0:
                pos = 2
            elif reading > 1.0:
                pos = 1
            else:  
                pos = 0
            
            columns = ['0' for i in range(5)]
            columns[pos] = '9'
            img = ((''.join(columns) + ':')*5)[0:-1]
            img = Image(img)
            display.show(img)
    
            radio.send('control'+controlling+str(raw))
            sleep(100)