# -*- coding: utf-8 -*-
from urllib.request import urlopen
from time import sleep
import re, os
import webbrowser
## "https://www.ods.org.hn/index.php/informes/costes-marginales/costosmarginales2019",
ODSurl = [
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/enero",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/febrero",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/marzocostosmarginales2020",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/abrilcostosmarginales2020",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/mayo",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/junio",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/julio",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/agosto",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/septiembre",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/octubre-cm20",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/noviembre-cm20",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2020/diciembrecostosm2020",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2021-costomarginales/enero21-costosmarginales",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2021-costomarginales/febrero21-costosmarginales",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2021-costomarginales/marzo21-costosmarginales",
          "https://www.ods.org.hn/index.php/informes/costes-marginales/2021-costomarginales/abril21-costosmarginales"       
          ]
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