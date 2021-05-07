# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image as pimg

BASE_TITLE = 'Image Lab'
current_title = BASE_TITLE
current_path = ''

def update_path(new_path):
    global current_path
    current_path = new_path

def openFile():
    path = askopenfilename(filetypes=[('Image File', '*.jpg')])
    update_path(path)
    global current_title
    current_title = BASE_TITLE + ' > ' + current_path
    window.title(current_title)

window = Tk()
window.iconphoto(False, PhotoImage(file='res/icon.png'))
window.title(current_title)
window.geometry('960x540')

menu_bar = Menu(window)

file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label='Open', command=openFile)
file_bar.add_command(label='Exit', command=window.destroy)

menu_bar.add_cascade(label='File', menu=file_bar)

window.config(menu=menu_bar)

canvas = Canvas(window,width=960,height=530, bg='#FFDD00')
canvas.pack()

window.mainloop()
