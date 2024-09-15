import pandas as pd
import yfinance as yf #yahoofinance(finansal verialtyapısı) veri çekmemizi sağlar
import streamlit as st #web tabanlı data uygulamalarının yazılmasını  sağlayan framework
import datetime
from datetime import timedelta,datetime
from prophet import Prophet
import base64
import matplotlib.pyplot as plt
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric

#facebook prophet ile tahmin yapma->facebook prophet faaceebook ml için kullandığı framework.Scikit learn tabanlı


st.title("Finansal Analiz ")
st.write("Data Analizi ve Görselleştirmesi Paneli")#metin
st.sidebar.title("Filtrele")

#data=yf.Ticker("BTC-USD")#bitcion verilerini  çekeriz
#df=data.history(period="1d",start="2010-02-21",end="2021-04-27")
#df.columns=["Açılış","En Yüksek","En Düşük","Kapanış","Hacim","Dividens","Stock Splits"]#kolon isimlerini değiştirdik
#st.dataframe(df)#tabloyu web sayfasında gösteririz
#st.line_chart(df["Kapanış"])#kapanışa göre graik çizimi
#st.line_chart(df["Hacim"])#hacime göre grafik çizimi

islem_turu=st.sidebar.radio("İşlem Türü",["Kripto","Borsa"])#sidebara yapıllacak işlemin seçilmesi için radiobar ekledik
if islem_turu == "Kripto":
    kriptosec=st.sidebar.selectbox("Kripto Para Türü",["BTC","ETH","XRP","DOT","DOGE","AVAX","BNB"])
    kriptosec=kriptosec+"-USD" #yahooda işlem yapabilmek için
    sembol=kriptosec
else:
    borsasec=st.sidebar.selectbox("Hisse Senetler",["ASELSAN","THY","GARANTİ","AKBANK","BJK"])
    senetler={
        "ASELSAN":"ASELS.IS",
        "THY":"THYAO.IS",
        "GARANTİ":"GARAN.IS",
        "AKBANK":"AKBNK.IS",
        "BJK":"BJKAS.IS"
    }
    hissesec =senetler[borsasec]
    sembol=hissesec

zaralık=range(1,720)
slider=st.sidebar.select_slider("Zaman Aralığı",options=zaralık,value=30)

bugun=datetime.today()
aralık=timedelta(days=slider)
st.sidebar.write("### Tarih Aralığı")

baslangic=st.sidebar.date_input("Başlangıç Tarihi", value=bugun-aralık) #başlangıç tarihi seçme
bitis=st.sidebar.date_input("Bitiş Tarihi", value=bugun)#bitiş tarihi seçme

st.sidebar.write("### Machine Learning Tahmin")
prophet=st.sidebar.checkbox("Facebook Prophet")

if prophet:
    fbaralık = range(1, 1441)
    fbper = st.sidebar.select_slider("Periyot", options=fbaralık, value=30)
    components=st.sidebar.checkbox("Components")
    cvsec = st.sidebar.checkbox("CV")
    if cvsec:
        st.sidebar.write("#### Metrik Seçiniz")
        metric = st.sidebar.radio("Metrik", ["rmse", "mse", "mape", "mdape"])

        st.sidebar.write("#### Parametre Seçiniz")
        inaralık = range(1, 144)
        cvint = st.sidebar.select_slider("İnitial", options=inaralık, value=120)

        peraralık = range(1, 144)
        cvper = st.sidebar.select_slider("CV Periyot", options=peraralık, value=30)

        horaralık = range(1, 144)
        cvhor = st.sidebar.select_slider("Horizon", options=horaralık, value=30)






#seçilen veriler göre grafik oluşturma
def grafikGetir(sembol,baslangıc,bitis):
    data = yf.Ticker(sembol)
    global df
    df=data.history(period="1d", start=baslangıc, end=bitis)
    st.line_chart(df["Close"])
    if prophet:
        # Zaman dilimini kaldır

        fb =df.reset_index()
        fb=fb[["Date","Close"]]#tarih ve kapanış sütunlarını alırız
        fb.columns=["ds","y"]
        fb['ds'] = fb['ds'].dt.tz_localize(None)
        global model
        model=Prophet()
        model.fit(fb)
        future=model.make_future_dataframe(periods=fbper)
        predict=model.predict(future)
        grap=model.plot(predict)
        st.write(grap)
        if components:
            grap2=model.plot_components(predict)
            st.write(grap2)

    else:
        st.sidebar.write("Olmadı")
            #predict=predict[["ds","trend"]]
            #predict=predict.set_index("ds")
            #st.line_chart(predict["trend"])

#Cross validation hesaplayan fonksiyon
def cvgrafik(model,initial,period,horizon,metric):
    initial=str(initial)+"days"
    period = str(period) + "days"
    horizon = str(horizon) + "days"
    cv = cross_validation(model, initial=initial, period=period, horizon=horizon)
    grap3=plot_cross_validation_metric(cv,metric=metric)
    st.write(grap3)


grafikGetir(sembol, baslangic, bitis)
if prophet:
    if cvsec:
        cvgrafik(model, cvint, cvper, cvhor, metric)

def indir(df):
    csv=df.to_csv()#tabloyu csv formatına çevirdik
    b64=base64.b64encode(csv.encode()).decode()#her şeyi dosya halinde çekmek için
    href=f'<a href="data:file/csv;base64,{b64}">CSV İndir</a>'
    return  href
st.markdown(indir(df),unsafe_allow_html=True)

def SMA(data,period=30,column="Close"):#sma indikatörü fonksiyonu
    return data[column].rolling(window=period).mean()
def EMA(data,period=21,column="Close"):
    return data[column].ewm(span=period,adjust=False).mean()#üstel ağırlıkları alırız
def MACD(data,period_long=26,period_short=12,period_signal=9,column="Close"):
    shortEMA=EMA(data,period_short,column=column)
    longEMA=EMA(data,period_long,column=column)
    data["MACD"]=shortEMA-longEMA
    data["Signal_Line"]=EMA(data,period_signal,column="MACD")
    return data
def RSI(data,period=14,column="Close"):
    delta=data[column].diff(1)
    delta=delta[1:]
    up=delta.copy()
    down=delta.copy()
    up[up<0]=0
    down[down>0]=0
    data["up"]=up
    data["down"]=down
    AVG_Gain=SMA(data,period,column="up")
    AVG_Loss=SMA(data,period,column="down")
    RS=AVG_Gain/AVG_Loss
    RSI=100.0-(100.0-(1.0+RS))
    data["RSI"]=RSI
    return  data

st.sidebar.write("### Finansal İndikatörler")
fi=st.sidebar.checkbox("Finansal İndikatörler")

def filer():
    if fi:
        fimacd = st.sidebar.checkbox("MACD")
        firsi = st.sidebar.checkbox("RSI")
        fisl = st.sidebar.checkbox("Signal Line")
        if fimacd:
            macd=MACD(df)
            st.write("MACD")
            st.line_chart(macd["MACD"])
        if firsi:
            rsi=RSI(df)
            st.write("RSI")
            st.line_chart(rsi["RSI"])
        if fisl:
            macd=MACD(df)
            st.write("Signal Line")
            st.line_chart(macd["Signal_Line"])



filer()




