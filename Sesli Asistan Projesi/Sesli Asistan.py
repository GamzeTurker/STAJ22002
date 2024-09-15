import random
from gtts import gTTS #google metin konuşmaları için kullanılır
from playsound import playsound #mp3 ve vav uzantılı dosyaları çalıştıran kütüphane
import pyaudio #mikrofandan gelen veriyi işlemek ve kaydetmek için kullanılır
import speech_recognition as sr #mikrofondan aldığı sesi yazıya dönüştürür
import os
import time
#internet işlemleri için selenium kütüphanesi kullanırız
from selenium import  webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests #internet üzerinden veri çekmeye yarayan kütüphane
from bs4 import BeautifulSoup #çeklen verilirin anlamlı ve okunabilir hale getirilmesini sağlayan kütüphane
import cv2
import tkinter as tk
from tkinter import messagebox
import threading
r=sr.Recognizer()#dediklerimiz algılanır
confirm_word_ = ["evet","onaylıyorum","doğru","evet bu numara"]
#sesli asistanı konuşturma
class SesliAsistan:
    def seslendirme(self,metin):
        #gTTs iki parametre alır text->metin lang->hangi dilde seslendireceği
        metin_seslendirme=gTTS(text=metin,lang="tr")
        #mp3 uzantılı ses dosyası oluşturduk.Sesli asistan gönderilen metni telaffuz edip ses dosyasını içine  kaydedecek  #ses dosyası ismi sürekli farklı olmak zorunda 
        dosya=str(random.randint(0,1000000000))+".mp3"#sesli dosyamız kaydedilecek
        metin_seslendirme.save(dosya) #dosyaya metin sesini kaydediriz
        playsound(dosya)#dosyayı okuturuz
        os.remove(dosya)#dosya okunduktan sonra silinecek.Sürekli dosya oluşturmaması için.
