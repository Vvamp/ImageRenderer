

#!/bin/python
from tkinter import *
from math import sin
from PIL import Image, ImageDraw
import PIL
import os
import math
import sys

#TODO
# Split in files

# Meta Data
PROGRAM_AUTHOR="Vincent van Setten"
PROGRAM_NAME="RGB Renderer"
PROGRAM_VERSION="0.6.1"

# Settings(Command Line Arguments)

# Settings base class
class setting:
    def __init__(self, name: str, description: str, isSwitch: bool, value, usage="", synonyms=[]):
        self.name = name
        self.description = description
        self.isSwitch = isSwitch 
        self.value = value
        self.usage = usage 
        self.synonyms = synonyms


# A dictionary of command line arguments. Try to refrai from using the key. Instead, use the value's synonyms. 
settings = {
    "debug"     : setting("debug", "Toggles debugging output.", True, False, "render.py --debug", ['-debug', 'd']),
    "findx"     : setting("findx", "Make the program find the correct height based on the width. If the width is also unknown, it makes a square image.", True, False, "render.py --findx", ['-findx', 'x']),
    "findy"     : setting("findy", "Makes the program find the correct width based on the height. If the height is also unknown, it makes a square image.", True, False, "render.py --findy", ['-findy', 'y']),
    "help"      : setting("help", "Shows this help menu.", True, False, "render.py --help", ['-help', 'h']),
    "path"      : setting("path", "Sets the path to the image path. This file has to be in raw text and should contain RGB data.", False, "unset", "render.py --path <path_to_file>", ['-path', '-file', 'f']),
    "width"     : setting("width", "Set the width of the image.", False, -1, "render.py --width <width>", ['-width']),
    "height"    : setting("height", "Set the height of the image.", False, -1, "render.py --height", ['-height']),
    "output"    : setting("output", "Save the image", False, "unset", "render.py --output <file>", ['-output', '-out', 'o'] ),
    "quiet"     : setting("quiet", "Hides the render window", True, False, "render.py -q", ['-quiet', 'q'])
}

def processCLI_Args(args):
    """Sets the list of values corresponding to the command line arguments

    Parameters:
    args (list of strings): The command line arguments passed. Excluding the name of the file
    """
    flagValue = False
    flagValue_value = "None"

    for argument in args:
        if settings["debug"].value:
            print("Processing > Command Line Argument {}".format(argument))
        if not flagValue:
            argFound = False
            for _setting in settings.values():
                if argument[1:].lower() in _setting.synonyms:
                    argFound = True
                    break
            if not argFound:
                print("Invalid argument '{}'. ".format(argument.replace('-', '').lower()))


        switches = []
        setvals = []
        for _setting in settings.values():
            for synonym in _setting.synonyms:
                if _setting.isSwitch:
                    switches.append(synonym)
                else:
                    setvals.append(synonym)

        if argument[1:].lower() in switches:
            value = True
            for _setting in settings.values():
                if( argument[1:].lower().lower() in _setting.synonyms):
                    _setting.value = value
        elif  argument[1:].lower() in setvals:
            flagValue = True
            flagValue_value = argument[1:].lower()
        elif flagValue:
            for _setting in settings.values():
                for synonym in _setting.synonyms:
                    if synonym == flagValue_value:
                        _setting.value = argument
            flagValue = False

#----------------------------------------------------------------------
# Small, Standalone functions

# Clamp Function - Thanks to stackoverflow
def clamp(x):
  """ Clips 'x' to the nearest value if it exceeds the max or min

  Parameters:
  x (int): The value to be clipped

  Returns:
  int:If the value is between 0 and 255, returns that value. If it exceeds 255, it returns 255. If it is below 0, 0 is returned.
  """   
  return max(0, min(x, 255))

# Help Function
def help():
    """Prints a list of command line arguments 
    """
    print("{}@{} by {}".format(PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_AUTHOR))
    print("\n[NAME]\t[FLAGS]\t\t\t[DESCRIPTION]")
    for _setting in settings.values():
        print("{}\t{}\t\t{}\n\tUsage: {}".format(_setting.name, _setting.synonyms, _setting.description, _setting.usage), end="\n\n")
    print("usage: python render.py [options]")
#----------------------------------------------------------------------

# Vital functions

def getData(imagePath):
    if settings["debug"].value == True:
        print("File IO > Opening image data...")
    dataFile = open(imagePath, "r")
    
    if settings["debug"].value == True:
        print("File IO > Reading data...", end="")
    data = dataFile.read()

    if settings["debug"].value == True:
        print(" success!")

    return data
def parseOutputData(data):
    if settings["debug"].value == True:
        print("Parser > Init Parsing output data...")
    rgbdata = []
    i=0
    for rgbval in data.split(')'):
        if(len(rgbval) <= 1):
            continue
        i+=1
        if settings["debug"].value == True:
            print("Parser > Total RGB bytes: {}".format(i))
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        rgbval = rgbval.replace('\n', '')
        rgbval = rgbval.replace(' ', '')
        if settings["debug"].value == True:
            print("Parser > Parsed: {}".format(rgbval))
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append((red, green, blue))
    if settings["debug"].value == True:
        print("Parser > Output data parsing success!")
    return rgbdata
