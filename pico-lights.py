from machine import Pin
import utime
import network

# Indexed at 0 (board labelling is 1)
# These must be the same length (ie 3)
outputs = (18, 19, 20)
leds = (10, 11, 12)
switches = (3, 4, 5)

# shortened version for the pin objects
out = []
led = []
sw = []

print ("Creating Entries")

# uses length of outputs
for i in range (0, len(outputs)):
    out.append(Pin(outputs[i], Pin.OUT))
    led.append(Pin(leds[i], Pin.OUT))
    sw.append(Pin(switches[i], Pin.IN, Pin.PULL_UP))

       
# Functions control both output and led
def turn_on (pin):
    out[pin].value(1)
    led[pin].value(1)
    
def turn_off (pin):
    out[pin].value(0)
    led[pin].value(0)

# Uses out to toggle - sets led to same
def toggle_out (pin):
    new_state = 1 - out[pin].value()
    print ("Setting out {} to {}".format(pin, new_state))
    out[pin].value(new_state)
    led[pin].value(new_state)


# Initialise Wifi
def main (): 
    running()
    


# Main loop
def running ():
    while(1):
        for i in range (0, len(sw)):
            if sw[i].value() == 0:
                toggle_out(i)
        utime.sleep (0.5)


if __name__ == '__main__':
    main()