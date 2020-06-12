from tkinter import *
from math import sin
import math
import sys

settings ={
    "debug" : False,
    "findy" : False,
    "findx" : False,
    "path" : "unset",
    "width" : -1,
    "height" : -1
}

def processCLI_Args(args):
    flagValue = False
    flagValue_value = "None"
    for argument in args:
        if not flagValue:
            if argument[1:] not in settings.keys():
                print("Invalid argument '{}'. ".format(argument[1:]))
                return


        switches = ["debug", "findy", "findx"]
        setvals = ["path", "width", "height"]

        if argument[1:].lower() in switches:
            value = True
            settings[argument[1:].lower()] = value
        elif argument[1:].lower() in setvals:
            flagValue = True
            flagValue_value = argument[1:]
        elif flagValue:
            settings[flagValue_value] = argument
            flagValue_value = False


def clamp(x): 
  return max(0, min(x, 255))


def loadData(imagePath, WIDTH, HEIGHT, findX=False, findY=False):
    if settings["debug"] == True:
        print("File IO > Opening image data...")
    dataFile = open(imagePath, "r")
    
    if settings["debug"] == True:
        print("File IO > Reading data...", end="")
    data = dataFile.read()

    if settings["debug"] == True:
        print(" success!")

    if settings["debug"] == True:
        print("Parser > Parsing data...", end="")
    rgbdata = []
    i=0
    for rgbval in data.split(')'):
        if(len(rgbval) <= 1):
            continue
        i+=1
        if settings["debug"] == True:
            print("Parser > RGB bytes: {}".format(i))
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        rgbval = rgbval.replace('\n', '')
        rgbval = rgbval.replace(' ', '')
        if settings["debug"] == True:
            print(rgbval)
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append("#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue)))
    if settings["debug"] == True:
        print(" success!")
        print ("Renderer > Rendering Image...", end="")

    if findY:
        HEIGHT = abs(math.floor(len(rgbdata)/WIDTH))
    if findX:
        WIDTH = abs(math.floor(len(rgbdata)/HEIGHT))
   

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
    if settings["debug"] == True:
        print(" success!")

    if settings["debug"] == True:
        print("Done > Total Bytes Processed: {:,}".format(i))
    mainloop()


def init():
    if len(sys.argv) > 1:
        processCLI_Args(sys.argv[1:])

    if settings["path"] == "unset":
        settings["path"] = input("Please enter the path to the image data > ")
    
    if settings["width"] == -1 and not settings["findx"]:
        settings["width"] = int(input("Image width > "))
    elif settings["width"] != -1 and not settings["findx"]:
        settings["width"] = int(settings["width"])
    
    if settings["height"] == -1 and not settings["findy"]:
        settings["height"] = int(input("Image height > "))
    elif settings["height"] != -1 and not settings["findy"]:
        settings["height"] = int(settings["height"])

    loadData(settings["path"], settings["width"], settings["height"], settings["findx"], settings["findy"])


init()