def parseData(data):
    if settings["debug"].value == True:
        print("Parser > Init Parsing data...")
    rgbdata = []
    i=0
    for rgbval in data.split(')'):
        if(len(rgbval) <= 1):
            continue
        i+=1
        if settings["debug"].value == True:
            print("Parser > Total RGB bytes: {}".format(i))
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        rgbval = rgbval.replace('\n', '')
        rgbval = rgbval.replace(' ', '')
        if settings["debug"].value == True:
            print("Parser > Parsed: {}".format(rgbval))
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append("#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue)))
    if settings["debug"].value == True:
        print("Parser > Data parsing success!")
    return rgbdata

def calculateWidth(rgbdata, height=-1):
    if height > 0:
        return abs(math.floor(len(rgbdata)/height))
    else:
        return math.floor(math.sqrt(len(rgbdata)))


def calculateHeight(rgbdata, width=-1):
    if width > 0:
        return abs(math.floor(len(rgbdata)/width))
    else:
        return math.floor(math.sqrt(len(rgbdata)))

def export(image):
    print("Export > Preparing image for exporting...")
   # Save the image to file if set
    if settings["output"].value != "unset":
        extension = ""
        if not settings["output"].value.endswith("jpg"):
            extension = ".jpg"
        name = settings["output"].value + extension
        print("Export > Saving image {}... ".format(name), end="")
        try:
            image.save(name)
        except:
            print('fail.')
        print("success!")

# Render Image Data
def render(imagePath: str, WIDTH: int, HEIGHT: int, findX=False, findY=False):
    """Loads image data from file, parses it and creates an image. If the size is unknown, it tries to find it, if the findX and findY params are set.

    Parameters:
    imagePath (str): Path to the image file
    WIDTH (int): Width of the image
    HEIGHT (int): Height of the image
    findX (bool): If the width of the image should be calculated automatically
    findY (bool): If the height of the image should be calculated automatically
    """

    # Retrieve data from file
    data = getData(imagePath)

    # Parse the data and store it in a 1d-array
    rgbdata = parseData(data)
    if settings["output"].value != "unset":
        photoData = parseOutputData(data)

    if settings["debug"].value == True:
        print ("Renderer > Rendering Image...", end="")
    
    WIDTH = int(WIDTH)
    HEIGHT = int(HEIGHT)

    # Check if the sizes have been calculated. Calculate them otherwise
    if findY == True and findX == False:
        HEIGHT = calculateHeight(rgbdata, WIDTH)
    elif findX == True and findY == False:
        WIDTH = calculateWidth(rgbdata, HEIGHT)
    elif findX and findY:
        HEIGHT = calculateHeight(rgbdata)
        WIDTH = calculateWidth(rgbdata)


    # Make a tkinter window
    if not 'TRAVIS' in os.environ:
        window = Tk()
        window.title("Image {}x{}".format(WIDTH, HEIGHT))
        
        # Make a canvas
        canvas = Canvas(window, width=1920, height=1080, bg="#000000")
        canvas.pack()

    # Initialize an empty photo
    if not 'TRAVIS' in os.environ:
        img = PhotoImage(width=WIDTH, height=HEIGHT)
        
    if settings["output"].value != "unset":
        img_output = Image.new("RGB", (int(WIDTH), int(HEIGHT)))
        img_draw = PIL.ImageDraw.Draw(img_output)

    if not 'TRAVIS' in os.environ:
        canvas.create_image((int(WIDTH)/2, int(HEIGHT)/2), image=img, state="normal")

    # Render pixels on the photo 1 by 1
    i = 0
    for y in range(0, int(HEIGHT)):
        for x in range(0, int(WIDTH)):
            if not 'TRAVIS' in os.environ:
                img.put(rgbdata[i], (x,y))
            if settings["output"].value != "unset":
                img_draw.point((x,y), photoData[i])
            i+=1
    if settings["debug"].value == True:
        print(" success!")

    # Output image if necessary
    if settings["output"].value != "unset":
        export(img_output)

    if settings["debug"].value == True:
        print("Done > Total Bytes Processed: {:,}".format(i))

    
    # Show everything
    if not settings["quiet"].value == True:
        if not 'TRAVIS' in os.environ:
            mainloop()


# Init function
def init():
    """ Processes the command line arguments and starts the image 
    """
    if len(sys.argv) > 1:
        processCLI_Args(sys.argv[1:])

    if settings["help"].value:
        help()
        exit(0)

    if settings["path"].value == "unset":
        settings["path"].value = input("Please enter the path to the image data > ")
    
    if settings["width"].value == -1 and not settings["findx"]:
        settings["width"].value = int(input("Image width > "))
    elif settings["width"].value != -1 and not settings["findx"]:
        settings["width"].value = int(settings["width"])
    
    if settings["height"].value == -1 and not settings["findy"]:
        settings["height"].value = int(input("Image height > "))
    elif settings["height"].value != -1 and not settings["findy"]:
        settings["height"].value = int(settings["height"])

    
    render(settings["path"].value, settings["width"].value, settings["height"].value, settings["findx"].value, settings["findy"].value)
#----------------------------------------------------------------------


# Main 
init()

