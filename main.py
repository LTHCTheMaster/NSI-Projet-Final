# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from PIL import ImageTk, Image as pimg
from src.img_base import transformImg

BASE_TITLE = 'Image Lab' #donne un titre de base à l'image
current_title = BASE_TITLE
current_path = ''

pilImage = None
drawedPilImage = None

current_pal = [(255,255,255),(0,0,0)]

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

def drawImageOnCanvasFromEdit():
    basewidth = 960
    baseheight = 530
    global drawedPilImage
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

def edit_NegColor():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'n')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'n')
    drawImageOnCanvasFromEdit()

def edit_GreyScale():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'g')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'g')
    drawImageOnCanvasFromEdit()

def edit_ci_r():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'ci_r')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'ci_r')
    drawImageOnCanvasFromEdit()

def edit_ci_g():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'ci_g')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'ci_g')
    drawImageOnCanvasFromEdit()

def edit_ci_b():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'ci_b')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'ci_b')
    drawImageOnCanvasFromEdit()

def edit_kp_r():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'k_r')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'k_r')
    drawImageOnCanvasFromEdit()

def edit_kp_g():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'k_g')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'k_g')
    drawImageOnCanvasFromEdit()

def edit_kp_b():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'k_b')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'k_b')
    drawImageOnCanvasFromEdit()

def edit_med_rg():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'm_rg')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'm_rg')
    drawImageOnCanvasFromEdit()

def edit_med_rb():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'm_rb')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'm_rb')
    drawImageOnCanvasFromEdit()

def edit_med_gb():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'm_gb')
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'm_gb')
    drawImageOnCanvasFromEdit()

def getPalFile():
    pathi = askopenfilename(filetypes=[('Color Tables File', '*.pctby')])
    try:
        with open(pathi, 'r+') as pfile:
            pfile.write('')
            lines = pfile.readlines()
            pfile.close()
            global current_pal
            current_pal = []
            for i in lines:
                line = i.split(';')
                current_pal.append((int(line[0]),int(line[1]),int(line[2])))
    except:
        pass

def edit_pal():
    global drawedPilImage
    drawedPilImage = transformImg(drawedPilImage, 'c', 'p', color_list=current_pal)
    global pilImage
    pilImage = transformImg(pilImage, 'c', 'p', color_list=current_pal)
    drawImageOnCanvasFromEdit()

def closeWindow():
    try:
        window.destroy()
    except:
        exit()

window = Tk() #donne un titre de base, une icône et une résolution a la fenêtre
window.iconphoto(False, PhotoImage(file='res/icon.png'))
window.title(current_title)
window.geometry('960x540')

menu_bar = Menu(window)

file_bar = Menu(menu_bar, tearoff=0) #toutes les options  de la barre de menu
file_bar.add_command(label='Open', command=openFile)
file_bar.add_command(label='Save', command=saveFile)
file_bar.add_command(label='Save as', command=saveAsFile)
file_bar.add_command(label='Exit', command=closeWindow)

menu_bar.add_cascade(label='File', menu=file_bar)

edit_bar = Menu(menu_bar, tearoff=0)

color_bar = Menu(edit_bar, tearoff=0)

color_bar.add_command(label='Negative', command=edit_NegColor)
color_bar.add_command(label='Grey scale', command=edit_GreyScale)

ign_kep_bar = Menu(color_bar, tearoff=0)

ign_kep_bar.add_command(label='Ignore Red', command=edit_ci_r)
ign_kep_bar.add_command(label='Ignore Green', command=edit_ci_g)
ign_kep_bar.add_command(label='Ignore Blue', command=edit_ci_b)
ign_kep_bar.add_command(label='Keep Red', command=edit_kp_r)
ign_kep_bar.add_command(label='Keep Green', command=edit_kp_g)
ign_kep_bar.add_command(label='Keep Blue', command=edit_kp_b)

color_bar.add_cascade(label='Ignore Or Keep', menu=ign_kep_bar)

med_bar = Menu(color_bar, tearoff=0)

med_bar.add_command(label='Red & Green Median', command=edit_med_rg)
med_bar.add_command(label='Red & Blue Median', command=edit_med_rb)
med_bar.add_command(label='Green & Blue Median', command=edit_med_gb)

color_bar.add_cascade(label='Two Colors Median', menu=med_bar)

pal_bar = Menu(color_bar, tearoff=0)

pal_bar.add_command(label='Open Color Tables File', command=getPalFile)
pal_bar.add_command(label='Run Editing', command=edit_pal)

color_bar.add_cascade(label='Editing by Color Tables', menu=pal_bar)

edit_bar.add_cascade(label='Color', menu=color_bar)

menu_bar.add_cascade(label='Edit', menu=edit_bar)

window.config(menu=menu_bar)

canvas = Canvas(window,width=960,height=530)
canvas.pack()

window.mainloop()
