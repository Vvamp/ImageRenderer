from tkinter import *
from math import sin
import math
import sys

PROGRAM_AUTHOR="Vincent van Setten"
PROGRAM_NAME="RGB Renderer"
PROGRAM_VERSION="0.4.2"

class setting:
    def __init__(self, name: str, description: str, isSwitch: bool, value, usage="", synonyms=[]):
        self.name = name
        self.description = description
        self.isSwitch = isSwitch 
        self.value = value
        self.usage = usage 
        self.synonyms = synonyms

settings ={
    "debug"     : setting("debug", "Toggles debugging output.", True, False, "render.py --debug", ['-debug', 'd']),
    "findy"     : setting("findx", "Make the program find the correct height based on the width. If the width is also unknown, it makes a square image.", True, False, "render.py --findx", ['-findx', 'x']),
    "findx"     : setting("findy", "Makes the program find the correct width based on the height. If the height is also unknown, it makes a square image.", True, False, "render.py --findy", ['-findy', 'y']),
    "help"      : setting("help", "Shows this help menu.", True, False, "render.py --help", ['-help', 'h']),
    "path"      : setting("path", "Sets the path to the image path. This file has to be in raw text and should contain RGB data.", False, "unset", "render.py --path <path_to_file>", ['-path', '-file', 'f']),
    "width"     : setting("width", "Set the width of the image.", False, -1, "render.py --width <width>", ['-width']),
    "height"    : setting("height", "Set the height of the image.", False, -1, "render.py --height", ['-height'])
}

def processCLI_Args(args):
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


def clamp(x): 
  return max(0, min(x, 255))


def help():
    print("{}@{} by {}".format(PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_AUTHOR))
    print("\n[NAME]\t[FLAGS]\t\t\t[DESCRIPTION]")
    for _setting in settings.values():
        print("{}\t{}\t\t{}\n\tUsage: {}".format(_setting.name, _setting.synonyms, _setting.description, _setting.usage), end="\n\n")
    print("usage: python render.py [options]")


def loadData(imagePath, WIDTH, HEIGHT, findX=False, findY=False):
    if settings["debug"].value == True:
        print("File IO > Opening image data...")
    dataFile = open(imagePath, "r")
    
    if settings["debug"].value == True:
        print("File IO > Reading data...", end="")
    data = dataFile.read()

    if settings["debug"].value == True:
        print(" success!")

    if settings["debug"].value == True:
        print("Parser > Parsing data...", end="")
    rgbdata = []
    i=0
    for rgbval in data.split(')'):
        if(len(rgbval) <= 1):
            continue
        i+=1
        if settings["debug"].value == True:
            print("Parser > RGB bytes: {}".format(i))
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        rgbval = rgbval.replace('\n', '')
        rgbval = rgbval.replace(' ', '')
        if settings["debug"].value == True:
            print(rgbval)
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append("#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue)))
    if settings["debug"].value == True:
        print(" success!")
        print ("Renderer > Rendering Image...", end="")

    if findY == True and findX == False:
        HEIGHT = abs(math.floor(len(rgbdata)/WIDTH))
    elif findX == True and findY == False:
        WIDTH = abs(math.floor(len(rgbdata)/HEIGHT))
    elif findX and findY:
        HEIGHT = math.floor(math.sqrt(len(rgbdata)))
        WIDTH = HEIGHT

    window = Tk()
    window.title("Image {}x{}".format(WIDTH, HEIGHT))
    canvas = Canvas(window, width=1920, height=1080, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=WIDTH, height=HEIGHT)
    canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")
    i = 0
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            img.put(rgbdata[i], (x,y))
            i+=1
    if settings["debug"].value == True:
        print(" success!")

    if settings["debug"].value == True:
        print("Done > Total Bytes Processed: {:,}".format(i))
    mainloop()


def init():
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

    
    loadData(settings["path"].value, settings["width"].value, settings["height"].value, settings["findx"].value, settings["findy"].value)


init()