from __future__ import print_function   
from PIL import Image
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
import time
os.environ['KERAS_BACKEND']='theano'
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

import CNN_ReadImg
padxlim = 320
padylim = 240
image_count=0
w=[]
pattern_in = np.ones((padylim,padxlim))
newCl=""
Cl="dog"

def output_res():
    global Cl,newCl,pattern_in,image_count
    Cl = newCl.get()
    print("New Type: %s\n" % (newCl.get()))
    img = Image.fromarray(pattern_in*255)
    if(img.mode!='RGB'):
        img = img.convert('RGB')
    img.save('data/test-'+str(image_count)+'-'+str(newCl.get())+'.bmp')
    image_count+=1

def drawdot(event):
    global w, pattern_in
    if(event.y >= padylim or event.x >= padxlim):
        return
    print("%d %d\n" % (event.y, event.x))
    pattern_in[event.y][event.x]=0
    x1, y1 = (event.x-1, event.y-1)
    x2, y2 = (event.x+1, event.y+1)
    w.create_oval(x1,y1,x2,y2)

def reset_bt():
    global pattern_in, w
    pattern_in = np.ones((padylim,padxlim))
    w.delete(tk.ALL)

def send_toCNN():
    global newCl, Cl
    g_pattern="It's "+Cl+"?"
    showinfo('Iguess...',g_pattern)
    if( askyesno('Is it correct?','Choose') ):
        showinfo(':)','Very good!')
    else:
        newWindow=tk.Toplevel()
        newWindow.title("Modify")
        tk.Label(newWindow,text="Correct catagory").pack()
        newCl = tk.Entry(newWindow)
        newCl.pack()
        tk.Button(newWindow, text="Submit", command=output_res).pack(fill=tk.X)

def retrain():
    pass

root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Painting Input")
w = tk.Canvas(root, width=padxlim, height=padylim)
w.pack(expand=tk.YES, fill=tk.BOTH)
w.bind("<B1-Motion>", drawdot)
submit=tk.Button(root,text="Submit",command=send_toCNN)
submit.pack(side=tk.LEFT)
reset=tk.Button(root,text="Reset",command=reset_bt)
reset.pack(side=tk.RIGHT)
cnnTrigger = tk.Button(root,text="Retrain",command=retrain)
cnnTrigger.pack(side=tk.BOTTOM)
tk.mainloop()
