from tkinter import *
from math import sin
dataFile = open("data3.txt",  'r')

def clamp(x): 
  return max(0, min(x, 255))

WIDTH, HEIGHT = 1920, 1080

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

data = dataFile.read()
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


for x in range(0, 120):
    for y in range(0, 160):
        img.put(rgbdata[x+y], (x,y))

mainloop()