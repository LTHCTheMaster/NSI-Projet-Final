# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image as pimg

BASE_TITLE = 'Image Lab'
current_title = BASE_TITLE
current_path = ''

pilImage = None

def update_path(new_path):
    global current_path
    current_path = new_path

def drawImageOnCanvasFromOpen():
    global pilImage
    pilImage = pimg.open(current_path)
    basewidth = 960
    wpercent = (basewidth / float(pilImage.size[0]))
    hsize = int((float(pilImage.size[1]) * float(wpercent)))
    pilImage = pilImage.resize((basewidth, hsize), pimg.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(basewidth // 2 + 1, hsize // 2 + 1, image=image)
    imagesprite.pack()

def openFile():
    pathi = askopenfilename(filetypes=[('Image File', '*.jpg')])
    update_path(pathi)
    global current_title
    current_title = BASE_TITLE + ' > ' + current_path
    window.title(current_title)
    drawImageOnCanvasFromOpen()
    
def saveAsFile():
    pathi = asksaveasfilename(filetypes=[('Image File', '*.jpg')])
    pilImage.save(pathi)

window = Tk()
window.iconphoto(False, PhotoImage(file='res/icon.png'))
window.title(current_title)
window.geometry('960x540')

menu_bar = Menu(window)

file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label='Open', command=openFile)
file_bar.add_command(label='Save as', command=saveAsFile)
file_bar.add_command(label='Exit', command=window.destroy)

menu_bar.add_cascade(label='File', menu=file_bar)

window.config(menu=menu_bar)

canvas = Canvas(window,width=960,height=530)
canvas.pack()

window.mainloop()
