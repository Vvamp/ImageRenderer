from tkinter import *
from math import sin

def clamp(x): 
  return max(0, min(x, 255))


def loadData(imagePath, WIDTH, HEIGHT):
    print("File IO > Opening image data...")
    dataFile = open(imagePath, "r")
    print("File IO > Reading data...", end="")
    data = dataFile.read()
    print(" success!")

    print("Parser > Parsing data...", end="")
    rgbdata = []
    i=0
    for rgbval in data.split(')'):
        if(len(rgbval) <= 1):
            continue
        i+=1
        print("Parser > RGB bytes: {}".format(i))
        rgbval = rgbval.replace('(', '')
        rgbval = rgbval.replace(')', '')
        rgbval = rgbval.replace('\n', '')
        rgbval = rgbval.replace(' ', '')
        print(rgbval)
        red = int(rgbval.split(',')[0])
        green = int(rgbval.split(',')[1])
        blue = int(rgbval.split(',')[2])
        rgbdata.append("#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue)))
    print(" success!")

    print ("Renderer > Rendering Image...", end="")
    window = Tk()
    window.title("Image {}x{}".format(WIDTH, HEIGHT))
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

    print("Done > Total Bytes Processed: {:,}".format(i))
    mainloop()


def init():
    imagePath = input("Please enter the path to the image data > ")
    width = int(input("Image width > "))
    height = int(input("Image height > "))

    loadData(imagePath, width, height)


init()