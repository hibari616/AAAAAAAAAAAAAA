global qq
global ww

############執行時開起網頁會有sleep睡眠等待3秒
############為了讓電腦能夠正確抓取資料所做的延遲
############執行完成會自動關閉不需要的網頁
############最後才會開啟我們要的網頁
def static1(urli):  ###先撈anime1.me的首頁資訊
    url = urli
    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    sp1=sp.find('tbody', {'class':'row-hover'})
    sp2 = sp1.find_all('tr', {'class':'row-2 even'})
    sp2 = sp1.find_all('td', {'class':'column-1'})
    sp3 = sp1.find_all('a', {'href':'/?cat=[0-9][0-9][0-9]'})
    data1={}
    
    for i in range(0,len(sp2)):
        temp=sp2[i]
        
    pat = '[0-9]+'
    for i in range(0,len(sp2)):
        temp=re.findall(pat, str(sp2[i]))
        temp="https://anime1.me/?cat="+str(temp[1])
        data1[str(sp2[i].text)]=(temp)
    return data1
def static2(st2):  #######根據使用者選擇的網頁進行讀取
    #####途中開起網頁是音為版權問題必須要載入網頁才能讀取資料
    url = st2
    html = requests.get(url)
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(st2)
    sp = BeautifulSoup(driver.page_source, 'html.parser')
    sp1= sp.find('div', {'id':'primary'})
    sp2= sp1.find('main', {'id':'main'})
    sp3 = sp2.find_all('a', {'rel':'bookmark'})
    pat='https://anime1.me/[0-9]+'
    data2={}
    for aa in range(1,len(sp3),3):
        temp=re.findall(pat, str(sp3[aa]))
        temp1=str(temp)
        str1=""
        for num in range(2,len(temp1)-2):
            str1+=temp1[num]
            
        data2[sp3[aa].text]=str1
    #print(data2)
    time.sleep(3)
    driver.close()
    return data2
def static3(st3):   ###############將選取的影片集數進行解析
    ###################
    html = requests.get(st3)
    #print(st3)
    sp1 = BeautifulSoup(html.text, 'html.parser')
    sp2=str(sp1.find('p'))
    sp3=sp2.split(" ")
    print(sp3)
    print(len(sp3))
    for k in range(len(sp3)):
        tempfin=""
        te=str(sp3[4])
        #if (len(sp3)==7):
        #    te1=str(sp3[6])
        if(te.find("drive.google.com")!=-1):
            print(te)
            tempgoogle=str(sp3[4])
            for l in range(5,len(tempgoogle)-1):
                tempfin=tempfin+tempgoogle[l]
            break
        #elif(te1.find("https://p.anime1.me/pic.php?id=")):
        if (len(sp3)==7):
            te1=str(sp3[5])
            print(te1+"test")
            ##print(sp3)
            sp4=te1
            tempfin="https://p.anime1.me/pic.php?id="
            pat='[0-9]+'
            temparr=re.findall(pat, (sp4))
            tempfin=tempfin+temparr[1]
            break
        else:
            break
    urlwork=tempfin
    print(urlwork)
    return urlwork
def static4(st4):  #####解析影片原始資料庫位子   直接抓取影片MP4路徑
    ##############開起網頁是為了先讓他執行JAVASCRIPT與法
    ##############執行完成後才會提供所有資料
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(st4)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    #for block in soup.select('.name'):
        #print(block.text)
    sp1=soup.find('div', {'id':'player'})
    sp2=sp1.find('video',{'class':'jw-video jw-reset'})
    sp3=str(sp2)
    sp4=sp3.split(" ")
    sp5=str(sp4[7])
    tempsp=""
    for bfstr in range(5,len(sp5)-1):
        tempsp=tempsp+sp5[bfstr]
    tempsp=tempsp.replace("amp;","")
    print(tempsp)
    driver.close()    
    return tempsp
########################################### GUI
def printList(event):   ##########第一次選擇影片名稱時觸發
    global var1
    print(lb.get(lb.curselection())) 
    var1=lb.get(lb.curselection())
    #pw=lb.get(lb.curselection())
    win.destroy()
    return var1
def printList1(event):  ############在選擇影片集數時觸發
    global var2
    print(lb.get(lb.curselection())) 
    var2=lb.get(lb.curselection())
    #pw=lb.get(lb.curselection())
    win.destroy()
    return var2
