# Code for Pixel status light - based around code for multiple Pixels, but only one used for status
import array, time
from machine import ADC, Pin
import rp2

# Hardcoded as these are tied to pico-lights board
NUM_LEDS = 1
PIN_NUM = 2
brightness = 0.6

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)
        
# NeoPixel used for pico-lights plus needs color in GRB format
def status_power():
    # Power on = Red
    pixels_set (0, (0,255,0))
    pixels_show()
    
# Connected to wireless network
def status_ready():
    # Green
    pixels_set (0, (255,0,0))
    pixels_show()
    
# Network in use
# Status is only a guide
# Note that due to the async nature of the code then there may be other requests that are changing status
def status_active():
    # Blue
    pixels_set (0, (0,0,255))
    pixels_show()