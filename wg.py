#!/bin/python3
import socket 
import pandas as pd
from nltk import *
from subprocess import call
import subprocess
import os
from time import sleep,ctime
import time
import pygsheets
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import gspread_dataframe as gd
import numpy as np
#import wget
import requests as rq

data1={}
curlresponse=[]
ncat_status=[]
servername1=[]
Ct_time=[]
Ct_time.append(ctime())

#f = open("/etc/wireguard/wg.conf", "w")
#servername=input("Enter Server Name : \t")
servername= ['lux-71-06-01','lux-41-04-07','lux-12-06-16','lux-18-03-08','lux-14-06-01','lux-58-03-01','lux-03-14-01','lux-59-07-07','lux-47-01-03','lux-05-16-01','lux-15-13-02','lux-15-11-06','lux-03-17-01','lux-15-07-04','lux-01-27-01','lux-39-04-01','lux-15-11-04','lux-11-09-01']
#Username = input("Enter User Name : \t")
#a1=servername.replace("lux","sx")
#b1=a1.replace("-","")
#host=f'{b1}-wg.pointtoserver.com'
#port=434

#data1['servername']=[f'{servername}']
#data1['attempt_time']=[ctime()]

#f.write("[Interface] \n")
#f.write("PrivateKey = yI62GTvtUIBbfxxOxqrLYyD94UHIsHGLb0mCyv91s2I= \n")

#content='add:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='
#content1='remove:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='
credentials = ServiceAccountCredentials.from_json_keyfile_name('/etc/wireguard/svaccountkey.json')
gc = gspread.authorize(credentials)
sheet_instance = gc.open('Wg').sheet1
#existing = gd.get_as_dataframe(sheet_instance)
#print(existing)

def netcat(host, port, content):
    f = open("/etc/wireguard/wg.conf", "w")
    f.write("[Interface] \n")
    f.write("PrivateKey = yI62GTvtUIBbfxxOxqrLYyD94UHIsHGLb0mCyv91s2I= \n")
#content='add:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='
#content1='remove:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='
    status=""
    a2=""
    count = 0
    z=""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096)
        if not data:
            break
        a = str(data)
        a2 += a
        count +=1
        #print(count)
        #print(y1)
        if count > 1:
            a3 = (word_tokenize(a2))
           # data["ncat_response"]=[str(f"{a3[27]}")+" "+str(f"{a3[36]}")+" "+str(f"{a3[40]}")+" "+str(f"{a3[49]}")]
            if a3[27]=="":
                a4="False"
                f.close()
                break
            f.write("Address = "+ a3[27]+"/32"+"\n")
            f.write("DNS = " + a3[36]+","+a3[40]+"\n")
            f.write("\n")
            f.write("[Peer]"+"\n")
            f.write("PublicKey = "+ a3[49]+"\n")
            f.write("AllowedIPs = 0.0.0.0/0"+"\n")
            f.write(f"Endpoint = {b1}-wg.pointtoserver.com:51820 \n")
            f.write("PersistentKeepalive = 21"+"\n")
            f.close()
            print("Addition Successful")
            a4="True"
            #data1['ncatistatus']=[f"{status}"]
            break
    s.close()
    return a4

