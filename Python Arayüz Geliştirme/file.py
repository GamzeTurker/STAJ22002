import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


window=tk.Tk()
window.geometry("500x800")
#file dialog
def openFile():
    fileName=filedialog.askopenfilename(initialdir="C:/Users/Gamze/Desktop/Python ile Yapay Zeka",title="select a file..")
    img=Image.open(fileName)
    img=ImageTk.PhotoImage(img)
    label=tk.Label(window,image=img)
    label.image(img)
    label.pack(padx=15,pady=15)
button=tk.Button(window,text="open file",command=openFile)
button.pack()


#plot
fig=Figure(figsize=(5,4),dpi=50)
data=np.arange(0,3,0.1)
fig.add_subplot(111).plot(data,data*2+10)
canvas=FigureCanvasTkAgg(fig,master=window)
canvas.draw()
canvas.get_tk_widget().pack()

#mouse event

def leftClick(event):
    tk.Label(window,text="left").pack()
def middleClick(event):
    tk.Label(window,text="middle").pack()
    
def rightClick(event):
    tk.Label(window,text="right").pack()

window.bind("<Button-1>",leftClick)#tek tıklama sol
window.bind("<Button-2>",middleClick)
window.bind("<Button-3>",rightClick)

window.mainloop()