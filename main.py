# -*- coding: utf-8 -*-

from tkinter import *

BASE_TITLE = 'Image Lab'
current_title = BASE_TITLE

window = Tk()
window.iconphoto(False, PhotoImage(file='res/icon.png'))
window.title(current_title)
window.geometry('960x540')

window.mainloop()
