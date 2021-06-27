# -*- coding: utf-8 -*-

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
dfs = dfs.set_index("Time")    
###### Definicion de plantas
#site = dfs.columns[50] # Guaymas
#site = dfs.columns[64] #Guaimaca
site = dfs.columns[87] #Caracol Knits

###### Series de tiempo
dfs["Año"] = dfs.index.year
dfs["Mensual"] = dfs.index.month
dfs["Mes por dia"] = dfs.index.day
dfs["Semana por dia"] = dfs.index.weekday
dfs["Por hora"] = dfs.index.hour

# Graficas
plt.figure(num = 1, figsize = (12, 6))
dfs[site].plot(marker='.', alpha=0.2, figsize=(12, 6))
plt.ylabel("Precios $/MWh")
plt.xlabel("Tiempo")
plt.title("Costos Marginales - "+site)
plt.show()

plt.figure(num = 2, figsize = (10, 6))
sb.boxplot(data = dfs, x = 'Año', y = site)
plt.title("Costos Marignales Promedio Anuales")
plt.show()

datype = ["Mensual", "Mes por dia", "Semana por dia", "Por hora"]
for tp, num in zip(datype, range(1,len(datype)+1)):
    plt.figure(num = num, figsize = (10,6))
    plt.title("Comparacion de CM "+tp+":2019 vs 2020 vs 2021")
    sb.lineplot(data = dfs.loc["2019-01":"2019-12"], x = tp, y = site, markers=True, dashes=False)
    sb.scatterplot(data = dfs.loc["2019-01":"2019-12"], x = tp, y = site, alpha = 0.1)
    sb.lineplot(data = dfs.loc["2020-01":"2020-12"], x = tp, y = site, markers=True, dashes=False)
    sb.scatterplot(data = dfs.loc["2020-01":"2020-12"], x = tp, y = site, alpha = 0.1)
    sb.lineplot(data = dfs.loc["2021-01":"2021-12"], x = tp, y = site, markers=True, dashes=False)
    sb.scatterplot(data = dfs.loc["2021-01":"2021-12"], x = tp, y = site, alpha = 0.1)
    plt.legend(["2019","2020","2021"])
    plt.show()

for tp, num in zip(datype, range(1,len(datype)+1)):
    plt.figure(num = num, figsize = (10,6))
    plt.title("Promedio CM Global "+tp)
    sb.lineplot(data = dfs.loc["2019-01":"2021-12"], x = tp, y = site, markers=True, dashes=False)
    sb.scatterplot(data = dfs.loc["2019-01":"2021-12"], x = tp, y = site, alpha = 0.025)
    plt.show()

plt.figure(num = 10, figsize = (10,6))
plt.title("Distribucion de precios")
sb.distplot(dfs[site].loc["2019-1":"2019-12"])
sb.distplot(dfs[site].loc["2020-1":"2020-12"])
sb.distplot(dfs[site].loc["2021-1":"2021-12"])
plt.legend(["2019","2020","2021"])
plt.show()

##### Pronostico de precio nodal diario 
pt0 = datetime.datetime(2022,1,1)
ptimevec = [pt0]
[ptimevec.append(ptimevec[-1] + datetime.timedelta(hours= 1)) for n in range(0,365*24) if ptimevec[-1]<datetime.datetime(2022,12,31,23)]
df19 = dfs[[site,"Por hora"]].loc["2019"]
df21 = dfs[[site,"Por hora"]].loc["2021"]
pdf = df19.append(df21)

#Global
predictarray = np.array(dfs[[site,"Por hora"]].loc["2019":"2021"])
daypow = [np.mean([p[0] for p in predictarray if n==p[1]]) for n in range(0,24)]
daystd = [np.std([p[0] for p in predictarray if n==p[1]]) for n in range(0,24)]
plt.figure(num = 11, figsize = (10,6))
plt.title("Perfil de CM diario - pronosticado")
plt.xlabel("Horas")
plt.ylabel("Costos Marginales [USD/MWh]")
plt.plot(daypow)
plt.fill_between(range(0,24),[x-s for x,s in zip(daypow, daystd)],[x+s for x,s in zip(daypow, daystd)], alpha = 0.3 )
anuCM = []
anuCMstd = []
[anuCM.extend(daypow) for n in range(0,365)]
[anuCMstd.extend(daystd) for n in range(0,365)]
dfexport = pd.DataFrame()
dfexport["Time"] = ptimevec
dfexport["USD/MWh"] = anuCM
dfexport["CM - STD"] = anuCMstd
dfexport = dfexport.set_index("Time")
#dfexport.to_excel("CM predictivos diarios.xlsx")

##Pre, Durante y Post Pandemia
predf = dfs[[site,"Por hora"]].loc["2019":"2020-03-11"]
durdf = dfs[[site,"Por hora"]].loc["2020-03-11":"2021-03"]
posdf = dfs[[site,"Por hora"]].loc["2021-03":"2021"]
dfvec = [predf,durdf,posdf]
Temp = ["Pre-pandemia","Durante pandemia", "Post-pandemia"]
for df,num,tit in zip(dfvec,range(0,3),Temp):
    predictarray= np.array(df)
    daypow = [np.mean([p[0] for p in predictarray if n==p[1]]) for n in range(0,24)]
    daystd = [np.std([p[0] for p in predictarray if n==p[1]]) for n in range(0,24)] 
    plt.figure(num = num, figsize = (10,6))
    plt.title("Perfil de CM diario - "+tit)
    plt.xlabel("Horas")
    plt.ylabel("Costos Marginales [USD/MWh]")
    plt.plot(daypow)
    plt.fill_between(range(0,24),[x-s for x,s in zip(daypow, daystd)],[x+s for x,s in zip(daypow, daystd)], alpha = 0.3 )
    plt.legend(["Precio promedio por hora", "Desviacion std. por hora"])

