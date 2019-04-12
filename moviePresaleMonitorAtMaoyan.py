import time 
import requests
import traceback
from wxpy import *
from lxml import etree
import tkinter as tk
from tkinter import messagebox

def getOneUrl(url):
    try:
        r=requests.get(url,timeout=30)
        #r.encoding=r.apparent_encoding
        return r.text
    except:
        traceback.print_exc()
        return None

def showMsg(astr):#astr:需要显示的文本
    window = tk.Tk()
    window.title(astr)
    window.geometry('400x400')
    tk.Button(window,text=astr).pack()
    window.mainloop()


def monitorBtnbuy(url,t=0):
    bot = Bot()
    while True:
        txt=getOneUrl(url)
        if txt==None:
            #time.sleep(2)
            pass
        else: 
            html=etree.HTML(txt)
            try:
                ptxt=html.xpath('/html/body/div[3]/div/div[2]/div[2]/a/text()')
                if ptxt==[]:
                    if t%5==0:
                        print('现在是{0},还没有预售信息；t={1}'.format(time.asctime(),t))
                        time.sleep(180)
                    if t%2==0:
                        time.sleep(15*60) #15分钟
                    time.sleep(120)
                elif ptxt[0]=='特惠购票': #赶紧想办法提醒自己
                    print(time.asctime(),ptxt[0],url)
                    group = bot.groups().search('def-self')[0] #给特定的群里发消息
                    group.send('预售开始！')
                    group.send(url)
                    print('msg.send()')
                    showMsg('Avengers: Endgame')
            except:
                traceback.print_exc()
        time.sleep(5)
        t+=1
        #if t>20:break


def monitorZhongguanc(url,t=0,ts=1):#对特定商圈的监测
    had=False
    while True: #主循环
        try:
            txt=requests.get(url).text
            html=etree.HTML(txt)
            mlst=html.xpath('//*[@id="app"]/div[2]/div[*]/div[1]/a/text()')
            mlen=len(mlst)
            if mlen>t:
                had=True
                for i in range(t,mlen):
                    print("add{0}".format(mlst[i]))
                print(mlst,url)
                t=mlen
                showMsg('zhongguanc')
                

            if had:
                had=False
            else:
                lct=time.localtime()
                if lct.tm_min>50: #50-60
                    ts=2
                elif lct.tm_min>35:#36-49
                    ts=5
                elif lct.tm_min>20: #21-34
                    ts=10
                elif lct.tm_min>15: #16-20
                    ts=4
                else: #0-15
                    ts=1
                    print('现在是{0},还没有预售消息;{1}'.format(time.asctime(),t))
                time.sleep(60*ts) #sleep一段时间继续爬页面

        except:#输出错误信息
            traceback.print_exc()
        time.sleep(ts) 



def monitorMeijia(url,t=0,ts=1):#对特定电影院特定电影的监测
    while True: #主循环
        try:
            txt=requests.get(url).text
            html=etree.HTML(txt)
            mlst=html.xpath('//*[@id="app"]/div[1]/div')[0].getchildren()
            had=False
            for m in mlst:
                mid=m.attrib.get('data-movieid',0)
                if mid=='248172':
                    print('电影院开启预售了！！{0}\n {1}'.format(time.asctime(),url))
                    had=True
                    break
            if had:
                showMsg('meijia')
            else:
                lct=time.localtime()
                if lct.tm_min>50: #50-60
                    ts=2
                elif lct.tm_min>35:#36-49
                    print('现在是{0},还没有预售消息,{1}'.format(time.asctime(),t))
                    ts=5
                elif lct.tm_min>20: #21-34
                    ts=10
                elif lct.tm_min>15: #16-20
                    ts=7
                else: #0-15
                    ts=1
                    print('现在是{0},还没有预售消息,t={1}'.format(time.asctime(),t))
                time.sleep(60*ts) #sleep一段时间继续爬页面

        except:#输出错误信息
            traceback.print_exc()
        time.sleep(ts) 
        t+=1
        if t>5000:
            break #因为是测试所以加了个break
        
        
url1='https://maoyan.com/films/1156894'
url='https://maoyan.com/films/248172' #Avengers: Endgame
#monitorBtnbuy(url,t=0)

#murl='https://maoyan.com/cinemas?movieId=248172&brandId=-1&areaId=688&districtId=17'
#monitorZhongguanc(murl,t=1,ts=1)
murl='https://maoyan.com/cinema/197?poi=279439&movieId=248172'
monitorMeijia(murl,t=0,ts=1)



#功能：对猫眼电影上特定电影、商圈+电影；电影院+电影 是否预售进行监测
