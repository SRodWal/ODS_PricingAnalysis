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
####### Leer archivos en carpeta de datos

files = [f for f in os.listdir('.') if os.path.isfile(f)]
folderdir = "Desktop/Documents/Work/ODS Price analysis/Data"
filetype = ".xlsx"
mypath = folderdir+"/**/*"+filetype

names = []
for f in files:
    if filetype in f:
        names.append(f)


######### Definimos variables
#Meses de estudio: Enero, Febrero y Marzo (2021)
weeks = [5,4,4,5]
month = [12,1,2,3]
def monthNum(num):
    return {1 : "Ene21", 2:"Feb21",3:"Mar21",12:"Dic20"}[num]

filenames = []
for w,m in zip(weeks,month):
    for l in range(1,w+1):
        name = "Data/CM_"+monthNum(m)+"_S"+str(l)+".xlsx"
        filenames.append(name)
    
dfs = []
master_dfs = []
k=0
for file in filenames:
    df = pd.read_excel(file)
    df.drop(labels = 0, axis=0, inplace = True)
    if file==filenames[0]:
        dfs=df.drop(labels = df.columns[0], axis=1, inplace = False)
    else:
        dfs = dfs.append(df.drop(labels = df.columns[0], axis=1, inplace = False), ignore_index = True)
    master_dfs.append(df)    
 
for name in dfs.columns:
    df = dfs[name]
    df = pd.to_numeric(df, errors = "coerce")
    dfs[name] = df
 
############ Price Distribution ###############
#for name in dfs.columns:
#    plt.figure(figsize = (10,8))
#    plt.title("Distribucion "+name+" N="+str(dfs[name].describe().loc[["count"]][0]) )
#    sb.distplot(dfs[name])
#    plt.show()
    
#statdat = dfs.describe().T
#statdat.to_excel("Global Review.xlsx")

#Generar el vector de tiempo
timevec = []
weekvec = [[dfs.head(0) for i in range(24)] for i in range(7)]
dayvec = [dfs.head(0) for i in range(24)]
for df in master_dfs:
    n = df.columns[0]
    timevec.extend(df[n])
    
####### Analisis por semana #########
k=0
for t, row in zip(timevec ,dfs.loc):
     day = t.weekday()
     hour = t.hour
     weekvec[day][hour]=weekvec[day][hour].append(row)
     dayvec[hour] = dayvec[hour].append(row)

price_week = dfs.head(0)
price_hour = dfs.head(0)
for i in range(7):
    for j in range(24):
        price_week = price_week.append(weekvec[i][j].describe().loc[['mean']])
        
for i in range(24):
    price_hour = price_hour.append(dayvec[i].describe().loc[['mean']])