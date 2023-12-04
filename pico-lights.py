# Pico Lights Plus - AP Mode
# Code for controlling LED lights using the
# Pico Lights Plus board with NeoPixel status
# Also needs secrets.py with WiFi login details
from machine import Pin
from utime import sleep
import network
import socket
import uasyncio as asyncio
import secrets
import re
from url_handler import URL_Handler
from pixelstatus import *

# Mode can be ap (access point where the Pico acts as a web server)
# or "client" [default] which connects to an existing network
# Note that client mode is blocking and will not run the rest of the code
# until a network connection is established
mode="ap"

# All documents in DocumentRoot are publically accessible
DocumentRoot = "public/"

# Indexed at 0 (board labelling is 1)
# These must be the same length (ie 3)
outputs = (18, 19, 20)
leds = (10, 11, 12)
switches = (3, 4, 5)

# shortened version for the pin objects
out = []
led = []
sw = []


url = URL_Handler(DocumentRoot)

#with open("index.html", "r") as index_file:
#    index_html = index_file.readlines()

      
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



def connect():
    #Connect to WLAN
    if mode== "ap":
        # Access Point mode
        ip = connect_ap_mode()
    else:
        ip = connect_client_mode()
    return ip
    


def connect_ap_mode ():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=secrets.SSID, password=secrets.PASSWORD)
    wlan.active(True)
    while wlan.active() == False:
        print ('Trying to setup AP mode')
    ip = wlan.ifconfig()[0]
    print('AP Mode is active')
    print('Connect to Wireless Network '+secrets.SSID)
    print('Connect to IP address '+ip)
    return ip

def connect_client_mode ():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power saving mode
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connect to IP address '+ip)    
    return ip



def setup_pins ():
    # uses length of outputs
    for i in range (0, len(outputs)):
        out.append(Pin(outputs[i], Pin.OUT))
        led.append(Pin(leds[i], Pin.OUT))
        sw.append(Pin(switches[i], Pin.IN, Pin.PULL_UP))


async def serve_client(reader, writer):
    status_active()
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = request_line.decode("utf-8")
    
    # LED change request (returns own string)
    led_change = url.change_led(request)
    if led_change != None:
        if (led_change[1] == "toggle"):
            toggle_out (led_change[0])
        elif (led_change[1] == "on"):
            turn_on (led_change[0])
        elif (led_change[1] == "off"):
            turn_off (led_change[0])
        # Ignore any other values (code doesn't support any)
        # Return status - currently just text (will change to JSON)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/text\r\n\r\n')
        writer.write('Status ...')
    
    
    else:
        # Otherwise is this is static file request
        
        url_value, url_file, url_type = url.validate_file(request)

        writer.write('HTTP/1.0 {} OK\r\nContent-type: {}\r\n\r\n'.format(url_value, url_type))
        # Send file 1kB at a time (avoid problem with large files exceeding available memory)
        with open(DocumentRoot+url_file, "rb") as read_file:
            data = read_file.read(1024)
            while data:
                writer.write(data)
                await writer.drain()
                data = read_file.read(1024)
            read_file.close()

    await writer.wait_closed()
    print("Client disconnected")

    status_ready()

# Initialise Wifi
async def main ():
    # Set Status LED to Red (power on)
    status_power()
    setup_pins ()
    print ("Connecting to network")
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset
    print ("IP address", ip)
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print ("Web server listening on", ip)
    status_ready()
    while True:
        #onboard.on()
        # Enable following line for heartbeat debug messages
        #print ("heartbeat")
        await asyncio.sleep(0.25)
        # Check gpio pins 10 times between checks for webpage (5 secs)
        for i in range (0, 5):
            check_gpio_buttons()
    


# Main loop
def check_gpio_buttons ():
    for i in range (0, len(sw)):
        if sw[i].value() == 0:
            toggle_out(i)
    sleep (0.5)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()