#tkinter pythonda arayüz geliştirme kütüphanesidir.Bazı widgetlar tk nin içinbe bazıları ttk nın içidedir
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window=tk.Tk()
window.geometry("500x450")
window.title("Welcome to first app")


def buttonFunction():
    label.config(text="Hello World",fg="black",bg="red",font="Times 25")
    value=entry.get()#içine yazılan değerleri alırız
    label.configure(text=value)
    entry.configure(state="disabled")#input alımını kapatırız
    
    #message box
    #message_box=messagebox.showinfo(title="İnfo",message="information")
    #message_box=messagebox.askretrycancel(title="info",message="information")
    #message_box=messagebox.askquestion(title="info",message="information")
    #message_box=messagebox.askyesnocancel(title="info",message="information")
    message_box=messagebox.showerror(title="info",message="information")
#button
button=tk.Button(window,text="First Button",activebackground="red",bg="black",fg="white",activeforeground="black",
                 height=15,width=50,command=buttonFunction)#buton ekleme
button.pack()#widgetı pencereye ekleriz

#label
label=tk.Label(window,text="Hi World",font="Times 16",fg="white",bg="black")
label.pack(side=tk.RIGHT,padx=25)#>labelı sağa tarafa konumlandırır


#entry-->text box
entry=tk.Entry(window,width=50)
entry.insert(string="write something only one time",index=0)
entry.pack(side=tk.LEFT,padx=25)
window.mainloop()#pencerenin görünebilmesini sağlar


