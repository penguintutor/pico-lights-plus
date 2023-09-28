# pico-lights-plus
Raspberry Pi Pico LED Light Controller Plus

Controls LED low-voltage lighting using a Raspberry Pi Pico and the Pico Lights Plus Board.

# Code
This version needs to be installed on a Raspberry Pi Pico W with the appropriate network enabled MicroPython. MicroPython can be installed through the Thonny editor.

To install the program, copy both the pico-lights.py and the pixelstatus.py files to the Raspberry Pi Pico. For the network connection you also need to create a file called secrets.py with details of your SSID and PASSWORD. The example below shows the formatting for the secrets.py file.

    SSID="NetworkSSID"
    PASSWORD="WiFiPassword"
    
## Running on startup

For the code to run automatically on start-up save the pico-lights.py file on your Pico as main.py.


# Printed Circuit Board

Details of the printed circuit board see (PenguinTutor Pico Lights Project)[https://www.penguintutor.com/projects/pico-lights]