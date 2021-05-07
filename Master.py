# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:05:33 2021

@author: serw1
"""

import pandas as pd
import datetime, os, calendar
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
#######
def monthNum(num):
    return {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",
            8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}[num]


####### Leer archivos en carpeta de datos
folderdir = os.getcwd()+"\\Data"
filetype = ".xlsx"
files = [f for f in os.listdir(folderdir) if "CM" in f]

######## Ordenar archivos por fecha e importar archivos
yrs = [19,20,21]
names = []
for y in yrs:
    bag = [f for f in files if str(y) in f]
    for m in range(1,13):
        names.extend([f for f in bag if monthNum(m) in f])
dfs = pd.DataFrame()
dfs_store = []
for f in names:
    df = pd.read_excel("Data/"+f)
    df = df.rename(columns = {df.columns[0]: 'Time'})
    if df.loc[0][3]=="$/MWh":
        df.drop(index = 0, axis = 0, inplace = True)       
    dfs = dfs.append(df, ignore_index = True)

for name in dfs.columns[1:len(dfs.columns)]:
    dfs[name] = dfs[name].astype(float)
#### Hora inicial de estudio Primero de junio del 19
t0 = datetime.datetime(2019, 6, 1)
timevec = [t0]
for i in range(1,len(dfs)):
    timevec.append(timevec[-1]+datetime.timedelta(hours = 1))
dfs["Time"] = timevec  
    
###### Definicion de plantas
planta = 51

###### Series de tiempo
###### statdat[Tipo de dato - mean, std min/max][serie de tiempo - ]
emptydf = pd.DataFrame()
statsdata = [] 
stats = ["mean","std",["min","max"]]  
weekvec = [emptydf for i in range(0,7)]
weeklyvec = [emptydf for i in range(0,54)]
dayvec = [emptydf for i in range(0,31)]
monthvec = [emptydf for i in range(0,12)]
hourvec = [emptydf for i in range(0,24)]
pool = [weekvec, weeklyvec,dayvec,monthvec,hourvec]
for t,i in zip(timevec, range(0,len(timevec))):
    weekvec[t.weekday()-1] = weekvec[t.weekday()-1].append(dfs.loc[i])
    weeklyvec[t.isocalendar()[1]] = weeklyvec[t.isocalendar()[1]].append(dfs.loc[i])
    dayvec[t.day-1] = dayvec[t.day-1].append(dfs.loc[i])
    monthvec[t.month-1] = monthvec[t.month-1].append(dfs.loc[i])
    hourvec[t.hour] = hourvec[t.hour].append(dfs.loc[i])
    
poollis = [[df.describe() for df in dat if not(df.empty)] for dat in pool]    
statdat = [[] for i in range(0,len(stats))]
for s, dat in zip(stats, statdat):
    [dat.append([df.loc[s] for df in lis]) for lis in poollis]
