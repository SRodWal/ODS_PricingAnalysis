# -*- coding: utf-8 -*-
from urllib.request import urlopen
from time import sleep
import re, os
import webbrowser

#Import data sources:
s_dir = os.getcwd()
fileloc = [f for f in os.listdir(s_dir) if "ODS" in f][0]
urllist = open(s_dir+"\\"+fileloc).readlines()
ODSurl = [f.replace("\n","").replace(" ","") for f in urllist]

ODSurl=ODSurl[len(ODSurl)-2:len(ODSurl)] # Updates last two month
#List of webpages to search
Meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
#This will order the month list to correspond the ODS links.
meses = []
for l in ODSurl:
    for m in Meses:
        if m.lower() in l:
            meses.append(m)

#Defines download, repository, and browser's directory
brow = r"C:\\Users\\serw1\\AppData\\Local\\Programs\\Opera\\launcher.exe"
downpath = "C:/Users/serw1/Downloads"
scrippath = os.getcwd().replace("\\","/")
pdfpath = scrippath+"/Data/DailyReports"
excelpath = scrippath+"/Data"
filetype = ".xlsx"

# Location of download files and storage 
for url, mes in zip(ODSurl,meses):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    data = re.findall("href=.*?"+filetype,html)
    webbrowser.register("opera", None,webbrowser.BackgroundBrowser(brow))
    op  =  webbrowser.get("opera")
    print("Iniciando mes de "+mes+". Total de archivos: "+str(len(data)))
    for l, s in zip(data, range(1,len(data)+1)):
        if not("www.ods.org" in l):
            l = l.replace('href="',"https://www.ods.org.hn")
        yr = l[-7:-5]
        links = (l[l.find("http"):len(l)])
        fileloc = downpath+"/"+links[links.find("Precios"):len(links)]
        fileout = "CM_"+mes+str(yr)+"_S"+str(s)+filetype
        outloc = excelpath+"/"+fileout
        print("Downloading file : "+links[links.find("Precios"):len(links)])
        op.open_new_tab(links)
        sleep(9)
        print("Moving and renaming : "+fileout)
        try:
            os.rename(fileloc,outloc)
        except FileNotFoundError:
            print("File not found in downloads")
            pass
        except FileExistsError:
            print("File already on directory - deleting file.")
            os.remove(fileloc)     
        print("Operation Completed")