def browsing_downloading_test():
 p = subprocess.Popen(["curl", "ipinfo.io/ip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 a = str(p.stdout.read())
 b=a.replace("b","")
 if b=='':
    data1['curl_response']=["False"]
  
 data1['curl_response']=[f'{b}']
 print("Curl command response = "+b)
# p1=subprocess.Popen(["wget","--server-response","http://google.com 2>&1","|","awk","'/^","HTTP/{print $2}'","|","grep" ,"200"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# url= 'http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3'
 url="https://www.facebook.com"
#p = subprocess.Popen(["wget","--server-response","http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3","2>&1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#url = 'https://www.someurl.com'
# a=os.system(f"wget -c --read-timeout=5 --tries=0 {url}")
 #a=os.system("wget --server-response http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3 2>&1 | awk '/^  HTTP/{print $2}'| grep -e '200'")
# a=os.system("wget --server-response http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3 2>&1 | grep -c 'HTTP/1.1 200 OK'")
# print(a)
 a=rq.get(url)
 b=a.status_code
#b=str(p.stdout.read())
# c=str(p.stderr.read())
# print('wget response'+ str(b))
# print(c)
 if b==200:
   data1['wget_response']=['True']
 else:
   data1['wget_response']=['False']

def ncat_profile_remove(host,port,content1):
    a2=""
    count=0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content1.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096)
        if not data:
            break
        a = str(data)
        a2 += a
        count+=1
        if count >= 2:
         a3 = (word_tokenize(a2))
         #print(a3[14])
         if a3[14]=="Successful":
          print("removal request successful")
          break
         elif a3[14]=="failed":
          print("removal request failed")
          break
          
    s.close()    

#existing = gd.get_as_dataframe(sheet_instance)

#print(ctime())
#start = time.time()       
#netcat(host,port,content)
#end = time.time()
#print(ctime(end))
#print("Time taken for ncat request = "+ str(end-start))

count=0
#existing = gd.get_as_dataframe(sheet_instance)   
while True:
# servername= ['lux-71-06-01','lux-41-04-07','lux-12-06-16','lux-18-03-08','lux-14-06-01','lux-58-03-01','lux-03-14-01','lux-59-07-07','lux-47-01-03','lux-05-16-01','lux-15-13-02','lux-15-11-06','lux-03-17-01','lux-15-07-04','lux-01-27-01','lux-39-04-01','lux-15-11-04','lux-11-09-01']
#Username = input("Enter User Name : \t")
 c1=servername[count]  
 a1=c1.replace("lux","sx")
 b1=a1.replace("-","")
 host=f'{b1}-wg.pointtoserver.com'
 print(host)
 port=434
 data1['servername']=[f'{c1}']
#data1['attempt_time']=[ctime()]

#f.write("[Interface] \n")
#f.write("PrivateKey = yI62GTvtUIBbfxxOxqrLYyD94UHIsHGLb0mCyv91s2I= \n")

 content='add:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='
 content1='remove:purevpn0s9276335:vhgJZEAACdtIBKzZUoJgQUAPz33b5VPYK2nR/ejeT10='

   
 data1['attempt_time']=[ctime()]
# ncat_profile_remove(host,port,content1)
 nc=netcat(host,port,content)
 
 if nc=="True":
  data1['ncat_status']=[f'{nc}']
  os.system("wg-quick up wg")
  time.sleep(3)
  browsing_downloading_test()
  time.sleep(60)
  os.system("wg-quick down wg")
  time.sleep(10)
  try:
     ncat_profile_remove(host,port,content1)
  except:
     continue
  finally:
     print("onto next iteration")  
 
 elif nc=="False":
  data1["ncat_status"]=['false']
  data1["wget_response"]=['false']
  data1["curl response"]=['false']
 count+=1 
 if count > len(servername):
     break
 df = pd.DataFrame(data1)
 existing = gd.get_as_dataframe(sheet_instance)
 updated = existing.append(df)
 gd.set_with_dataframe(sheet_instance,updated)
 time.sleep(360)
#os.system("wg-quick up wg")
#browsing_downloading_test()
#time.sleep(120)

#os.system("wg-quick down wg")
#time.sleep(2)
#ncat_profile_remove(host,port,content1)

# df = pd.DataFrame(data1)
# updated = existing.append(df)
# gd.set_with_dataframe(sheet_instance,updated)
#time.sleep(60)


#def export_to_sheets(worksheet_name,df,mode='r'):
#    ws = gc.open("Wg").worksheet(worksheet_name)
#    if(mode=='w'):
#        ws.clear()
#        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=True,resize=True)
#        return True
#    elif(mode=='a'):
#        ws.add_rows(df.shape[0])
#        gd.set_with_dataframe(worksheet=ws,dataframe=df,include_index=False,include_column_header=False,row=ws.row_count+1,resize=False)
#        return True
#    else:
#        return gd.get_as_dataframe(worksheet=ws)
    
#df = pd.DataFrame.from_records([{'a': i, 'b': i * 2} for i in range(100)])
#import numpy as np
#df = pd.DataFrame(np.column_stack([servername1,Ct_time,ncat_status,curlresponse],columns=['Servername', 'Connection Time', 'NcatResponse','CurlResponse'])
#gd.set_with_dataframe(sheet_instance, df)
#export_to_sheets("Sheet1",df,'a')




#def runInParallel(*fns):
#  proc = []
#  for fn in fns:
#    p = Process(target=fn)
#    p.start()
#    proc.append(p)
#  for p in proc:
#    p.join()

#runInParallel(func1, func2)


