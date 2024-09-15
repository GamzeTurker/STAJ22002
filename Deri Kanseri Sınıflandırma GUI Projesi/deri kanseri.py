#kullanıcı arayüzü kütüphaneleri
import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog
from tkinter import messagebox
#python ımage library
from PIL import ImageTk,Image #resimleri alabilmemiz için
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
#CNN 
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam


#%%
deri_df=pd.read_csv("C:/Users/Gamze/Desktop/Python ile Yapay Zeka/Deri Kanseri Sınıflandırma/HAM10000_metadata.csv")
deri_df.head()
deri_df.info()
#sns.countplot(x="dx",data=deri_df)#kaç tane kanser hücresi sınıfının olduğunu gösterir

#%% preprocess(ön işlem)
veri_klasoru=("C:/Users/Gamze/Desktop/Python ile Yapay Zeka/Deri Kanseri Sınıflandırma/HAM10000_images_part_1/")
ext=".jpg"

#veri_klasoru+image_id[i]+ext
deri_df["path"]=[veri_klasoru + i + ext for i in deri_df["image_id"]]#yeni bir kolon oluşturduk resimlerin dosya yolunu tutan
deri_df["image"] = deri_df["path"].map(lambda x: np.asarray(Image.open(x).resize((100, 75))))#deri_df path içindeki herbir satırı fonksiyon yapar
#plt.imshow(deri_df["image"][0])

deri_df["dx_idx"]=pd.Categorical(deri_df["dx"]).codes

# standardization
x_train=np.asarray(deri_df["image"].to_list())
x_train_mean=np.mean(x_train)
x_train_std=np.std(x_train)
x_train=(x_train-x_train_mean)/x_train_std #x_traine standardization yapıldı

#one hot encoding
y_train=to_categorical(deri_df["dx_idx"],num_classes=7)#7 sınıfı olan dx_idx sütununa one hot encoding uygulandı


#%% CNN

input_shape = (75,100,3)
num_classes = 7

