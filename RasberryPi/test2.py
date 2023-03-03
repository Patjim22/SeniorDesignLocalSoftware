import sys
import re
import evdev


dev =evdev.InputDevice('/dev/input/event0')
dev.grab()

for event in dev.read_loop():
     if event.type == ecodes.EV_KEY: 
      data = categorize(event) # Save the event temporarily to introspect it 
      if data.scancode == 42: 
       if data.keystate == 1: 
        caps = True 
       if data.keystate == 0: 
        caps = False 
      if data.keystate == 1: # Down events only 
       if caps: 
        key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
       else: 
        key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
       if (data.scancode != 42) and (data.scancode != 28): 
        x += key_lookup 
       if(data.scancode == 28): 
        print (x)   # Print it all out! 
        #user_authentication(x)
        x = ''