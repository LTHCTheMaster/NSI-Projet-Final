# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image as pimg

BASE_TITLE = 'Image Lab' #donne un titre de base à l'image
current_title = BASE_TITLE
current_path = ''

pilImage = None
drawedPilImage = None

def update_path(new_path): #mettre a jour le chemin du fichier actuel
    global current_path
    current_path = new_path

def drawImageOnCanvasFromOpen(): #permet d'afficher l'image
    global pilImage
    pilImage = pimg.open(current_path)
    global drawedPilImage
    drawedPilImage = pilImage
    wd, hg = pilImage.size
    basewidth = 960
    baseheight = 530
    if not (wd <= basewidth and hg <= baseheight):
        #Generate the wd ratio
        ratio = basewidth / wd
        hsize = int(hg * ratio)
        #check hg from wd ratio
        if hsize <= baseheight:
            drawedPilImage = drawedPilImage.resize((basewidth, hsize), pimg.ANTIALIAS)
        else:
            #Generate the hg ratio
            ratio = baseheight / hg
            wsize = int(wd * ratio)
            #check wd from hg ratio
            if wsize <= basewidth:
                drawedPilImage = drawedPilImage.resize((wsize, baseheight), pimg.ANTIALIAS)
            else:
                drawedPilImage = drawedPilImage.resize((basewidth, baseheight), pimg.ANTIALIAS)
    
    image = ImageTk.PhotoImage(drawedPilImage)
    imagesprite = canvas.create_image(basewidth // 2 + 1, baseheight // 2 + 1, image=image)
    imagesprite.pack()

def openFile(): #permet d'ouvrir une image
    pathi = askopenfilename(filetypes=[('Image File', '*.jpg')])
    update_path(pathi)
    global current_title
    current_title = BASE_TITLE + ' > ' + current_path
    window.title(current_title)
    drawImageOnCanvasFromOpen()
    
def saveAsFile(): #permet de sauvegarder sous une image 
    pathi = asksaveasfilename(filetypes=[('Image File', '*.jpg')])
    pilImage.save(pathi)
    
def saveFile(): #permet de sauvegarder une image
    if current_path == '':
        saveAsFile()
    else:
        pilImage.save(current_path)

window = Tk() #donne un titre de base, une icône et une résolution a la fenêtre
window.iconphoto(False, PhotoImage(file='res/icon.png'))
window.title(current_title)
window.geometry('960x540')

menu_bar = Menu(window)

file_bar = Menu(menu_bar, tearoff=0) #toutes les options  de la barre de menu
file_bar.add_command(label='Open', command=openFile)
file_bar.add_command(label='Save', command=saveFile)
file_bar.add_command(label='Save as', command=saveAsFile)
file_bar.add_command(label='Exit', command=window.destroy)

menu_bar.add_cascade(label='File', menu=file_bar)

window.config(menu=menu_bar)

canvas = Canvas(window,width=960,height=530)
canvas.pack()

window.mainloop()