model = Sequential()
model.add(Conv2D(32, kernel_size = (3,3), activation = "relu", padding = "Same", input_shape = input_shape))
model.add(Conv2D(32, kernel_size = (3,3), activation = "relu", padding = "Same"))
model.add(MaxPool2D(pool_size = (2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size = (3,3), activation = "relu", padding = "Same"))
model.add(Conv2D(64, kernel_size = (3,3), activation = "relu", padding = "Same"))
model.add(MaxPool2D(pool_size = (2,2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(128,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(num_classes,activation="softmax"))
model.summary()

optimizer = Adam(learning_rate = 0.0001)
model.compile(optimizer = optimizer, loss = "categorical_crossentropy", metrics = ["accuracy"])

epochs = 5
batch_size = 25

history = model.fit(x = x_train, y = y_train, batch_size = batch_size, epochs = epochs, verbose = 1, shuffle = True)

model.save("my_model2.keras")

# %% load
model1 = load_model(r"C:\Users\Gamze\Desktop\Python ile Yapay Zeka\Deri Kanseri Sınıflandırma\my_model1.keras")
model2 = load_model(r"C:\Users\Gamze\Desktop\Python ile Yapay Zeka\Deri Kanseri Sınıflandırma\my_model2.keras")

#%%prediction
index=5
y_pred=model1.predict(x_train[index].reshape(1,75,100,3))
y_pred_class = np.argmax(y_pred, axis = 1)

#%%
window=tk.Tk()
window.geometry("1080x640")
window.title("Deri  Kanseri Sınıflandırma")

##global variables
img_name=" "
count=0
img_jpg=""
##frames
frame_left=tk.Frame(window,width=540,height=640,bd="2")
frame_left.grid(row=0,column=0)

frame_right=tk.Frame(window,width=540,height=640,bd="2")
frame_right.grid(row=0,column=1)

frame1=tk.LabelFrame(frame_left,text="Image",width=540,height=500)#resimleri alıcağımız bölüm
frame1.grid(row=0,column=0)

frame2=tk.LabelFrame(frame_left,text="Model and Save",width=540,height=140)#modelleri seçeceğimiz bölüm
frame2.grid(row=1,column=0)

frame3=tk.LabelFrame(frame_right,text="Features",width=270,height=640)#özelliklerin olduğu bölüm
frame3.grid(row=0,column=0)

frame4=tk.LabelFrame(frame_right,text="Result",width=270,height=640)#tahmin sonuçlarının olduğu bölüm
frame4.grid(row=0,column=1,padx=10)

#frame1
def imageResize(img):
    basewidth=500
    wpercent=(basewidth/float(img.size[0]))#1000*1200
    hSize=int(float(img.size[1]*float(wpercent)))
    img=img.resize((basewidth,hSize),Image.Resampling.LANCZOS)
    return img
def openImage():
    global img_name
    global count
    global img_jpg
    count+=1
    if(count!=1):
        messagebox.showinfo(title="Warning",message="Sadece bir tane resim seçiniz")
    else:
        img_name=filedialog.askopenfilename(initialdir="C:/Users/Gamze/Desktop/Python ile Yapay Zeka/Deri Kanseri Sınıflandırma/")
        img_jpg = img_name.split("/")[-1].split(".")[0]
        tk.Label(frame1,text=img_jpg,bd=3).pack(pady=10)
        
        #open and image show
        img=Image.open(img_name)
        img=imageResize(img)
        img=ImageTk.PhotoImage(img)
        panel=tk.Label(frame1,image=img)
        panel.image=img
        panel.pack(padx=15,pady=10)
        
        #image feature
        data=pd.read_csv(r"C:\Users\Gamze\Desktop\Python ile Yapay Zeka\Deri Kanseri Sınıflandırma\HAM10000_metadata.csv")
        cancer=data[data.image_id==img_jpg]
        for i in range(cancer.size):
            x=0.4
            y=(i/10)/2
            tk.Label(frame3,font=("Times",12),text=str(cancer.iloc[0,i])).place(relx=x,rely=y)

        
menubar=tk.Menu(window)
window.config(menu=menubar)
file=tk.Menu(menubar)
menubar.add_cascade(label="File",menu=file)
file.add_command(label="Open",command=openImage)

#frame3
def classification():
    if img_name !=" " and models.get() !=" ":
        if models.get()=="Model1" :
            classification_model=model1
            
        else:
            classification_model=model2
        z=deri_df[deri_df.image_id==img_jpg]
        z=z.image.values[0].reshape(1,75,100,3)
        z=(z-x_train_mean)/x_train_std
        h=classification_model.predict(z)[0]
        h_index=np.argmax(h)
        predicted_cancer=list(deri_df.dx.unique())[h_index]
        for i in range(len(h)):
            x=0.5
            y=(i/10)/2
            if i!=h_index:
                tk.Label(frame4,text=str(h[i])).place(relx=x,rely=y)
            else:
                tk.Label(frame4,bg="green",text=str(h[i])).place(relx=x,rely=y)
        if chvar.get()==1:#modelden çıkan sonuçları kaydetme
            val=entry.get()
            entry.config(state="disable")#metin geldikten sonra entrye bir şey eklenemez
            path_name=val+".txt"#sonucu txt şeklinde kaydederiz
            save_txt=img_name+"--" +str(predicted_cancer)
            text_file=open(path_name,"w")#dosyayı açarız ve yazma işlemi olacağını belirtiriz,
            text_file.write(save_txt)#içine yazılacak değer
            text_file.close()#dosyayı kapatırız
        else:
            print("Save is not selected")
           
    else:
        messagebox.showinfo(title="Warning",message="Choose image and Model First!")#resim seçilmediğinde uyarı mesajı verir
        tk.Label(frame3,text="Choose image and Model First!").place(relx=0.1,rely=0.6)
columns=["lesion_id","image_id","dx","dx_type","age","sex","localization"]
for i in range(len(columns)):
    x=0.1
    y=(i/10)/2
    tk.Label(frame3,font=("Times",12),text=str(columns[i])+":").place(relx=x,rely=y)
classify_button=tk.Button(frame3,bg="red",bd=4,font=("Times",13),activebackground="orange",text="Classify",command=classification)
classify_button.place(relx=0.1,rely=0.5)


#frame4
labels=deri_df.dx.unique()
for i in range(len(columns)):
    x=0.1
    y=(i/10)/2
    tk.Label(frame4,font=("Times",12),text=str(labels[i])+":").place(relx=x,rely=y)

#frame2
#combo box
model_selection_label=tk.Label(frame2,text="Sınıflandırma Modelini Seçiniz:")
model_selection_label.grid(row=0,column=0,padx=5)
models=tk.StringVar()
model_selection=ttk.Combobox(frame2,textvariable=models,values=( "Model1","Model2"),state="readonly")
model_selection.grid(row=0,column=1,padx=5)

#check box
chvar=tk.IntVar()
chvar.set(0)
xbox=tk.Checkbutton(frame2,text="Save Classification Result",variable=chvar)
xbox.grid(row=1,column=0,pady=5)

entry=tk.Entry(frame2,width=25)
entry.insert(string="Saving name...",index=0)
entry.grid(row=1,column=1)
window.mainloop()