#mikrofana söylenenleri metin olarak yazdırma
    def mikrofon(self):
           with sr.Microphone() as kaynak: #mikrofana erişim sağlarız
               #print("Sizi dinliyorum...")
               
               pencere.update_idletasks()  # Pencereyi güncelle
               listen=r.listen(kaynak)#mikrofandan gelen sesleri dinleyecek
               ses=""
               try:
                   ses=r.recognize_google(listen,language="tr-TR") #algılamayı hangi dilde yapacağı.Deninenleri string olarak geri alıcaz
               except sr.UnknownValueError:#denileni algılayamama hatası
                   self.seslendirme("ne dediğinizi anlayamadım.")
                   etiket.config(text="Ne dediğinizi anlayamadım")
               return ses 
    def ses_karsilik(self,gelen_ses):#gelen sese karşılık verme
        if(gelen_ses in "Merhaba"):
             etiket.config(text="Size de merhabalar")
             self.seslendirme("Size de merhabalar")
        elif(gelen_ses in "nasılsın"):
             etiket.config(text="İyiyim siz nasılsınız")
             self.seslendirme("iyiyim siz nasılsınız")
        elif(gelen_ses in "müzik aç" or gelen_ses in "video aç" ):
            etiket.config(text="Müzik Açıyorum")
            self.muzikAc()
        elif(gelen_ses in "google aç" or  gelen_ses in "arama yap"):
            etiket.config(text="Arama Yapıyorum")
            self.google()
        elif(gelen_ses in "film öner" or gelen_ses in "film önerisi yap"):
            etiket.config(text="Film Açıyorum")
            self.filmAc()
        elif (gelen_ses in "hava durumu"):
            etiket.config(text="Hava Durumu")
            self.havaDurumu()
        elif (gelen_ses in "Fotoğraf çek"):
            etiket.config(text="Fotoğraf Çekiyorum")
            self.fotograf()
        elif (gelen_ses in "Oyun aç"):
            etiket.config(text="Oyun Açıyorum")
            self.oyunAc()
        elif (gelen_ses in "mesaj at"):
            etiket.config(text="Mesaj Atıyorum")
            self.whatsApp()         
    def muzikAc(self):
         try:
               self.seslendirme("ne açmamı istersiniz")
               cevap=self.mikrofon()
               url="https://www.youtube.com/results?search_query="+cevap
               tarayici=webdriver.Chrome()
               tarayici.get(url)
               ilk_video=tarayici.find_element(By.XPATH,"//*[@id='video-title']/yt-formatted-string").click()
               time.sleep(5)
               self.seslendirme("istediğiniz içerik bu mu ")
               gelen_komut=self.mikrofon()
               if(gelen_komut in "Hayır"):
                   sayac=2
                   tarayici.back()
                   while(sayac<5):
                       diger_videolar=tarayici.find_element(By.XPATH,f"//*[@id='contents']/ytd-video-renderer[{sayac}]").click()
                       time.sleep(5)
                       self.seslendirme("istediğiniz içerik bu mu")
                       komut=self.mikrofon()
                       if(komut in "Evet"):
                           self.seslendirme("keyifli vakit geçirmeler...")
                           break
                       else:
                           self.seslendirme("o zaman diğer videolara bakalım")
                           tarayici.back()
                           sayac+=1
               else:
                   self.seslendirme("keyifli vakit geçirmeler...")
         except:
             self.seslendirme("bir hata meydana geldi.lütfen daha sonra tekrar deneyiniz")
    def google(self):
         self.seslendirme("ne aramamı istersiniz")
         cevap=self.mikrofon()
         url="https://www.google.com/search?q="+cevap
         self.seslendirme("{} ile ilgili bulduğum içerik bunlar".format(cevap))
         tarayici=webdriver.Chrome()
         tarayici.get(url)
         site=tarayici.find_element(By.XPATH,"//*[@id='rso']//h3").click()#ilk siteye tıklar
         time.sleep(10)
         tarayici.quit()
         
    def filmAc(self):
        try:
            self.seslendirme("hangi tür film istersiniz")
            cevap=self.mikrofon()
            if (cevap == "bilim kurgu"):
                cevap = "bilim-kurgu-filmleri-izle"
            elif (cevap == "aile"):
                cevap = "aile-filmleri-izle"
            elif (cevap == "aksiyon"):
                cevap = "aksiyon-filmleri-izle"
            elif (cevap == "romantik"):
                cevap = "romantik-filmler-hd-izle"
            elif (cevap == "suc"):
                cevap = "suc-filmleri-izle"
            elif (cevap == "psikolojik"):
                cevap = "psikolojik-filmler-izle"
            elif (cevap == "savaş"):
                cevap = "savas-filmleri-izle"
            elif (cevap == "korku"):
                cevap = "korku-filmleri-izle"
            elif (cevap == "gerilim"):
                cevap = "gerilim-filmleri-hd-izle"
            elif (cevap == "komedi"):
                cevap = "komedi-filmleri-hd-izle"
            elif (cevap=="animasyon"):
                cevap="animasyon-filmleri-izle"
            else:
                cevap="populer-filmler" #eğer farklı bir komut gelirse doğrudan yabancı filmlere gidelim

            tarayici=webdriver.Chrome()
            tarayici.get("https://www.fullhdfilmizlesene.de/filmizle/{}".format(cevap))
            ilk_kart=tarayici.find_element(By.XPATH,"/html/body/div[5]/div[1]/main/section/ul/li[1]").click()
            time.sleep(3)
            self.seslendirme("bu film uygun mu")
            gelen_cevap=self.mikrofon()
            if(gelen_cevap in "hayır"):
                self.seslendirme("o zaman diğer filmlere bakalım")
                tarayici.back()
                sayac=2
                while (sayac<10):
                    diger_filmler=tarayici.find_element(By.XPATH,"/html/body/div[5]/div[1]/main/section/ul/li[{}]".format(sayac)).click()
                    time.sleep(4)
                    self.seslendirme("bu film uygun mu")
                    komut=self.mikrofon()
                    if(komut in "evet"):
                        self.seslendirme("keyifli seyirler")
                        time.sleep(5)
                        break
                    else:
                        self.seslendirme("o zaman diğer filmlere bakalım")
                        tarayici.back()
                        sayac+=1
            else:
                 self.seslendirme("keyifli seyirler")
                 time.sleep(5)
        except  :
              self.seslendirme("bir hata meydana geldi")
    def havaDurumu(self):
          self.seslendirme("hangi şehrin hava durumunu istersiniz")
          cevap=self.mikrofon().lower()
          print(cevap)
          def HavaRaporlari(gununIndeksi):
              url="https://havadurumu15gunluk.xyz/havadurumu/630/ {} -hava-durumu-15-gunluk.html".format(cevap)
              response=requests.get(url)
              if(response.status_code==200):#ise internet üzerinden veriler başarılı bir şekilde gelmiştir
                  #print("işlem başarılı")
                  
                  #gelen verileri işleme     
                  soup=BeautifulSoup(response.text,"html.parser")#İlk parametre verilerin metin şeklinde gelmesini sağlar.İkinci parametre parçalamaya ve daha iyi okunabilir hale gelmesini sağlar
                  #print(soup)
                  tumVeriler=soup.find_all("tr")[gununIndeksi].text#tr olan satır kodlarını alır
                  tumVeriler=tumVeriler.replace("Saatlik"," ").strip()
                 
                  print(tumVeriler)
                  gunluk_hava=" "
                  gunduzSicaklik=tumVeriler[-6:-4]
                  geceSicaklik=tumVeriler[-3:-1]
                  print("Gündüz Sıcaklık:",gunduzSicaklik)
                  print("Gece Sıcaklık:",geceSicaklik)
                  gun=["Bugün","Yarın"]
                  
                  if not any(g in tumVeriler for g in gun):
                      tumVeriler=tumVeriler[6:-6].strip()
                      gunun_ismi=tumVeriler[:3]
                      gunKısaltma=["Sal","Çar","Per","Cum","Cmt","Paz","Pzt"]
                      for x in gunKısaltma:
                          if x in tumVeriler:
                              gunluk_hava=tumVeriler.replace(x," ")
                      print("Hava durumu "+gunluk_hava)
                      gununİsimleri={"Paz":"Pazartesi","Sal":"Salı","Çar":"Çarşamba","Per":"Perşembe","Cum":"Cuma","Cmt":"Cumartesi","Paz":"Pazar"}
                      gunun_ismi=gununİsimleri[gunun_ismi]
                      print("Günün Adı:",gunun_ismi)
                      return "{} için {} hava raporları şu şekilde:Hava: {} Gündüz sıcaklığı: {}  derece Gece Sıcaklığı:{} ".format(cevap,gunun_ismi,gunluk_hava,gunduzSicaklik,geceSicaklik)
                  else:
                      tumVeriler=tumVeriler[0:-6].strip()
                      gunun_ismi = tumVeriler[:5]
                      print("Günün İsmi:",gunun_ismi)
                      for g in gun:
                          gunluk_hava = tumVeriler.replace(g, " ")
                      print("Hava durumu :"+gunluk_hava) 
                      return "{} için {} hava raporları şu şekilde:Hava: {} Gündüz sıcaklığı: {}  derece Gece Sıcaklığı:{} ".format(cevap,gunun_ismi,gunluk_hava,gunduzSicaklik,geceSicaklik)
              else:
                  print("Hata meydana geldi")#bazı web siteleri veri çekmye izin vermeyebilir.Ya da internet kaynaklı hatalar
          self.seslendirme("{} şehir için yarının mı yoksa 5 günlük raporlarını mı istersiniz" .format(cevap))
          cevap2=self.mikrofon()
          if(cevap2 == "yarının"):
              self.seslendirme(HavaRaporlari(2))
         

          else:
             sayac=1
             while sayac<6:
                 self.seslendirme(HavaRaporlari(sayac))
                 sayac+=1
    def fotograf(self):
         self.seslendirme("kameranızı hemen açıyorum")
         kamera=cv2.VideoCapture(0)
         kontrol,resim=kamera.read()
         self.seslendirme("gülümseyin çekiyorum")
         cv2.imwrite("deneme.jpg",resim)
         kamera.release()
         cv2.destroyAllWindows()
         time.sleep(2)
         self.seslendirme("fotoğrafınızı görmek istiyor musunuz")
         cevap=self.mikrofon()
         if (cevap in "Evet"):
             resim=cv2.imread("deneme.jpg")
             cv2.imshow("Deneme Resim 1:",resim)
             cv2.waitKey(0)
             cv2.destroyAllWindows()
    def oyunAc(self):
        self.seslendirme("hangi oyunu açmamı istersiniz")
        cevap=self.mikrofon()
        if(cevap in "araba oyunu"):
            self.seslendirme("oyununuzu hemen açıyorum")
            os.startfile("C:\\Users\\Gamze\\Desktop\\Asphalt 9 Legends.lnk")
    def whatsApp(self):
        tarayici=webdriver.Chrome()
        tarayici.get("https://web.whatsapp.com/")
        self.seslendirme("Lütfen QR kodu taratın ve Enter tuşuna basın.")
        input("Lütfen QR kodu taratın ve Enter tuşuna basın.")
        self.seslendirme("Kime mesaj göndermek istersiniz?")
        kisi = self.mikrofon()
        self.seslendirme(f"{kisi} kişisine ne mesajı göndermek istersiniz?")
        mesaj = self.mikrofon()
        self.seslendirme("{} kişisine '{}' mesajını gönderiliyor ".format(kisi,mesaj))
        search_box = tarayici.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        search_box.click()
        search_box.send_keys(kisi)
        search_box.send_keys(Keys.RETURN)
        message_box =tarayici.find_element(By.XPATH,  "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]")
        message_box.click()
        message_box.send_keys(mesaj)
        message_box.send_keys(Keys.RETURN)
        self.seslendirme("Mesaj başarıyla gönderildi.")
        tarayici.quit()
    def uyanma_fonksiyonu(self,gelen_ses):
         
         if (gelen_ses in "hey junior"):
             text=self.seslendirme("Dinliyorum")
             etiket.config(text="Dinliyorum...")
             while True:
                 ses=self.mikrofon()
                 if(ses !=""):
                     self.ses_karsilik(ses)
                     
                 else:
                     return False    
def sesli_asistan_aktif():
    global asistan_aktif
    while asistan_aktif:
        etiket.config(text="Sizi dinliyorum")
        gelen_ses = asistan.mikrofon().lower()
        if gelen_ses != "":
            print(gelen_ses)
            asistan.uyanma_fonksiyonu(gelen_ses)
# Pencereyi kapatma işlevi
def pencereyi_kapat():
    global asistan_aktif
    asistan_aktif = False  # İş parçacığını durdurmak için bayrak
    pencere.destroy()  # Pencereyi kapat             
pencere=tk.Tk()        
pencere.title("Sesli Asistan Junior")
pencere.geometry("400x400")

etiket = tk.Label(pencere, font=("Arial", 16), wraplength=300)
etiket.place(relx=0.5, rely=0.5, anchor='center')
# Sesli asistan nesnesi oluştur
asistan = SesliAsistan()
asistan_aktif=True
# Sesli asistanı ayrı bir iş parçacığında başlat
asistan_thread = threading.Thread(target=sesli_asistan_aktif, daemon=True)
asistan_thread.start()
# Pencere kapandığında çağrılacak işlev
pencere.protocol("WM_DELETE_WINDOW", pencereyi_kapat)

pencere.mainloop()

        
    

