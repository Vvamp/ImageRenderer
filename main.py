from tkinter import *
from math import sin

def clamp(x): 
  return max(0, min(x, 255))


def loadData(imagePath, WIDTH, HEIGHT):
    print("> Opening image data...")
    dataFile = open(imagePath, "r")
    print("> Reading data...", end="")
    data = dataFile.read()
    print(" success!")

    print("> Parsing data...", end="")
    rgbdata = []
    for rgbval in data.split(' '):
        if(len(rgbval) <= 1):
            continue
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append("#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue)))
    print(" success!")

    print ("> Rendering Image...", end="")
    window = Tk()
    canvas = Canvas(window, width=1920, height=1080, bg="#000000")
    canvas.pack()
    img = PhotoImage(width=WIDTH, height=HEIGHT)
    canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")
    i = 0
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            img.put(rgbdata[i], (x,y))
            i+=1
    print(" success!")

    print("> Total Bytes Processed: {:,}".format(len(rgbdata)*2) )
    mainloop()


def init():
    imagePath = input("Please enter the path to the image data > ")
    width = int(input("Image width > "))
    height = int(input("Image height > "))

    loadData(imagePath, width, height)


init()