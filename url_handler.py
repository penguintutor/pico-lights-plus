# Module for pico-lights-plus to validate requests
# For security reasons all files that the user may
# access must be listed in this file
import re


class URL_Handler:
    
    static_files = {
        "index.html": "text/html",
        "onbutton.png": "image/png",
        "offbutton.png": "image/png",
        "jquery.min.js": "text/javascript",
        "picolights.js": "text/javascript",
        "picolights.css": "text/css"
        }
    
    def __init__(self, docroot):
        self.docroot = docroot
    
    
    # Do I need to change LEDs
    # Returns tuple with LED to change or None
    # return is <lednum>, <status>
    # where status = "on", "off", "toggle"
    def change_led (self, request):
        # Check it's a "lights" request
        # Split request into parts - eg. GET <filename> HTTPcode
        url_parts = request.split(" ", 2)
        # Check it's a GET request (don't use posts)
        if (url_parts[0] != "GET"):
            return None
        # Check it is http 1.x
        if (not url_parts[2].startswith("HTTP/1.")):
            return None
        # Check first character is a /
        if (url_parts[1][0:7] != "/lights"):
            return None
        print ("Lights command checking for action")
        # Regular expressing Looking for toggle request
        m = re.search ('light=(\d)&action=toggle', request)
        if m != None:
            led_selected = int(m.group(1))-1
            # check valid number
            if (led_selected >=0 and led_selected <= 2) :
                return (led_selected, "toggle")
        # Look for turn on request
        m = re.search ('light=(\d)&action=on', request)
        if m != None:
            led_selected = int(m.group(1))-1
            # check valid number
            if (led_selected >=0 and led_selected <= 2) :
                return (led_selected, "on")
        # Look for turn off request
        m = re.search ('light=(\d)&action=off', request)
        if m != None:
            led_selected = int(m.group(1))-1
            # check valid number
            if (led_selected >=0 and led_selected <= 2) :
                return (led_selected, "off")
        return None
    
    # Is this a valid file?
    # If so return (200, filename, filetype)
    # If not return index.html (may change to 404 file in future)
    def validate_file (self, request):
        # Split request into parts - eg. GET <filename> HTTPcode
        url_parts = request.split(" ", 2)
        # Check it's a GET request (don't use posts)
        if (url_parts[0] != "GET"):
            return (400, "index.html", "text/html")
        # Check it is http 1.x
        if (not url_parts[2].startswith("HTTP/1.")):
            return (400, "index.html", "text/html")
        # Check first character is a /
        if (url_parts[1][0] != "/"):
            return (400, "index.html", "text/html")
        # Strip /
        req_filename = url_parts[1][1:]
        # If filename in list of allowed static files then return as a 200
        if req_filename in URL_Handler.static_files.keys():
            print ("Permitted file "+req_filename)
            return (200, req_filename, URL_Handler.static_files[req_filename])
        return (200, "index.html", "text/html")
        
        