####################################################
#def checkPW():
#    if(pw.get() == "1234"):
#        msg.set("上一夜！")
#    else:
#        msg.set("密碼錯誤，請修正密碼！")
####################################################
#def checkPW1():
#    if(pw.get() == "1234"):
#        msg.set("下一夜！")
#    else:
#        msg.set("密碼錯誤，請修正密碼！")
################################################## MAIN
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import tkinter as tk
import time
url='https://anime1.me/'
userInput=""
userstat=1
usertemp=""
dat1=dat2=dat3=[]
var=""
while(userInput!="end"):    ########用來做終止條件的程式碼
    win = tk.Tk()
    count=0
   
    if(userstat==1):   #######起始狀態 選擇影片名稱
                    #######建構起始GUI介面
                    #######顯示網頁中多個影片名稱
                    ######並可使用滑鼠滾輪上下滑動
                    ######將使用者選擇的影片資料傳送給下一個區塊處理
        dat1=[]
        stat=-1
        select1=static1(url)
        selist=""
        while(stat==-1):
            count=1
            scrolly = tk.Scrollbar(win)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            lb = tk.Listbox(win, yscrollcommand=scrolly.set)
            lb.bind('<Double-Button-1>',printList)
            for i in select1:
                dat1.append(i)
                ###############print("{}:{}".format(count,i))
                count=count+1
            ###
            ##################print(dat1)
            for i in range(len(dat1)-1):
                count=count+1
                a=lb.insert(tk.END,dat1[i])
                
                
            lb.pack()
            win.mainloop()
            ###############print("回傳值"+var1)
            ################print(printList)
            ###
            userInput
            for i in range(len(dat1)):
                if(dat1[i]==var1):
                    t1=int(i+1)
                    userInput=str(t1)    
                    ##########print(dat1[i],i)
            #userInput=input("輸入選擇的編號:")
            if(userInput.isdigit()):
                if((int(userInput)>0)and((int(userInput)-1)<=len(select1))):
                    usertemp=dat1[int(userInput)-1]
                    userstat=2
                    stat=0
                else:
                    stat=-1
            elif(userInput=="end"):
                break
    elif(userstat==2):  #########選擇影片集數的處理區塊
        #############以及建構GUI介面
        ############將使用者選擇的資料做比對並傳值給下一個區塊
        dat2=[]
        select2=static2(select1[usertemp])
        stat=-1
        while(stat==-1):
            count=1
            
            for i in select2:
                dat2.append(i)
                print("{}:{}".format(count,i))
                count=count+1
            scrolly = tk.Scrollbar(win)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            lb = tk.Listbox(win, yscrollcommand=scrolly.set)
            
            selist=lb.bind('<Double-Button-1>',printList1)
            for i in range(len(dat2)-1):
                count=count+1
                a=lb.insert(tk.END,dat2[i])
                
                
            lb.pack()
            win.mainloop()
            print("var2"+var2)
            for i in range(len(dat2)):
                if(dat2[i]==var2):
                    t1=int(i)
                    userInput=str(t1)    
                    print(dat2[i],(i))
            ###################################
            #userInput=input()
            print(select2)
            if(userInput.isdigit()):
                if((int(userInput)>0)and((int(userInput)-1)<=len(select1))):
                    usertemp=dat2[int(userInput)]
                    #print(usertemp)
                    usertemp=select2[usertemp]
                    #print(usertemp)
                    userstat=3
                    stat=0
                else:
                    stat=-1
    elif(userstat==3):
        dat3=[]
        #select3=static3(select2[usertemp])
        #print("user"+usertemp)
        select3=static3(usertemp)
        #print("static3"+select3)
        #print("static3google:",end="")
        #print(select3.find("google"))
        #print("static3anime:",end="")
        #print(select3.find("anime"))
        if(select3.find("google")!=-1):  ####判斷影片來源是否為google雲端
            #print("google"+select3)
            fin=select3
        elif(select3.find("anime")!=-1):  #####判斷影片來源是否為站內空間
            fin=static4(select3)
            print(fin)
        else:                        
            #####因此網站只使用google及站內空間存放影片
            #####若都不是則表示影片已經下架了
            print("此影片已經下架")
            userInput="end"
            break
        print(fin)
        time.sleep(3)
        userstat=1
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(fin)
        driver.close()
        break
#print(data1["極道超女"])
#print(sp1)
###########################################################################

##########################################################################
#url = data2['極道超女 [12]']


##########################################################################
